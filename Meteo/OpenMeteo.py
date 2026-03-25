# Reference: https://open-meteo.com/en/docs
import requests

def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": 45.49068460938023,
    	"longitude": -73.58147714232855,
    	"current": ["temperature_2m", "relative_humidity_2m", "weather_code", "pressure_msl", "surface_pressure"],
    }
    results = requests.get(url, params=params)
    data = results.json()
    # print(data['current'])
    # print(json.dumps(data, indent=4))
    return data['current']
