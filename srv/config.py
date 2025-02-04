import os

# Configuration Paths
STATION_DATA_PATH = os.path.join("datascraping", "station_data", "station_ids.json")
DATA_BY_ENV_PATH = os.path.join("json_templates", "data_by_env.json")
ENV_DATA_PATH = os.path.join("json_templates", "env_data.json")

BUS_LINES = {
    str(i)
    for i in [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 21, 24, 25, 26, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 50
    ]
}

SCRAPING_INTERVAL_MINUTES = 15
SCRAPING_INTERVAL_SECONDS = SCRAPING_INTERVAL_MINUTES * 60