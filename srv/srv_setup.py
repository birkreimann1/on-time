from firebase_admin import db
from srv.srv_firebase.firebase_handler import initialize_firebase, firebase_ref
import srv.srv_json.json_handler as json_handler
from srv.config import ENV_DATA_PATH, DATA_BY_ENV_PATH, STATION_DATA_PATH
from srv.srv_logging.logger import log

# Uses templates for bus and enviroment data to create a blank database object
def create_setup_json(station_data, env_data_template, data_by_env_template):
    """Test"""
    setup_json = {}
    for id, station in station_data.items():
        setup_json[id] = {
            "lines": {line: data_by_env_template for line in station["lines"]},
            "env_data": env_data_template
        }
    return setup_json

def setup_database():
    """Test"""
    initialize_firebase()
    log("Firebase initialised", category="Server", priority="INFO")
    
    # Load static station data and database templates
    station_data = json_handler.load_json(STATION_DATA_PATH)
    data_by_env_template = json_handler.load_json(DATA_BY_ENV_PATH)
    env_data_template = json_handler.load_json(ENV_DATA_PATH)
    
    # Create blank database object
    setup_json = create_setup_json(station_data, env_data_template, data_by_env_template)
    log("Empty station object created", category="Server", priority="INFO")
    
    # Overwrite database branch with blank slate
    ref = db.reference(firebase_ref)
    ref.set(setup_json)
    log("Firebase database set up", category="Server", priority="INFO")

if __name__ == "__main__":
    setup_database()