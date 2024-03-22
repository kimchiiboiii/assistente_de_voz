import openmeteo_requests
import requests
import requests_cache
import pandas as pd
from retry_requests import retry
from urllib.request import urlopen
import json


# class Weather:
#     def get_weather(self, location):
    
        # # Setup the Open-Meteo API client with cache and retry on error
        # cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        # retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        # openmeteo = openmeteo_requests.Client(session = retry_session)

        # # Make sure all required weather variables are listed here
        # # The order of variables in hourly or daily is important to assign them correctly below
        # url = "https://api.open-meteo.com/v1/forecast"
        # params = {
        #     "latitude": 25.7743,
        #     "longitude": -80.1937,
        #     "current": ["temperature_2m", "apparent_temperature", "precipitation", "weather_code"],
        #     "timezone": "America/New_York"
        # }
        # responses = openmeteo.weather_api(url, params=params)

        # # Process first location. Add a for-loop for multiple locations or weather models
        # response = responses[0]
        # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        # print(f"Elevation {response.Elevation()} m asl")
        # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # # Current values. The order of variables needs to be the same as requested.
        # current = response.Current()
        # current_temperature_2m = current.Variables(0).Value()
        # current_apparent_temperature = current.Variables(1).Value()
        # current_precipitation = current.Variables(2).Value()
        # current_weather_code = current.Variables(3).Value()

        # print(f"Current time {current.Time()}")
        # print(f"Current temperature_2m {current_temperature_2m}")
        # print(f"Current apparent_temperature {current_apparent_temperature}")
        # print(f"Current precipitation {current_precipitation}")
        # print(f"Current weather_code {current_weather_code}")





# replace name= with a variable that has the user-inputted location.
location_url = "https://geocoding-api.open-meteo.com/v1/search?name=Miami&count=1&language=en&format=json"

location_response = urlopen(location_url)
location_data = json.loads(location_response.read())

print(location_data)


# I have the json file read now I just need to extract the latitude and longitude from it








# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 25.7743,
	"longitude": -80.1937,
	"current": ["temperature_2m", "apparent_temperature", "precipitation", "weather_code"],
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch",
	"timeformat": "unixtime",
	"timezone": "America/New_York"
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
current_apparent_temperature = current.Variables(1).Value()
current_precipitation = current.Variables(2).Value()
current_weather_code = current.Variables(3).Value()

print(f"Current time {current.Time()}")
print(f"Current temperature_2m {round(current_temperature_2m, 2)}")
print(f"Current apparent_temperature {round(current_apparent_temperature, 2)}")
print(f"Current precipitation {round(current_precipitation, 2)}")
print(f"Current weather_code {current_weather_code}")
