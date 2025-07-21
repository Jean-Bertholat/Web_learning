from typing import Dict, Any, List
import logging
from injector import inject

from backend.services.interfaces.Iweather_service import IWeatherService
from backend.services.schemas.weather_resp_schema import WeatherResponse, WeatherForecastResponse
from backend.repositories.interfaces import IWeatherRepository

logger = logging.getLogger(__name__)

class WeatherService(IWeatherService):
    """
    Service météorologique utilisant l'injection de dépendances avec injector.
    Le repository approprié (PostgreSQL ou Mock) est injecté automatiquement.
    """
    
    @inject
    def __init__(self, weather_repository: IWeatherRepository):
        """
        Initialise le service avec injection de dépendances.
        
        Args:
            weather_repository: Repository météorologique (injecté automatiquement)
        """
        self.weather_repository = weather_repository
        logger.info(f"WeatherService initialisé avec {type(weather_repository).__name__}")
    
    async def get_current_weather(self, region_name: str) -> WeatherResponse:
        """
        Récupère les données météorologiques actuelles pour une région
        
        Args:
            region_name: Le nom de la région
            
        Returns:
            WeatherResponse contenant les données météo actuelles
        """
        try:
            logger.info(f"Récupération de la météo pour: {region_name}")
            
            weather_data = await self.weather_repository.get_weather_by_region(region_name)
            
            if not weather_data:
                logger.warning(f"Aucune donnée météo trouvée pour: {region_name}")
                # Données par défaut
                weather_data = {
                    "region": region_name,
                    "temperature": 20.0,
                    "condition": "Unknown",
                    "humidity": 50
                }
            else:
                # Adapter les clés si nécessaire
                weather_data = {
                    "region": weather_data.get("region_name", region_name),
                    "temperature": weather_data.get("temperature", 20.0),
                    "condition": weather_data.get("condition", "Unknown"),
                    "humidity": weather_data.get("humidity", 50)
                }
            
            return WeatherResponse(**weather_data)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la météo pour {region_name}: {str(e)}")
            # Retourner des données par défaut en cas d'erreur
            return WeatherResponse(
                region=region_name,
                temperature=20.0,
                condition="Erreur de récupération",
                humidity=50
            )
    
    async def get_weather_forecast(self, region_name: str, days: int) -> WeatherForecastResponse:
        """
        Récupère les prévisions météorologiques pour une région
        
        Args:
            region_name: Le nom de la région
            days: Nombre de jours de prévisions
            
        Returns:
            WeatherForecastResponse contenant les prévisions
        """
        try:
            logger.info(f"Récupération des prévisions pour: {region_name} sur {days} jours")
            
            forecasts = await self.weather_repository.get_weather_forecast(region_name, days)
            
            if not forecasts:
                logger.warning(f"Aucune prévision trouvée pour: {region_name}")
                # Prévision par défaut
                forecast_data = {
                    "region": region_name,
                    "temperature": 22.0,
                    "condition": "Partly Cloudy",
                    "humidity": 60,
                    "day": "Demain"
                }
            else:
                # Prendre la première prévision et adapter les clés
                first_forecast = forecasts[0]
                forecast_data = {
                    "region": first_forecast.get("region_name", region_name),
                    "temperature": first_forecast.get("temperature", 22.0),
                    "condition": first_forecast.get("condition", "Partly Cloudy"),
                    "humidity": first_forecast.get("humidity", 60),
                    "day": first_forecast.get("day", "Demain")
                }
            
            return WeatherForecastResponse(**forecast_data)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des prévisions pour {region_name}: {str(e)}")
            # Retourner des données par défaut en cas d'erreur
            return WeatherForecastResponse(
                region=region_name,
                temperature=22.0,
                condition="Erreur de récupération",
                humidity=60,
                day="Erreur"
            )

# Classes supplémentaires pour maintenir la compatibilité avec l'existant
class WeatherService1(WeatherService):
    """Alias pour maintenir la compatibilité"""
    pass
