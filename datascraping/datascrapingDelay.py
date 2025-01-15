import requests
import datetime
from time import sleep
import os.path
import json
import re

#folder = "datascrapingDelayData"
folder = "datascrapingSWHL"
os.makedirs(folder, exist_ok=True)

time = datetime.datetime.now()
time_formatted = re.sub(r'[-:., ]', '_', str(time))

station_data = {}
file_path = os.path.join("stationData", "station.json")
with open(file_path, 'r', encoding="utf-8") as file:
    station_data = json.load(file)

def checkRequestLimit(response):
    if response.status_code in {429, 502, 503}:
        retry_after = int(response.headers.get('Retry-After', 5))  # Default to 60 seconds if not found
        print(f"Rate limit exceeded. Retrying in {retry_after} seconds.")
        sleep(retry_after)
        response = requests.get(url)
        response = checkRequestLimit(response)
    return(response)

station_nr = 0

for station in station_data:
    station_nr += 1 
    id = station_data[station]["id"]
    url = f"https://netzplan.swhl.de/api/v1/stationboards/hafas/{id}?v=0&limit=10000"
    response = requests.get(url)
    response = checkRequestLimit(response)
    if response.status_code == 200:
        json_data = response.json()
        filename = f"{id}_{time_formatted}.json"
        filepath = os.path.join(folder, filename)
        with open(filepath, 'w') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        print(f"Station {station_nr}/{len(station_data)}: {station}")
    else:
        print(f"Failed to retrieve JSON. Status code: {response.status_code}")