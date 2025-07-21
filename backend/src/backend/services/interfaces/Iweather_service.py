from abc import ABC, abstractmethod
from typing import Dict, Any

from backend.services.schemas.region_resp_schema import RegionResponse
from backend.services.schemas.weather_resp_schema import WeatherResponse

class IWeatherService(ABC):
    @abstractmethod
    async def get_current_weather(self, region_name: str) -> RegionResponse:
        """Récupère la météo actuelle pour une région donnée"""
        pass

    @abstractmethod
    async def get_weather_forecast(self, region_name: str, days: int) -> WeatherResponse:
        """Récupère les prévisions météo pour une région donnée et un nombre de jours"""
        pass
