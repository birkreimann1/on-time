import time
import os
import argparse
from srv.srv_logging.logger import log, set_global_log_level
from srv.srv_firebase.firebase_handler import initialize_firebase
from srv.config import STATION_DATA_PATH, SCRAPING_INTERVAL_SECONDS
from srv.srv_data.data_handler import get_station_data
from srv.srv_firebase.firebase_firestore import upload_station_data_to_firebase

def parse_args():
    """Test"""
    parser = argparse.ArgumentParser(description="Run the server with specific logging options.")
    parser.add_argument(
        '--loglevel',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help="Set the log level (default: INFO)"
    )
    return parser.parse_args()

def get_file_modification_time(file_path):
    """Test"""
    return os.path.getmtime(file_path)

def run_srv_loop():
    """Test"""
    args = parse_args()
    set_global_log_level(args.loglevel)
    log(f"Starting server loop with log level {args.loglevel}", category="Server", priority="INFO")
    
    initialize_firebase()
    
    start_time = time.time()
    last_modified_time = get_file_modification_time(STATION_DATA_PATH)
    initial_run = True

    while True:
        elapsed_time = int(time.time() - start_time)

        if elapsed_time >= SCRAPING_INTERVAL_SECONDS or initial_run:
            initial_run = False
            log(f'Time since start of last loop: {elapsed_time} seconds, starting next loop.', category='SERVER', priority='INFO')
            start_time = time.time()

            get_station_data()
            current_modified_time = get_file_modification_time(STATION_DATA_PATH)
            log(f'{current_modified_time}, {last_modified_time}')
            if current_modified_time > last_modified_time:
                log(f"Detected change in {STATION_DATA_PATH}. Uploading to Firebase...", category='SERVER', priority='INFO')
                upload_station_data_to_firebase(STATION_DATA_PATH)
                last_modified_time = current_modified_time

            log(f'Loop finished in {round(time.time() - start_time, 2)} seconds.', category='SERVER', priority='INFO')

        time.sleep(1)

if __name__ == "__main__":
    run_srv_loop()
