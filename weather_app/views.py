import datetime
from pathlib import Path
import requests
from django.shortcuts import render
import json

# Create your views here.
path_to_api_key = Path(__file__).resolve().parent.parent / "API_KEY"


def index(request):
    API_KEY = open(path_to_api_key, "r").read()
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}/next7days?unitGroup=metric&include=days&key={}&contentType=json"
    if request.method == "POST":
        city = request.POST["city"]
        # city2 = request.POST.get('city2', None)
        daily_weather1 = get_weather(city, API_KEY, url)

        # if city2:
        #     daily_weather2 = get_weather(city2, API_KEY, url)
        # else:
        #     daily_weather2 = None

        context = {
            "daily_weather1": daily_weather1,
            # "daily_weather2": daily_weather2,
        }
        return render(request, "weather_app/index.html", context)

    else:
        return render(request, "weather_app/index.html")


def get_weather(city, api_key, url):
    response = requests.request("GET", url.format(city, api_key)).json()
    # response = requests.get(url.format(city, api_key)
    # response = open('data.json', 'r').read()
    # response = json.loads(response)
    daily_weather = []
    for i in range(0, 7):
        date = response['days'][i]['datetime']
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        date = date_obj.strftime('%d-%m-%Y')
        daily_weather.append({
            "city": response['resolvedAddress'].split(',')[0],
            "temp_max": response['days'][i]['tempmax'],
            "temp_min": response['days'][i]['tempmin'],
            "temp": response['days'][i]['temp'],
            "description": response['days'][i]['conditions'],
            "icon": response['days'][i]['icon'],
            "date": date,
            "day": date_obj.strftime('%A'),
        })
    return daily_weather
