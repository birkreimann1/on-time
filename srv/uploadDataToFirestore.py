import os
from google.cloud import firestore
from google.oauth2 import service_account
import json

service_account_file = "./.env/ontime-e0281-firebase-adminsdk-ytrxe-54e35eba18.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_file

db = firestore.Client()

file_path = os.path.join("datascraping\stationData", "station_ids.json")
with open(file_path, 'r') as file:
    data = json.load(file)

doc_ref = db.collection("stations")
for id in data:
    doc_ref.document(id).set(data[id])