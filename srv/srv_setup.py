import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import json

cred = credentials.Certificate('./.env/ontime-e0281-firebase-adminsdk-ytrxe-16671a0c2b.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ontime-e0281-default-rtdb.europe-west1.firebasedatabase.app',
    'databaseAuthVariableOverride': None
})


station_data = {}
file_path = os.path.join("datascraping\stationData", "station_ids.json")
with open(file_path, 'r', encoding="utf-8") as file:
    station_data = json.load(file)

env_data_template = {}
file_path = os.path.join("json_templates", "environmental-data.json")
with open(file_path, 'r', encoding="utf-8") as file:
    env_data_template = json.load(file)

setup_json = {}
for id in station_data:
    station = station_data[id]
    json_data = {}
    for line in station["lines"]:
        json_data[line] = env_data_template
    setup_json[id] = json_data

ref = db.reference('/stations')
ref.set(setup_json)