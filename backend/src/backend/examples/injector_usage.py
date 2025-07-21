"""
Guide pratique d'utilisation de l'injection de dépendances avec injector.
Ce fichier montre les différentes façons d'utiliser l'injector dans votre application.
"""

import asyncio
import logging
from typing import List

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_basic_usage():
    """
    Exemple d'utilisation basique de l'injector.
    Montre comment obtenir des instances de services.
    """
    logger.info("=== Exemple d'utilisation basique ===")
    
    try:
        # Importer les fonctions utilitaires
        from backend.di.container import get_region_service, get_weather_service
        
        # Obtenir des instances via l'injector
        region_service = get_region_service()
        weather_service = get_weather_service()
        
        logger.info(f"Service régions: {type(region_service).__name__}")
        logger.info(f"Service météo: {type(weather_service).__name__}")
        
        return region_service, weather_service
        
    except ImportError as e:
        logger.error(f"Erreur d'import: {e}")
        logger.info("Assurez-vous d'avoir installé injector: pip install injector")
        return None, None

async def example_service_usage():
    """
    Exemple d'utilisation des services obtenus via l'injector.
    """
    logger.info("=== Exemple d'utilisation des services ===")
    
    # Obtenir les services
    region_service, weather_service = example_basic_usage()
    
    if region_service and weather_service:
        try:
            # Test du service régions
            logger.info("Test du service régions...")
            region = await region_service.get_region_info(1)
            logger.info(f"Région récupérée: {region.name}")
            
            # Test du service météo
            logger.info("Test du service météo...")
            weather = await weather_service.get_current_weather("Paris")
            logger.info(f"Météo à {weather.region}: {weather.temperature}°C, {weather.condition}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'utilisation des services: {e}")
            return False
    
    return False

def example_manual_injector():
    """
    Exemple d'utilisation manuelle de l'injector.
    Montre comment créer et configurer l'injector manuellement.
    """
    logger.info("=== Exemple d'utilisation manuelle ===")
    
    try:
        from injector import Injector
        from backend.di.container import ApplicationModule
        from backend.services.interfaces.Iregion_info_service import IRegionInformationService
        
        # Créer un injector avec la configuration
        injector = Injector([ApplicationModule()])
        
        # Obtenir une instance via l'injector
        region_service = injector.get(IRegionInformationService)
        
        logger.info(f"Service créé manuellement: {type(region_service).__name__}")
        
        return injector
        
    except ImportError as e:
        logger.error(f"Erreur d'import: {e}")
        return None

def example_testing_configuration():
    """
    Exemple de configuration pour les tests.
    Montre comment utiliser l'injector avec des mocks pour les tests.
    """
    logger.info("=== Exemple de configuration pour tests ===")
    
    try:
        import os
        from backend.di.container import reset_injector, get_injector
        
        # Configurer l'environnement pour les tests
        os.environ["APP_ENV"] = "test"
        os.environ["USE_DATABASE"] = "false"
        
        # Réinitialiser l'injector pour prendre en compte la nouvelle config
        reset_injector()
        
        # Obtenir le nouvel injector configuré pour les tests
        test_injector = get_injector()
        
        from backend.services.interfaces.Iregion_info_service import IRegionInformationService
        region_service = test_injector.get(IRegionInformationService)
        
        logger.info(f"Service configuré pour les tests: {type(region_service).__name__}")
        
        # Remettre la configuration normale
        os.environ["APP_ENV"] = "development"
        os.environ["USE_DATABASE"] = "true"
        reset_injector()
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur de configuration test: {e}")
        return False

def show_dependency_graph():
    """
    Montre le graphe des dépendances configurées.
    """
    logger.info("=== Graphe des dépendances ===")
    
    try:
        from backend.di.container import get_injector
        
        injector = get_injector()
        
        # Informations sur les bindings
        logger.info("Bindings configurés:")
        logger.info("- IRegionRepository -> PostgreSQLRegionRepository ou RegionRepository (mock)")
        logger.info("- IWeatherRepository -> PostgreSQLWeatherRepository ou WeatherRepository (mock)")
        logger.info("- IRegionInformationService -> RegionInformationService")
        logger.info("- IWeatherService -> WeatherService")
        logger.info("- AsyncSession -> Session de base de données (singleton)")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage du graphe: {e}")
        return False

async def main():
    """Fonction principale pour exécuter tous les exemples"""
    logger.info("🚀 Exemples d'utilisation de l'injection de dépendances avec injector")
    logger.info("="*70)
    
    # Exemple basique
    example_basic_usage()
    
    # Exemple d'utilisation des services
    await example_service_usage()
    
    # Exemple manuel
    example_manual_injector()
    
    # Exemple configuration tests
    example_testing_configuration()
    
    # Graphe des dépendances
    show_dependency_graph()
    
    logger.info("="*70)
    logger.info("✅ Tous les exemples ont été exécutés")

if __name__ == "__main__":
    asyncio.run(main())
