import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def analyseWMOCode(code):
    if code in [0, 1]:
        return "clear"
    elif code in [2, 3]:
        return "clouds"
    elif code in [45, 48]:
        return "fog"
    elif code in [51, 53, 55]:
        return "rain"
    elif code in [56, 57]:
        return "rain"  # Freezing drizzle is considered rain
    elif code in [61, 63, 65]:
        return "rain"
    elif code in [66, 67]:
        return "rain"  # Freezing rain is considered rain
    elif code in [71, 73, 75]:
        return "snow"
    elif code == 77:
        return "snow"
    elif code in [80, 81, 82]:
        return "rain"
    elif code in [85, 86]:
        return "snow"
    elif code in [95, 96, 99]:
        return "thunderstorm"
    else:
        return "unknown"
    
def analyseTrafficTime(current_time, timezone='CET'):
    date = pd.to_datetime(current_time, unit='s', utc=True).tz_convert(timezone)
    
    if date.dayofweek < 5:
        if (date.hour >= 6 and date.hour < 9) or (date.hour >= 16 and date.hour < 19):
            return "work"
        else:
            return "offwork"
    else:
        if (date.hour >= 10 and date.hour < 20):
            return "free"
        else:
            return "offwork"

def analyseTemp(temp):
    if temp < 0:
        return "freezing"
    elif 1 <= temp <= 10:
        return "cool"
    elif 11 <= temp <= 20:
        return "mild"
    elif 21 <= temp <= 30:
        return "warm"
    elif temp > 30:
        return "hot"

def getDataByCoords(lat, long):

	env_data = {"weather": [], "traffic": "", "light": [], "temp": []}
	weather = []
	traffic = []
	light = []
	temp = []

	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": lat,
		"longitude": long,
		"current": ["temperature_2m", "is_day", "weather_code", "wind_speed_10m"],
		"timeformat": "unixtime"
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	#print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    
	# Current values. The order of variables needs to be the same as requested.
	current = response.Current()
	current_time = current.Time()
	current_temperature_2m = current.Variables(0).Value()
	current_is_day = current.Variables(1).Value()
	current_weather_code = current.Variables(2).Value()
	current_wind_speed_10m = current.Variables(3).Value()

	# https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM
	weather.append(analyseWMOCode(current_weather_code))

	# https://www.rmets.org/metmatters/beaufort-wind-scale
	if current_wind_speed_10m > 50.0:
		weather.append("storm")
          
	light.append("day") if current_is_day else light.append("night")
	temp.append(analyseTemp(current_temperature_2m))
	traffic.append(analyseTrafficTime(current_time))

	env_data["weather"] = weather
	env_data["light"] = light
	env_data["temp"] = temp
	env_data["traffic"] = traffic

	return env_data
