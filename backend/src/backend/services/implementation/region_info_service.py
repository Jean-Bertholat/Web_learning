from typing import Dict, Any
import logging
from injector import inject

from backend.services.schemas.region_resp_schema import RegionResponse
from backend.services.interfaces.Iregion_info_service import IRegionInformationService
from backend.repositories.interfaces import IRegionRepository

logger = logging.getLogger(__name__)

class RegionInformationService(IRegionInformationService):
    """
    Service d'information des régions utilisant l'injection de dépendances avec injector.
    Le repository approprié (PostgreSQL ou Mock) est injecté automatiquement.
    """
    
    @inject
    def __init__(self, region_repository: IRegionRepository):
        """
        Initialise le service avec injection de dépendances.
        
        Args:
            region_repository: Repository des régions (injecté automatiquement)
        """
        self.region_repository = region_repository
        logger.info(f"RegionInformationService initialisé avec {type(region_repository).__name__}")
    
    async def get_region_info_by_id(self, region_id: int) -> RegionResponse:
        """
        Récupère les informations d'une région par son ID
        
        Args:
            region_id: L'ID de la région à récupérer
            
        Returns:
            RegionResponse contenant les informations de la région
        """
        try:
            logger.info(f"Récupération des informations pour la région ID: {region_id}")
            
            # Utilisation du repository injecté
            region_data = await self.region_repository.get_region_by_id(region_id)

            if not region_data:
                logger.warning(f"Aucune région trouvée avec l'ID: {region_id}")
                # Retourner des données par défaut si aucune région n'est trouvée
                region_data = {
                    "id": region_id,
                    "name": "Région inconnue",
                    "nb_habitants": 0,
                    "language": "français"
                }
            
            return RegionResponse(**region_data)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la région {region_id}: {str(e)}")
            # Retourner des données par défaut en cas d'erreur
            return RegionResponse(
                id=region_id,
                name="Erreur de récupération",
                nb_habitants=0,
                language="français"
            )
    
    async def get_all_regions(self) -> list[RegionResponse]:
        """
        Récupère toutes les régions disponibles
        
        Returns:
            Liste de RegionResponse contenant toutes les régions
        """
        try:
            logger.info("Récupération de toutes les régions")

            regions_data = await self.region_repository.get_all_regions()

            return [RegionResponse(**region_data) for region_data in regions_data]
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de toutes les régions: {str(e)}")
            return []
    
    async def create_region(self, region_data: Dict[str, Any]) -> RegionResponse:
        """
        Crée une nouvelle région
        
        Args:
            region_data: Données de la région à créer
            
        Returns:
            RegionResponse de la région créée
        """
        try:
            logger.info(f"Création d'une nouvelle région: {region_data.get('name')}")
            
            created_region = await self.region_repository.create_region(region_data)
            
            if not created_region:
                raise Exception("Échec de la création de la région")
            
            return RegionResponse(**created_region)
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la région: {str(e)}")
            raise e