import openmeteo_requests
import requests
import requests_cache
import pandas as pd
from retry_requests import retry
from urllib.request import urlopen
import json
  

class Weather:
     
     
     
        def get_weather(self, city):



                # Setup the Open-Meteo API client with cache and retry on error
                cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
                retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
                openmeteo = openmeteo_requests.Client(session = retry_session)
                
                
                # Take city_name sent from assistente.py as an arg and plug it into the geocoding API.
                # Use geocoding API to grab the coordinates of a place so it can be plugged into the weather forecast params.
                
                geocode_arg = "+".join(city)
                url = f"https://geocoding-api.open-meteo.com/v1/search?name={geocode_arg}&count=1&language=en&format=json"
                location_response = urlopen(url)
                location_data = json.loads(location_response.read())
                latitude = location_data['results'][0]['latitude']
                longitude= location_data['results'][0]['longitude']
                coordinates = [latitude, longitude]
          

                # Make sure all required weather variables are listed here
                # The order of variables in hourly or daily is important to assign them correctly below
                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                        "latitude": coordinates[0],
                        "longitude": coordinates[1],
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
                print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
                print(f"Elevation: {response.Elevation()} m asl")
                

                # Current values. The order of variables needs to be the same as requested.
                current = response.Current()
                current_temperature_2m = current.Variables(0).Value()
                current_apparent_temperature = current.Variables(1).Value()
                current_precipitation = current.Variables(2).Value()
                current_weather_code = current.Variables(3).Value()
                current_weather_code = int(current_weather_code)
                
                
                new_weather_code = self.sort_weather_codes(current_weather_code)
                
                
                print(f"Current temperature_2m: {round(current_temperature_2m, 2)}")
                print(f"Current apparent_temperature: {round(current_apparent_temperature, 2)} fahrenheit.")
                print(f"Current precipitation: {round(current_precipitation, 2)} inches.")
                print(new_weather_code)

        
        def sort_weather_codes(self, current_weather_code):
                
                # Returns a description of the weather code.
                
                
                if current_weather_code == 0:
                    new_weather_code = "Clear"
                    return new_weather_code
                elif current_weather_code in (1, 2, 3):
                        new_weather_code = "Partly Cloudy"
                        return new_weather_code
                elif current_weather_code in (45, 48):
                        new_weather_code = "Fog"
                        return new_weather_code
                elif current_weather_code in (51, 53, 55):
                        new_weather_code = "Light Rain"
                        return new_weather_code
                elif current_weather_code in (61, 63, 65, 66, 67, 80, 81, 82):
                       new_weather_code = "Rain"
                       return new_weather_code
                elif current_weather_code in (71, 73, 75, 77, 85, 86):
                        new_weather_code = "Snow"
                        return new_weather_code
                elif current_weather_code == 95:
                        new_weather_code = "Thunderstorm"
                        return new_weather_code
                elif current_weather_code in (96, 99):
                        new_weather_code = "Hail"
                        return new_weather_code
                else:
                        print(f"Unknown weather code {current_weather_code}")
         