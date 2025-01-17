import time
import datascrapingDelay as dsd

start_time = time.time()
dsd.getStationData()
while True:
    if time.time() - start_time >= dsd.scraping_interval_seconds:
        print(time.time() - start_time)
        start_time = time.time()
        dsd.getStationData()
