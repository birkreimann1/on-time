from .data_processor import process_transit_data
from srv.config import SCRAPING_INTERVAL_SECONDS, BUS_LINES, STATION_DATA_PATH
from .data_scraper import fetch_station_data
from srv.srv_json.json_handler import load_json
from srv.srv_weatherdata import fetch_weather_data as weather
from srv.srv_logging.logger import log

def get_station_data():
    """Load station data from JSON and process each station"""
    station_data = load_json(STATION_DATA_PATH)

    for station_nr, (station_id, station) in enumerate(station_data.items(), 1):
        process_station_data(station_id, station)
        log(f'[{station_nr}/{len(station_data)}] Parsed station {station["name"]} at ID {station_id}', category='DATA_HANDLER', priority='INFO')


def process_station_data(station_id, station):
    """Process data for a single station"""
    coords = station["coords"]
    current_env_data = weather.getDataByCoords(float(coords["lat"]), float(coords["long"]))
    station_data = fetch_station_data(station_id)
    process_transit_data(station_data, station_id, current_env_data, BUS_LINES, SCRAPING_INTERVAL_SECONDS)

if __name__ == "__main__":
    get_station_data()
