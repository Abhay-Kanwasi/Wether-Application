import django.contrib.admin
import datetime

import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    API_KEY = "6c95aea4394470358b051f4346769e68"

    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecasts_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    # Check if it is a get request or a post request
    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.get('city2', None) # Not required so if it's not then it will be fine
        
        # for city 1
        weather_data1, daily_forecastss1 = fetch_weather_and_forecasts(city1, API_KEY, current_weather_url, forecasts_url)

        # for city 2
        if city2:
            weather_data2, daily_forecastss2 = fetch_weather_and_forecasts(city2, API_KEY, current_weather_url, forecasts_url)
        else:
            weather_data2, daily_forecastss2 = None, None

        context = {
            "weather_data1" : weather_data1,
            "daily_forecasts1" : daily_forecastss1,
     
            "weather_data2" : weather_data2,
            "daily_forecasts2" : daily_forecastss2 
        }
        return render(request, "weather_app/index.html", context)

    else:
        # If it is a get request simply show the index.html
        return render(request, "weather_app/index.html")
    
def fetch_weather_and_forecasts(city, api_key, current_weather_url, forecasts_url):
    response = requests.get(current_weather_url.format(city, api_key)).json() #json so we treat it like a dictionary
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecasts_response = requests.get(forecasts_url.format(lat, lon, api_key)).json()

    # This data will be provided to html to render this is just the structure of the response
    weather_data = {
        "city" : city,
        "temperature" : round(response['main']['temp']-273.15,2),#273.15 because temp in kalvin
        "description" : response['weather'][0]['description'],
        "icon" : response['weather'][0]['icon']
    }

    daily_forecastss = []
    for daily_data in forecasts_response['daily'][:5]:
        daily_forecastss.append({
            "day" : datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp" : round(daily_data['temp']['min'] - 273.15, 2),
            "max_temp" : round(daily_data['temp']['max'] - 273.15, 2),
            "description" : daily_data['weather'][0]['description'],
            "icon" : daily_data['weather'][0]['icon']
        })
    return weather_data, daily_forecastss
