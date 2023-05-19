import requests

from django.shortcuts import render
from django.http import HttpResponse

# URL and API key for making API call
API_KEY = "4da3135aeca586f32bb18c5c27d81cdb"
Geocoding_API_URL = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit={}&appid={}"
Weather_API_URl = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"


# Create your views here.
def index(request):

    if request.method == "POST":

        # Get City from form
        city = request.POST.get("city")

        # Get city coordinate
        lat, lon = get_geocoding_api_response(city, "1")

        # Get weather for that city
        weather_response = get_weather_api_response(lat, lon)

        return render(request, "weather/index.html", weather_response)
        

    return render(request, "weather/index.html")


# Function to send api call for Geocoding API
def get_geocoding_api_response(city: str, limit: str):
    
    # Send Get request to Geocoding url and format response as a json object
    geocoding_api_respone = requests.get(Geocoding_API_URL.format(city, limit, API_KEY)).json()

    print(geocoding_api_respone)

    # Get latitude and longitude of the city location 
    lat, lon = geocoding_api_respone[0]["lat"], geocoding_api_respone[0]["lon"]
    
    return lat, lon

def get_weather_api_response(lat: int, lon: int):

    # Send the request
    weather_api_response = requests.get(Weather_API_URl.format(lat, lon, API_KEY)).json()

    print(weather_api_response)

    return weather_api_response

