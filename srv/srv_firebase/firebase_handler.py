import firebase_admin
from firebase_admin import credentials, db

firebase_ref = "/stations_test"

def initialize_firebase():
    cred = credentials.Certificate('./.env/ontime-e0281-firebase-adminsdk-ytrxe-54e35eba18.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ontime-e0281-default-rtdb.europe-west1.firebasedatabase.app',
        'databaseAuthVariableOverride': None
    })

def set_firebase_data(ref_path, data):
    """Sets data to a specific Firebase reference path."""
    db.reference(ref_path).set(data)

def get_firebase_data(ref_path):
    """Fetches data from a specific Firebase reference path."""
    return db.reference(ref_path).get()
