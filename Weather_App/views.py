import requests
import datetime

from django.shortcuts import render
from django.http import HttpResponse

# URL and API key for making API call
API_KEY = "4da3135aeca586f32bb18c5c27d81cdb"
Geocoding_API_URL = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit={}&appid={}"
Weather_API_URL = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric"
Forcast_API_URL = "api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"

# Create your views here.
def index(request):
    if request.method == "POST":

        # Get City from form
        city = request.POST["city"]
        if not city:
            return render(request, "weather/index.html")
        
        # Get city coordinate, if city doesn't exist lat and lon = 0
        lat, lon = get_geocoding_api_response(city, "1")

        # Get weather for that city
        weather = get_weather_api_response(lat, lon)

        # Convert UTC to datetime
        weather["dt"] = datetime.datetime.fromtimestamp(weather["dt"])

        context = {
            "weather": weather
        }

        return render(request, "weather/index.html", context)
    

    return render(request, "weather/index.html")


# Function to send api call for Geocoding API
def get_geocoding_api_response(city: str, limit: str):
    
    # Send Get request to Geocoding url and format response as a json object
    geocoding_api_respone = requests.get(Geocoding_API_URL.format(city, limit, API_KEY)).json()
    if not geocoding_api_respone:
        return 0, 0

    # Get latitude and longitude of the city location 
    lat, lon = geocoding_api_respone[0]["lat"], geocoding_api_respone[0]["lon"]
    
    return lat, lon

def get_weather_api_response(lat: int, lon: int):

    # Send the request
    weather_api_response = requests.get(Weather_API_URL.format(lat, lon, API_KEY)).json()

    return weather_api_response

