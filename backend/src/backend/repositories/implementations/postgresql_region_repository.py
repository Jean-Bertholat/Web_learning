from backend.repositories.interfaces import IRegionRepository
from backend.database.models import Region
from backend.database.connection import AsyncSession
from sqlalchemy import select
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

class PostgreSQLRegionRepository(IRegionRepository):
    """
    Implémentation PostgreSQL du repository des régions.
    Utilise SQLAlchemy pour interagir avec la base de données.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_region_info_by_id(self, region_id: int) -> Dict[str, Any]:
        """
        Récupère une région par son ID depuis PostgreSQL
        
        Args:
            region_id: L'ID de la région à récupérer
            
        Returns:
            Dictionnaire contenant les informations de la région ou dictionnaire vide si non trouvée
        """
        try:
            # Création de la requête SQL avec SQLAlchemy
            stmt = select(Region).where(Region.id == region_id)
            result = await self.session.execute(stmt)
            region = result.scalar_one_or_none()
            
            if region:
                logger.info(f"Région trouvée: {region.name} (ID: {region_id})")
                return region.to_dict()
            else:
                logger.warning(f"Aucune région trouvée avec l'ID: {region_id}")
                return {}
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la région {region_id}: {str(e)}")
            return {}
    
    async def get_all_regions(self) -> List[Dict[str, Any]]:
        """
        Récupère toutes les régions depuis PostgreSQL
        
        Returns:
            Liste des dictionnaires contenant les informations de toutes les régions
        """
        try:
            # Requête pour récupérer toutes les régions, triées par nom
            stmt = select(Region).order_by(Region.name)
            result = await self.session.execute(stmt)
            regions = result.scalars().all()
            
            regions_list = [region.to_dict() for region in regions]
            logger.info(f"Récupération de {len(regions_list)} régions depuis la base de données")
            
            return regions_list
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de toutes les régions: {str(e)}")
            return []
    
    async def create_region(self, region_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée une nouvelle région dans PostgreSQL
        
        Args:
            region_data: Dictionnaire contenant les données de la région
            
        Returns:
            Dictionnaire contenant les informations de la région créée
        """
        try:
            new_region = Region(
                name=region_data.get("name"),
                nb_habitants=region_data.get("nb_habitants", 0),
                language=region_data.get("language", "français"),
                country=region_data.get("country", "France"),
                latitude=region_data.get("latitude"),
                longitude=region_data.get("longitude")
            )
            
            self.session.add(new_region)
            await self.session.commit()
            await self.session.refresh(new_region)
            
            logger.info(f"Nouvelle région créée: {new_region.name} (ID: {new_region.id})")
            return new_region.to_dict()
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Erreur lors de la création de la région: {str(e)}")
            return {}
