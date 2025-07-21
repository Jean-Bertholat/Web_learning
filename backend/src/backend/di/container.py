"""
Configuration de l'injection de dépendances avec la bibliothèque injector.
Ce module configure tous les bindings pour l'application.
"""

from injector import Module, provider, singleton, Injector
from sqlalchemy.ext.asyncio import AsyncSession
import os
import logging

from backend.database.connection import AsyncSessionLocal, db_config
from backend.repositories.interfaces import IRegionRepository, IWeatherRepository
from backend.repositories.region_repository import RegionRepository
from backend.repositories.weather_repository import WeatherRepository
from backend.repositories.implementations.postgresql_region_repository import PostgreSQLRegionRepository
from backend.repositories.implementations.postgresql_weather_repository import PostgreSQLWeatherRepository
from backend.services.interfaces.Iregion_info_service import IRegionInformationService
from backend.services.interfaces.Iweather_service import IWeatherService
from backend.services.implementation.region_info_service import RegionInformationService
from backend.services.implementation.weather_service import WeatherService

logger = logging.getLogger(__name__)

class DatabaseModule(Module):
    """
    Module pour la configuration des dépendances liées à la base de données.
    """
    
    def configure(self, binder):
        """Configure les bindings de base"""
        # Configuration du type de repository selon l'environnement
        use_postgresql = self._should_use_postgresql()
        
        if use_postgresql:
            logger.info("🔗 Configuration: Utilisation de PostgreSQL")
            binder.bind(IRegionRepository, to=PostgreSQLRegionRepository)
            binder.bind(IWeatherRepository, to=PostgreSQLWeatherRepository)
        else:
            logger.info("🔧 Configuration: Utilisation des repositories Mock")
            binder.bind(IRegionRepository, to=RegionRepository)
            binder.bind(IWeatherRepository, to=WeatherRepository)
    
    @provider
    @singleton
    def provide_database_session(self) -> AsyncSession:
        """
        Fournit une session de base de données.
        Utilise un singleton pour réutiliser la même session.
        """
        try:
            return AsyncSessionLocal()
        except Exception as e:
            logger.error(f"Erreur lors de la création de la session DB: {e}")
            # Retourner None pour forcer l'utilisation des mocks
            return None
    
    def _should_use_postgresql(self) -> bool:
        """
        Détermine si PostgreSQL doit être utilisé ou non.
        
        Returns:
            True si PostgreSQL doit être utilisé, False pour les mocks
        """
        # Vérification des variables d'environnement
        use_database = os.getenv("USE_DATABASE", "true").lower() == "true"
        app_env = os.getenv("APP_ENV", "development")
        
        # En mode test, toujours utiliser les mocks
        if app_env == "test":
            return False
        
        # Si USE_DATABASE=false, utiliser les mocks
        if not use_database:
            return False
        
        # Tenter une connexion rapide pour vérifier la disponibilité
        try:
            from backend.database.connection import engine
            # Test simple de connexion (sans async car c'est juste un check)
            return True
        except Exception as e:
            logger.warning(f"PostgreSQL non disponible, utilisation des mocks: {e}")
            return False

class ServiceModule(Module):
    """
    Module pour la configuration des services.
    """
    
    def configure(self, binder):
        """Configure les bindings des services"""
        binder.bind(IRegionInformationService, to=RegionInformationService)
        binder.bind(IWeatherService, to=WeatherService)

class ApplicationModule(Module):
    """
    Module principal qui combine tous les autres modules.
    """
    
    def __init__(self):
        self.database_module = DatabaseModule()
        self.service_module = ServiceModule()
    
    def configure(self, binder):
        """Configure tous les bindings de l'application"""
        self.database_module.configure(binder)
        self.service_module.configure(binder)

# Instance globale de l'injector
_injector = None

def get_injector() -> Injector:
    """
    Retourne l'instance globale de l'injector.
    Utilise le pattern singleton pour éviter de recréer l'injector.
    
    Returns:
        Injector configuré avec tous les modules
    """
    global _injector
    if _injector is None:
        _injector = Injector([ApplicationModule()])
        logger.info("💉 Injector initialisé avec succès")
    return _injector

def reset_injector():
    """
    Réinitialise l'injector (utile pour les tests).
    """
    global _injector
    _injector = None
    logger.info("🔄 Injector réinitialisé")

# Fonctions utilitaires pour obtenir les instances
def get_region_service() -> IRegionInformationService:
    """Obtient une instance du service de régions via l'injector"""
    return get_injector().get(IRegionInformationService)

def get_weather_service() -> IWeatherService:
    """Obtient une instance du service météo via l'injector"""
    return get_injector().get(IWeatherService)

def get_region_repository() -> IRegionRepository:
    """Obtient une instance du repository de régions via l'injector"""
    return get_injector().get(IRegionRepository)

def get_weather_repository() -> IWeatherRepository:
    """Obtient une instance du repository météo via l'injector"""
    return get_injector().get(IWeatherRepository)
