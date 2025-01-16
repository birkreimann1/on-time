import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 52.52,
	"longitude": 13.41,
	"current": ["temperature_2m", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "wind_speed_10m", "wind_gusts_10m"],
	"hourly": ["is_day", "sunshine_duration", "freezing_level_height"],
	"timeformat": "unixtime"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_is_day = current.Variables(1).Value()
current_precipitation = current.Variables(2).Value()
current_rain = current.Variables(3).Value()
current_showers = current.Variables(4).Value()
current_snowfall = current.Variables(5).Value()
current_weather_code = current.Variables(6).Value()
current_cloud_cover = current.Variables(7).Value()
current_wind_speed_10m = current.Variables(8).Value()
current_wind_gusts_10m = current.Variables(9).Value()

print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current is_day {current_is_day}")
print(f"Current precipitation {current_precipitation}")
print(f"Current rain {current_rain}")
print(f"Current showers {current_showers}")
print(f"Current snowfall {current_snowfall}")
print(f"Current weather_code {current_weather_code}")
print(f"Current cloud_cover {current_cloud_cover}")
print(f"Current wind_speed_10m {current_wind_speed_10m}")
print(f"Current wind_gusts_10m {current_wind_gusts_10m}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_is_day = hourly.Variables(0).ValuesAsNumpy()
hourly_sunshine_duration = hourly.Variables(1).ValuesAsNumpy()
hourly_freezing_level_height = hourly.Variables(2).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["is_day"] = hourly_is_day
hourly_data["sunshine_duration"] = hourly_sunshine_duration
hourly_data["freezing_level_height"] = hourly_freezing_level_height

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)
