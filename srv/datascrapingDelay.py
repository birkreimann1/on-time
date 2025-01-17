import requests
import time
import os.path
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from weatherdata import readData as weather

cred = credentials.Certificate('./.env/ontime-e0281-firebase-adminsdk-ytrxe-16671a0c2b.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ontime-e0281-default-rtdb.europe-west1.firebasedatabase.app',
    'databaseAuthVariableOverride': None
})

bus_lines = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
             "12", "15", "16", "17", "18", "21", "24", "25", "26", "30",
             "31", "32", "33", "34", "35", "36", "38", "39", "40", "50"]

scraping_interval_minutes = 20
scraping_interval_seconds = 60*scraping_interval_minutes

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

        url = f"https://netzplan.swhl.de/api/v1/stationboards/hafas/{id}?v=0&limit=1000"
        response = requests.get(url)
        response = checkRequestLimit(response, url)
        if response.status_code == 200:
            json_data = response.json()
            if "data" in json_data and isinstance(json_data["data"], list):
                for transit in json_data["data"]:
                    if "time" in transit and "realtime" in transit:
                        current_line = transit["line"]["name"]
                        current_time = int(time.time())
                        transit_time = int(transit["time"])
                        if (transit_time - current_time) <= scraping_interval_seconds and current_line in bus_lines:
                            delay = int(transit["realtime"]) - transit_time
                            delay_score = createDelayScore(delay)
                            ref_path = f"/stations/{id}/{current_line}"
                            ref = db.reference(ref_path)
                            env_data = ref.get()
                            if not env_data:
                                ref_path = f"/stations/{id}"
                                ref = db.reference(ref_path)
                                current_line_data = ref.get()
                                current_file_path = os.path.join("json_templates", "environmental-data.json")
                                with open(current_file_path, 'r', encoding="utf-8") as file:
                                    current_station_data = json.load(file)
                                current_line_data.update({current_line: current_station_data})
                                ref.set(current_line_data)
                                ref_path = f"/stations/{id}/{current_line}"
                                ref = db.reference(ref_path)
                                env_data = ref.get()
                                station["lines"].append(current_line)
                                with open(file_path, "w", encoding="utf-8") as json_file:
                                    json.dump(station_data, json_file, indent=4, ensure_ascii=False)
                            for factor_name in env_data:
                                env_data = setEnvData(env_data, delay_score, current_env_data[factor_name], factor_name)
                            writeEnvData(id, current_line, env_data)                           
            print(f"Parsed station {station["name"]} at id {id}")
        else:
            print(f"Failed to retrieve JSON. Status code: {response.status_code}")

def setEnvData(env_data, delay_score, factor_data, factor_type):
    for factor in factor_data:
        factor_score = float(env_data[factor_type][factor]["score"])
        factor_data_size = int(env_data[factor_type][factor]["data_size"])
        new_factor_data_size = factor_data_size + 1
        new_factor_score = str((factor_score * factor_data_size + delay_score)/new_factor_data_size)
        env_data[factor_type][factor]["score"] = new_factor_score
        env_data[factor_type][factor]["data_size"] = str(new_factor_data_size)
    return env_data

def writeEnvData(id, current_line, env_data):
    light_ref_path = f"/stations/{id}/{current_line}"
    light_ref = db.reference(light_ref_path)
    light_ref.set(env_data)

def createDelayScore(delay):
    delay_score = round(100 - delay/18, 2)
    if delay_score < 0:
        delay_score = 0
    return delay_score

#delay_array = np.linspace(0, 1800, 31)
#for delay in delay_array:
#    delay_score = createDelayScore(delay)
#    print(delay_score)
