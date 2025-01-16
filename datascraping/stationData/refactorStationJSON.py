import os
import json

station_data = {}
file_path = os.path.join("datascraping\stationData", "station.json")
with open(file_path, 'r', encoding="utf-8") as file:
    station_data = json.load(file)

reformatted_station_data = {}
for station_name in station_data:
    station = station_data[station_name]
    station_id = station["id"]
    data = {}
    data["name"] = station_name
    data["lines"] = station["lines"]
    data["coords"] = station["coords"]
    reformatted_station_data[station_id] = data

folder = "datascraping/stationData"
os.makedirs(folder, exist_ok=True)
with open(os.path.join(folder, "station_ids.json"), "w", encoding="utf-8") as json_file:
    json.dump(reformatted_station_data, json_file, indent=4, ensure_ascii=False)