### scraper/weather_scraper.py
import requests
import json

def get_weather_data(location):
    url = f"https://api.weatherapi.com/v1/forecast.json?key=YOUR_API_KEY&q={location}&days=3"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Weather API failed"}
