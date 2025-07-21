from backend.repositories.interfaces import IWeatherRepository
from backend.database.models import WeatherData, WeatherForecast
from backend.database.connection import AsyncSession
from sqlalchemy import select, desc, and_
from typing import Any, Dict, List
from datetime import datetime, date, timedelta
import logging

logger = logging.getLogger(__name__)

class PostgreSQLWeatherRepository(IWeatherRepository):
    """
    Implémentation PostgreSQL du repository météorologique.
    Utilise SQLAlchemy pour interagir avec la base de données.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_weather_by_region(self, region_name: str) -> Dict[str, Any]:
        """
        Récupère les données météorologiques actuelles pour une région depuis PostgreSQL
        
        Args:
            region_name: Le nom de la région
            
        Returns:
            Dictionnaire contenant les données météo actuelles
        """
        try:
            # Récupérer la donnée météo la plus récente pour la région (non-forecast)
            stmt = (select(WeatherData)
                   .where(and_(
                       WeatherData.region_name.ilike(f"%{region_name}%"),
                       WeatherData.is_forecast == False
                   ))
                   .order_by(desc(WeatherData.recorded_at))
                   .limit(1))
            
            result = await self.session.execute(stmt)
            weather_data = result.scalar_one_or_none()
            
            if weather_data:
                logger.info(f"Données météo trouvées pour {region_name}")
                return weather_data.to_dict()
            else:
                logger.warning(f"Aucune donnée météo trouvée pour: {region_name}")
                # Retourner des données par défaut si aucune donnée n'est trouvée
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
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des données météo pour {region_name}: {str(e)}")
            return {}
    
    async def get_weather_forecast(self, region_name: str, days: int) -> List[Dict[str, Any]]:
        """
        Récupère les prévisions météorologiques pour une région depuis PostgreSQL
        
        Args:
            region_name: Le nom de la région
            days: Nombre de jours de prévisions
            
        Returns:
            Liste des prévisions météorologiques
        """
        try:
            # Calculer la date limite pour les prévisions
            end_date = date.today() + timedelta(days=days)
            
            # Récupérer les prévisions pour la région
            stmt = (select(WeatherForecast)
                   .where(and_(
                       WeatherForecast.region_name.ilike(f"%{region_name}%"),
                       WeatherForecast.forecast_date <= end_date,
                       WeatherForecast.forecast_date >= date.today()
                   ))
                   .order_by(WeatherForecast.forecast_date)
                   .limit(days))
            
            result = await self.session.execute(stmt)
            forecasts = result.scalars().all()
            
            if forecasts:
                forecasts_list = [forecast.to_dict() for forecast in forecasts]
                logger.info(f"Prévisions trouvées pour {region_name}: {len(forecasts_list)} jours")
                return forecasts_list
            else:
                logger.warning(f"Aucune prévision trouvée pour: {region_name}")
                # Retourner des prévisions par défaut si aucune donnée n'est trouvée
                default_forecasts = []
                for i in range(min(days, 5)):  # Maximum 5 jours de prévisions par défaut
                    forecast_date = date.today() + timedelta(days=i+1)
                    default_forecasts.append({
                        "region_name": region_name,
                        "forecast_date": forecast_date.isoformat(),
                        "day": self._get_day_name(forecast_date),
                        "temperature": 22.0,
                        "condition": "Partly Cloudy",
                        "humidity": 60,
                        "pressure": 1013.25,
                        "wind_speed": 10.0,
                        "wind_direction": "NW",
                        "precipitation_probability": 20
                    })
                return default_forecasts
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des prévisions pour {region_name}: {str(e)}")
            return []
    
    def _get_day_name(self, forecast_date: date) -> str:
        """Retourne le nom du jour pour une date donnée"""
        days = {
            0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi",
            4: "Vendredi", 5: "Samedi", 6: "Dimanche"
        }
        return days.get(forecast_date.weekday(), "Inconnu")
    
    async def create_weather_data(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée une nouvelle entrée de données météo dans PostgreSQL
        
        Args:
            weather_data: Dictionnaire contenant les données météo
            
        Returns:
            Dictionnaire contenant les données météo créées
        """
        try:
            new_weather = WeatherData(
                region_name=weather_data.get("region_name"),
                temperature=weather_data.get("temperature"),
                condition=weather_data.get("condition"),
                humidity=weather_data.get("humidity"),
                pressure=weather_data.get("pressure"),
                wind_speed=weather_data.get("wind_speed"),
                wind_direction=weather_data.get("wind_direction"),
                is_forecast=weather_data.get("is_forecast", False),
                forecast_day=weather_data.get("forecast_day", 0)
            )
            
            self.session.add(new_weather)
            await self.session.commit()
            await self.session.refresh(new_weather)
            
            logger.info(f"Nouvelles données météo créées pour: {new_weather.region_name}")
            return new_weather.to_dict()
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Erreur lors de la création des données météo: {str(e)}")
            return {}
    
    async def create_weather_forecast(self, forecast_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée une nouvelle prévision météorologique dans PostgreSQL
        
        Args:
            forecast_data: Dictionnaire contenant les données de prévision
            
        Returns:
            Dictionnaire contenant la prévision créée
        """
        try:
            new_forecast = WeatherForecast(
                region_name=forecast_data.get("region_name"),
                forecast_date=forecast_data.get("forecast_date"),
                day_name=forecast_data.get("day_name"),
                temperature_min=forecast_data.get("temperature_min"),
                temperature_max=forecast_data.get("temperature_max"),
                temperature_avg=forecast_data.get("temperature_avg"),
                condition=forecast_data.get("condition"),
                humidity=forecast_data.get("humidity"),
                pressure=forecast_data.get("pressure"),
                wind_speed=forecast_data.get("wind_speed"),
                wind_direction=forecast_data.get("wind_direction"),
                precipitation_probability=forecast_data.get("precipitation_probability", 0)
            )
            
            self.session.add(new_forecast)
            await self.session.commit()
            await self.session.refresh(new_forecast)
            
            logger.info(f"Nouvelle prévision créée pour: {new_forecast.region_name}")
            return new_forecast.to_dict()
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Erreur lors de la création de la prévision: {str(e)}")
            return {}
    
    async def get_weather_history(self, region_name: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Récupère l'historique des données météo pour une région
        
        Args:
            region_name: Le nom de la région
            days: Nombre de jours d'historique (par défaut 7)
            
        Returns:
            Liste des données météo historiques
        """
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            stmt = (select(WeatherData)
                   .where(and_(
                       WeatherData.region_name.ilike(f"%{region_name}%"),
                       WeatherData.recorded_at >= start_date,
                       WeatherData.is_forecast == False
                   ))
                   .order_by(desc(WeatherData.recorded_at)))
            
            result = await self.session.execute(stmt)
            weather_history = result.scalars().all()
            
            history_list = [weather.to_dict() for weather in weather_history]
            logger.info(f"Historique météo récupéré pour {region_name}: {len(history_list)} entrées")
            
            return history_list
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'historique météo pour {region_name}: {str(e)}")
            return []
