from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time
import json
import csv
import difflib
import os.path

# Configure Firefox options
options = Options()
options.add_argument("--headless")  # Run Firefox in headless mode (optional)

# Set up the WebDriver (replace 'geckodriver_path' with the actual path to geckodriver)
#geckodriver_path = "/usr/bin/geckodriver"
# service = Service(geckodriver_path)

options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
service = Service(executable_path=r"D:\Programme\geckodriver\geckodriver.exe")
driver = webdriver.Firefox(service=service, options=options)

print("WebDriver Setup complete.")

districts = ["Lübeck", "Bad Schwartau", "Stockelsdorf", "Roggenhorst", "Moisling", "Krummesse", "Blankensee", "Herrnburg", "Selmsdorf", "Schlutup", "Kücknitz", "Travemünde", "Sereetz"]

stations_gtfs = {}
with open("gtfs/stops.csv", mode="r", newline="", encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        if row["location_type"] and [item for item in districts if item in row["stop_name"]]:
            stations_gtfs[row["stop_name"]] = {"coords": {}}
            coords = {"lat": None, "long": None}
            coords["lat"] = row["stop_lat"]
            coords["long"] = row["stop_lon"]
            coords["src"] = row["stop_name"]
            stations_gtfs[row["stop_name"]]["coords"] = coords

def compareStation(station):
    similarity_max = 0.0
    result = None
    for entry in stations_gtfs.keys():
        similarity = difflib.SequenceMatcher(None, station, entry).ratio()
        if similarity > similarity_max:
            similarity_max = similarity
            result = entry
    return stations_gtfs[result]

try:
    # Open the URL
    url = "https://www.swhl.de/mobil/fahrplanauskunft/haltestellen/"
    driver.get(url)

    # Allow the page to load
    for i in range(1, 6):
        time.sleep(1)
        print(f"Waited {i}/5 seconds.")

    # Find all elements with the class "stopName"
    stop_elements = driver.find_elements(By.CLASS_NAME, "StopName")


    station_json = {}
    for stop_element in stop_elements:
        station = stop_element.find_element(By.CLASS_NAME, "b-regular").text
        station_lines = stop_element.find_elements(By.CLASS_NAME, "StopDot")

        station_json[station] = {"lines": [], "coords": {}}
        station_line_arr = []

        for station_line in station_lines:
            station_line_arr.append(station_line.text)

        station_json[station]["lines"] = station_line_arr
        station_json[station]["coords"] = compareStation(station)["coords"]


    folder = "stationData"
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "station.json"), "w", encoding="utf-8") as json_file:
        json.dump(station_json, json_file, indent=4, ensure_ascii=False)

finally:
    # Close the WebDriver
    driver.quit()
