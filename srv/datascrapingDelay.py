import requests
import time
import os.path
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from weatherdata import readData as weather

cred = credentials.Certificate('./.env/ontime-e0281-firebase-adminsdk-ytrxe-372c88d62b.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ontime-e0281-default-rtdb.europe-west1.firebasedatabase.app',
    'databaseAuthVariableOverride': None
})

bus_lines = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
             "12", "15", "16", "17", "18", "21", "24", "25", "26", "30",
             "31", "32", "33", "34", "35", "36", "38", "39", "40", "50"]

scraping_interval_minutes = 20
scraping_interval_seconds = 60*scraping_interval_minutes
ref_root = "/stations_new_score"

def checkRequestLimit(response, url):
    if response.status_code in {429, 502, 503}:
        retry_after = int(response.headers.get('Retry-After', 5))  # Default to 60 seconds if not found
        print(f"Rate limit exceeded. Retrying in {retry_after} seconds.")
        time.sleep(retry_after)
        response = requests.get(url)
        response = checkRequestLimit(response, url)
    return response

def getStationData():
    #folder = "datascrapingDelayData"
    folder = "datascrapingSWHL"
    os.makedirs(folder, exist_ok=True)

    #time = datetime.datetime.now()
    #time_formatted = re.sub(r'[-:., ]', '_', str(time))

    station_data = {}
    file_path = os.path.join("datascraping", "stationData", "station_ids.json")
    with open(file_path, 'r', encoding="utf-8") as file:
        station_data = json.load(file)

    station_nr = 0
    
    for id in station_data:
        station_nr += 1
        station = station_data[id]
        coords = station["coords"]
        current_env_data = weather.getDataByCoords(float(coords["lat"]),float(coords["long"]))

        url = f"https://netzplan.swhl.de/api/v1/stationboards/hafas/{id}?v=0&limit=300"
        response = requests.get(url)
        response = checkRequestLimit(response, url)
        if response.status_code == 200:
            json_data = response.json()
            ref_path = f"{ref_root}/{id}/env_data"
            ref = db.reference(ref_path)
            ref.set(current_env_data)
            if response.text == '{"data":[]}':
                print(f'[{station_nr}/{len(station_data)}] WARNING: Failed to extract data about station {station["name"]} at ID {id}')
                continue
            if "data" in json_data and isinstance(json_data["data"], list):
                for transit in json_data["data"]:
                    if "time" in transit and "realtime" in transit:
                        current_line = transit["line"]["name"]
                        current_time = int(time.time())
                        transit_realtime = int(transit["realtime"])
                        arrival_in = transit_realtime - current_time
                        if arrival_in > -60 and arrival_in <= scraping_interval_seconds and current_line in bus_lines:
                            delay = transit_realtime - int(transit["time"])
                            cancelled = bool(transit["cancelled"])
                            delay_type = getDelayType(delay, cancelled)
                            ref_path = f"{ref_root}/{id}/lines/{current_line}"
                            ref = db.reference(ref_path)
                            env_data = ref.get()
                            if not env_data:
                                ref_path = f"{ref_root}/{id}/lines"
                                ref = db.reference(ref_path)
                                current_line_data = ref.get()
                                data_by_env_file_path = os.path.join("json_templates", "data_by_env.json")
                                with open(data_by_env_file_path, 'r', encoding="utf-8") as file:
                                    data_by_env = json.load(file)
                                current_line_data.update({current_line: data_by_env})
                                ref.set(current_line_data)
                                ref_path = f"{ref_root}/{id}/lines/{current_line}"
                                ref = db.reference(ref_path)
                                env_data = ref.get()
                                station["lines"].append(current_line)
                                with open(file_path, "w", encoding="utf-8") as json_file:
                                    json.dump(station_data, json_file, indent=4, ensure_ascii=False)
                            for factor_name in env_data:
                                env_data = setEnvData(env_data, delay, delay_type, current_env_data[factor_name], factor_name)
                            writeEnvData(id, current_line, env_data)
                        elif arrival_in > (scraping_interval_seconds + 300):
                            break
            print(f'[{station_nr}/{len(station_data)}] Parsed station {station["name"]} at ID {id}')
        else:
            print(f"Failed to retrieve JSON. Status code: {response.status_code}")

def setEnvData(env_data, delay, delay_type, factor_data, factor_type):
    for factor in factor_data:
        if(delay > 0):
            env_data[factor_type][factor]["delay_info"][delay_type] = int(env_data[factor_type][factor]["delay_info"][delay_type]) + 1
            delay_total = int(env_data[factor_type][factor]["delay_total"])
            new_delay_total = delay_total + 1
            average_delay = float(env_data[factor_type][factor]["average_delay"])
            new_average_delay = str((average_delay * delay_total + delay)/new_delay_total)
            env_data[factor_type][factor]["delay_total"] = str(new_delay_total)
            env_data[factor_type][factor]["average_delay"] = str(new_average_delay)
        delay_score = createDelayScore(env_data[factor_type][factor]["delay_info"], int(env_data[factor_type][factor]["data_size"]) + 1)
        factor_data_size = int(env_data[factor_type][factor]["data_size"]) + 1
        env_data[factor_type][factor]["score"] = delay_score
        env_data[factor_type][factor]["data_size"] = str(factor_data_size)
    return env_data

def getDelayType(delay, cancelled):
    if delay == 0:
        return "punctual"
    elif 0 < delay < 300:
        return "short"
    elif 300 <= delay < 900:
        return "medium"
    elif 900 <= delay < 1800:
        return "long"
    elif 1800 <= delay:
        return "extreme"
    elif cancelled:
        return "cancelled"


def writeEnvData(id, current_line, env_data):
    line_ref_path = f"{ref_root}/{id}/lines/{current_line}"
    line_ref = db.reference(line_ref_path)
    line_ref.set(env_data)

def createDelayScore(delay_info, data_size):
    delay_score = round(100 * (1 - (float(delay_info["short"]) * 0.5 + float(delay_info["medium"]) * 0.6
                   + float(delay_info["long"]) * 0.7 + float(delay_info["extreme"]) * 0.8
                   + float(delay_info["cancelled"]) * 1.0)/float(data_size)), 2)
    return delay_score

#delay_array = np.linspace(0, 1800, 31)
#for delay in delay_array:
#    delay_score = createDelayScore(delay)
#    print(delay_score)

#start_time = time.time()
#getStationData()
#while True:
#    if time.time() - start_time >= scraping_interval_seconds:
#        print(time.time() - start_time)
#        start_time = time.time()
#        getStationData()
