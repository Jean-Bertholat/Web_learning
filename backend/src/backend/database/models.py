from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, CheckConstraint
from sqlalchemy.dialects.mysql import DECIMAL as Decimal
from sqlalchemy.sql import func
from backend.database.connection import Base

class Region(Base):
    """Modèle pour la table des régions"""
    
    __tablename__ = "regions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    nb_habitants = Column(Integer, nullable=False, default=0)
    language = Column(String(50), nullable=False, default="français")
    country = Column(String(100), nullable=False, default="France")
    latitude = Column(Decimal(9, 6), nullable=True)
    longitude = Column(Decimal(9, 6), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "nb_habitants": self.nb_habitants,
            "language": self.language,
            "country": self.country,
            "latitude": float(self.latitude) if self.latitude else None,
            "longitude": float(self.longitude) if self.longitude else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class WeatherData(Base):
    """Modèle pour les données météorologiques actuelles"""
    
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String(100), nullable=False, index=True)
    temperature = Column(Decimal(5, 2), nullable=False)
    condition = Column(String(100), nullable=False)
    humidity = Column(Integer, nullable=False)
    pressure = Column(Decimal(6, 2), nullable=True)
    wind_speed = Column(Decimal(5, 2), nullable=True)
    wind_direction = Column(String(3), nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    is_forecast = Column(Boolean, default=False, nullable=False)
    forecast_day = Column(Integer, default=0, nullable=False)
    
    __table_args__ = (
        CheckConstraint('humidity >= 0 AND humidity <= 100', name='check_humidity_range'),
    )
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            "id": self.id,
            "region_name": self.region_name,
            "temperature": float(self.temperature),
            "condition": self.condition,
            "humidity": self.humidity,
            "pressure": float(self.pressure) if self.pressure else None,
            "wind_speed": float(self.wind_speed) if self.wind_speed else None,
            "wind_direction": self.wind_direction,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None,
            "is_forecast": self.is_forecast,
            "forecast_day": self.forecast_day
        }

class WeatherForecast(Base):
    """Modèle pour les prévisions météorologiques"""
    
    __tablename__ = "weather_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String(100), nullable=False, index=True)
    forecast_date = Column(Date, nullable=False, index=True)
    day_name = Column(String(20), nullable=False)
    temperature_min = Column(Decimal(5, 2), nullable=True)
    temperature_max = Column(Decimal(5, 2), nullable=True)
    temperature_avg = Column(Decimal(5, 2), nullable=True)
    condition = Column(String(100), nullable=False)
    humidity = Column(Integer, nullable=False)
    pressure = Column(Decimal(6, 2), nullable=True)
    wind_speed = Column(Decimal(5, 2), nullable=True)
    wind_direction = Column(String(3), nullable=True)
    precipitation_probability = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        CheckConstraint('humidity >= 0 AND humidity <= 100', name='check_forecast_humidity_range'),
        CheckConstraint('precipitation_probability >= 0 AND precipitation_probability <= 100', name='check_precipitation_range'),
    )
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            "id": self.id,
            "region_name": self.region_name,
            "forecast_date": self.forecast_date.isoformat() if self.forecast_date else None,
            "day": self.day_name,
            "temperature_min": float(self.temperature_min) if self.temperature_min else None,
            "temperature_max": float(self.temperature_max) if self.temperature_max else None,
            "temperature": float(self.temperature_avg) if self.temperature_avg else None,
            "condition": self.condition,
            "humidity": self.humidity,
            "pressure": float(self.pressure) if self.pressure else None,
            "wind_speed": float(self.wind_speed) if self.wind_speed else None,
            "wind_direction": self.wind_direction,
            "precipitation_probability": self.precipitation_probability,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
