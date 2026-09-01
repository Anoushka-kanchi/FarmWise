import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_coordinates(city):
    geocoding_url = "https://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city,
        "limit": 1,
        "appid": API_KEY
    }

    response = requests.get(
    geocoding_url,
    params=params,
    timeout=10
    )

    if response.status_code != 200:
        error_message = response.json().get("message", "Geocoding API error")
        return {"error": error_message}

    data = response.json()

    if not data:
        return {"error": "city not found"}

    return {
        "city": data[0]["name"],
        "country": data[0].get("country"),
        "latitude": data[0]["lat"],
        "longitude": data[0]["lon"]
    }

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        error_message = response.json().get("message", "Weather API error")
        return {"error": error_message}

    data = response.json()

    weather = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "clouds": data["clouds"]["all"],
        "description": data["weather"][0]["description"],
        "sunrise": data["sys"]["sunrise"],
        "sunset": data["sys"]["sunset"]
    }

    return weather

def get_forecast(latitude, longitude):
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(forecast_url, params=params)

    if response.status_code != 200:
        error_message = response.json().get("message", "Forecast API error")
        return {"error": error_message}

    return response.json()

def format_forecast(forecast_data):
    if "error" in forecast_data:
        return forecast_data

    formatted = []

    for item in forecast_data["list"]:
        formatted.append({
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "wind_speed": item["wind"]["speed"],
            "description": item["weather"][0]["description"],
            "rain_probability": item.get("pop", 0) * 100
        })

    return formatted
def get_weather_data(city):
    location = get_coordinates(city)

    if "error" in location:
        return location

    current_weather = get_weather(city)

    if "error" in current_weather:
        return current_weather

    forecast_data = get_forecast(
        location["latitude"],
        location["longitude"]
    )

    forecast = format_forecast(forecast_data)

    if "error" in forecast:
        return forecast

    return {
        "location": location,
        "current": current_weather,
        "forecast": forecast
    }

if __name__ == "__main__":
    data = get_weather_data("Bangalore")
    print(data)