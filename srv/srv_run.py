import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('./.env/ontime-e0281-firebase-adminsdk-ytrxe-16671a0c2b.json')

# Initialize the app with the service account credentials
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ontime-e0281-default-rtdb.europe-west1.firebasedatabase.app',
    'databaseAuthVariableOverride': None
})

# The app only has access to public data as defined in the Security Rules
ref = db.reference('/stations')
ref.set({
    '9006091': {
        'lines': {
            "7": {
                "headsigns": {
                    "Bad Schwartau ZOB": {
                        "attr": "test"
                    },
                    "Bornkamp": {
                        "attr": "test"
                    }
                }
            },
            "9": {
                "headsigns": {
                    "Bad Schwartau ZOB": {
                        "attr": "test"
                    },
                    "Grillenweg": {
                        "attr": "test"
                    }
                }
            }
        }
    }
})
print(ref.get())
