import time
from datascrapingDelay import getStationData

scraping_interval_minutes = 20
scraping_interval_seconds = 60*scraping_interval_minutes

start_time = time.time()
getStationData()
while True:
    if time.time() - start_time >= scraping_interval_seconds:
        print(time.time() - start_time)
        start_time = time.time()
        getStationData()
