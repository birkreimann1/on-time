import requests
import time
from srv.srv_logging.logger import log

def check_request_limit(response, url):
    """Handles rate limits and retries or logs other unexpected responses."""
    
    while response.status_code in {429, 502, 503}:
        retry_after = int(response.headers.get("Retry-After", 5))
        log(f"Rate limit exceeded or server error. Retrying in {retry_after} seconds.", category='SWHL-API', priority='WARNING')
        time.sleep(retry_after)
        response = requests.get(url)

    if response.status_code == 200:
        return response
    elif response.status_code == 400:
        log("Bad Request (400): The request is invalid. Please check the URL or parameters.", category='SWHL-API', priority='ERROR')
    elif response.status_code == 401:
        log("Unauthorized (401): Authentication failed. Please check your credentials.", category='SWHL-API', priority='ERROR')
    elif response.status_code == 403:
        log("Forbidden (403): Permission denied. Please check your access rights.", category='SWHL-API', priority='ERROR')
    elif response.status_code == 404:
        log("Not Found (404): The resource was not found. Check the station ID or URL.", category='SWHL-API', priority='WARNING')
    elif response.status_code == 408:
        log("Request Timeout (408): The request took too long to process. Retrying.", category='SWHL-API', priority='WARNING')
    elif 500 <= response.status_code < 600:
        log(f"Server error ({response.status_code}): Something went wrong on the server. Retrying.", category='SWHL-API', priority='WARNING')
    else:
        log(f"Unexpected status code: {response.status_code}. Response: {response.text}", category='SWHL-API', priority='WARNING')
    
    return None

def fetch_station_data(station_id):
    """Fetch station data from the API and handle errors."""
    url = f"https://netzplan.swhl.de/api/v1/stationboards/hafas/{station_id}?v=0&limit=300"
    response = requests.get(url)

    response = check_request_limit(response, url)
    
    if response is None:
        log(f"Failed to fetch data for station {station_id}. Skipping.", category='SWHL-API', priority='WARNING')
        return None

    return response.json()
