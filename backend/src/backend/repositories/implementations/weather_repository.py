from backend.repositories.interfaces import IWeatherRepository
from typing import Any, Dict, List
from datetime import datetime, date, timedelta
import logging

logger = logging.getLogger(__name__)

class WeatherRepository(IWeatherRepository):
    """
    Implémentation mock du repository météorologique.
    Utilise des données fictives pour les tests et le développement.
    """
    
    def __init__(self):
        # Données météo fictives pour le développement/test
        self._weather_data = {
            "Paris": {
                "region_name": "Paris",
                "temperature": 22.5,
                "condition": "Partly Cloudy",
                "humidity": 65,
                "pressure": 1013.25,
                "wind_speed": 15.2,
                "wind_direction": "NW",
                "recorded_at": datetime.now().isoformat()
            },
            "Lyon": {
                "region_name": "Lyon",
                "temperature": 25.1,
                "condition": "Sunny",
                "humidity": 58,
                "pressure": 1015.80,
                "wind_speed": 8.7,
                "wind_direction": "S",
                "recorded_at": datetime.now().isoformat()
            },
            "Marseille": {
                "region_name": "Marseille",
                "temperature": 28.3,
                "condition": "Sunny",
                "humidity": 52,
                "pressure": 1016.90,
                "wind_speed": 12.3,
                "wind_direction": "SE",
                "recorded_at": datetime.now().isoformat()
            }
        }

    async def get_weather_by_region(self, region_name: str) -> Dict[str, Any]:
        """Récupère les données météo pour une région (version mock)"""
        logger.info(f"Mock: Récupération des données météo pour {region_name}")
        
        # Recherche case-insensitive
        for key, weather in self._weather_data.items():
            if key.lower() in region_name.lower() or region_name.lower() in key.lower():
                return weather
        
        # Données par défaut si la région n'est pas trouvée
        return {
            "region_name": region_name,
            "temperature": 20.0,
            "condition": "Unknown",
            "humidity": 50,
            "pressure": 1013.25,
            "wind_speed": 0.0,
            "wind_direction": "N",
            "recorded_at": datetime.now().isoformat()
        }

    async def get_weather_forecast(self, region_name: str, days: int) -> List[Dict[str, Any]]:
        """Récupère les prévisions météo pour une région (version mock)"""
        logger.info(f"Mock: Récupération des prévisions pour {region_name} sur {days} jours")
        
        forecasts = []
        base_temp = 22.0
        conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Stormy"]
        
        for i in range(min(days, 5)):  # Maximum 5 jours
            forecast_date = date.today() + timedelta(days=i+1)
            day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            
            forecasts.append({
                "region_name": region_name,
                "forecast_date": forecast_date.isoformat(),
                "day": day_names[forecast_date.weekday()],
                "temperature": base_temp + (i * 2) - 1,  # Variation de température
                "condition": conditions[i % len(conditions)],
                "humidity": 60 + (i * 5),
                "pressure": 1013.0 + (i * 2),
                "wind_speed": 10.0 + (i * 2),
                "wind_direction": ["N", "NE", "E", "SE", "S"][i % 5],
                "precipitation_probability": [10, 20, 60, 80, 30][i % 5]
            })
        
        return forecasts
    
    async def create_weather_data(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée une nouvelle entrée de données météo (version mock)"""
        logger.info(f"Mock: Création de données météo pour {weather_data.get('region_name')}")
        
        # Dans la version mock, on simule juste la création
        created_data = weather_data.copy()
        created_data["id"] = len(self._weather_data) + 1
        created_data["recorded_at"] = datetime.now().isoformat()
        
        return created_data
    
    async def create_weather_forecast(self, forecast_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée une nouvelle prévision météorologique (version mock)"""
        logger.info(f"Mock: Création de prévision pour {forecast_data.get('region_name')}")
        
        # Dans la version mock, on simule juste la création
        created_forecast = forecast_data.copy()
        created_forecast["id"] = 100 + len(self._weather_data)
        created_forecast["created_at"] = datetime.now().isoformat()
        
        return created_forecast
    
    async def get_weather_history(self, region_name: str, days: int = 7) -> List[Dict[str, Any]]:
        """Récupère l'historique météo pour une région (version mock)"""
        logger.info(f"Mock: Récupération de l'historique météo pour {region_name} sur {days} jours")
        
        history = []
        base_temp = 20.0
        
        for i in range(days):
            history_date = datetime.now() - timedelta(days=i)
            history.append({
                "region_name": region_name,
                "temperature": base_temp + (i % 10) - 5,  # Variation historique
                "condition": ["Sunny", "Cloudy", "Rainy"][i % 3],
                "humidity": 50 + (i % 30),
                "pressure": 1010.0 + (i % 20),
                "wind_speed": 5.0 + (i % 15),
                "wind_direction": ["N", "S", "E", "W"][i % 4],
                "recorded_at": history_date.isoformat(),
                "is_forecast": False
            })
        
        return history
