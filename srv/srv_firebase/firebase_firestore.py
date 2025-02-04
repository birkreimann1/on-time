import os
from google.cloud import firestore
from google.oauth2 import service_account
from srv.config import STATION_DATA_PATH
import json
from srv.srv_logging.logger import log

service_account_file = "./.env/ontime-e0281-firebase-adminsdk-ytrxe-54e35eba18.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_file
db = firestore.Client()

def upload_station_data_to_firebase(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    doc_ref = db.collection("stations")
    for station_id, station_info in data.items():
        doc_ref.document(station_id).set(station_info)
    
    log("Station data uploaded to Firebase.", category='FIREBASE', priority='INFO')

if __name__ == "__main__":
    upload_station_data_to_firebase(STATION_DATA_PATH)
