import time
import datascrapingDelay as dsd

timestamps = [60 * i for i in range(1, dsd.scraping_interval_minutes)]

start_time = time.time()
dsd.getStationData()
print(f'[SYSTEM] Loop finished in {round(time.time() - start_time, 2)} seconds.')
while True:
    if time.time() - start_time >= dsd.scraping_interval_seconds:
        print(f'[SYSTEM] Time since start of last loop: {round(time.time() - start_time, 2)} seconds, starting next loop.')
        start_time = time.time()
        dsd.getStationData()
        print(f'[SYSTEM] Loop finished in {round(time.time() - start_time, 2)} seconds.')
    if int(time.time() - start_time) in timestamps:
        print(f'[SYSTEM] Time until next loop: {dsd.scraping_interval_seconds - int(time.time() - start_time)}.0 seconds.')
    time.sleep(1)
