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
import requests

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
    stations = []
    for stop_element in stop_elements:
        station = stop_element.find_element(By.CLASS_NAME, "b-regular").text
        station_lines = stop_element.find_elements(By.CLASS_NAME, "StopDot")
        stations.append(station)

        station_json[station] = {"id": "", "lines": [], "coords": {}}
        station_line_arr = []

        for station_line in station_lines:
            station_line_arr.append(station_line.text)

        station_json[station]["lines"] = station_line_arr
    
    for station in stations:
        url = f"https://swhl.vercel.app/api/stops?search={station}&luebeckOnly=true"
        response = requests.get(url)
        if response.status_code == 200:
            response_data = response.json()["data"]
            for entry in response_data:
                lat = float(entry["lat"])
                long = float(entry["lon"])
                if 10.55 < long < 10.95 and 53.75 < lat < 54 and station.lower().replace("straße", "str").replace(".", "") in entry["name"].lower().replace("straße", "str").replace(".", "") and entry.get("extId") is not None:
                    coords = {"lat": None, "long": None}
                    coords["lat"] = entry["lat"]
                    coords["long"] = entry["lon"]
                    station_json[station]["coords"] = coords
                    station_json[station]["id"] = entry["extId"]
                    break
        else:
            print(f"Failed to retrieve JSON. Status code: {response.status_code}")


    folder = "stationData"
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "station.json"), "w", encoding="utf-8") as json_file:
        json.dump(station_json, json_file, indent=4, ensure_ascii=False)

finally:
    # Close the WebDriver
    driver.quit()
