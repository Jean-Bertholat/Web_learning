from typing import Dict, Any
from backend.services.interfaces.Iweather_service import IWeatherService

from backend.services.schemas.weather_resp_schema import WeatherForecastResponse, WeatherResponse


class WeatherService(IWeatherService):
    async def get_current_weather(self, region_name: str) -> WeatherResponse:
        weather_data = {
            "region": region_name,
            "temperature": 22,
            "condition": "Ensoleillé",
            "humidity": 65
        }
        return WeatherResponse(**weather_data)


class WeatherService1(IWeatherService):
    async def get_current_weather(self, region_name: str) -> WeatherResponse:
        response = {
        "region": "le nom que j'ai choisit",
        "temperature": 1000,
        "condition": "ça va",
        "humidity": 20
        }
        return WeatherResponse(**response)
    
    async def get_weather_forecast(self, region_name, days) -> WeatherForecastResponse:
        response = {
            "region": region_name,
            "temperature": 0,
            "condition": "ça va dans les prochains jours",
            "humidity": 20,
            "day": days
        }
        return WeatherForecastResponse(**response)