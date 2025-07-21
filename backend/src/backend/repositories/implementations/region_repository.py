from backend.repositories.interfaces import IRegionRepository
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

# Exemple d'implémentation avec une fausse base (à remplacer par du SQLAlchemy, etc.)
class RegionRepository(IRegionRepository):
    """
    Implémentation mock du repository des régions.
    Utilise des données fictives pour les tests et le développement.
    """
    
    def __init__(self):
        self._regions = [
            {"id": 1, "name": "Paris", "nb_habitants": 2165423, "language": "français", "country": "France"},
            {"id": 2, "name": "Lyon", "nb_habitants": 515695, "language": "français", "country": "France"},
            {"id": 3, "name": "Marseille", "nb_habitants": 863310, "language": "français", "country": "France"},
            {"id": 4, "name": "Toulouse", "nb_habitants": 479553, "language": "français", "country": "France"},
            {"id": 5, "name": "Nice", "nb_habitants": 342295, "language": "français", "country": "France"},
            {"id": 10, "name": "Normandie", "nb_habitants": 3320000, "language": "français", "country": "France"},
        ]
        self._next_id = max(region["id"] for region in self._regions) + 1

    async def get_region_info_by_id(self, region_id: int) -> Dict[str, Any]:
        """Récupère une région par son ID (version mock)"""
        logger.info(f"Mock: Récupération de la région avec l'ID {region_id}")
        
        for region in self._regions:
            if region["id"] == region_id:
                return region
        return {}

    async def get_all_regions(self) -> List[Dict[str, Any]]:
        """Récupère toutes les régions (version mock)"""
        logger.info(f"Mock: Récupération de toutes les régions ({len(self._regions)} régions)")
        return self._regions.copy()
    
    async def get_region_by_name(self, region_name: str) -> Dict[str, Any]:
        """Récupère une région par son nom (version mock)"""
        logger.info(f"Mock: Récupération de la région avec le nom {region_name}")
        
        for region in self._regions:
            if region_name.lower() in region["name"].lower() or region["name"].lower() in region_name.lower():
                return region
        return {}
    
    async def create_region(self, region_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée une nouvelle région (version mock)"""
        logger.info(f"Mock: Création d'une nouvelle région: {region_data.get('name')}")
        
        new_region = {
            "id": self._next_id,
            "name": region_data.get("name", "Unknown"),
            "nb_habitants": region_data.get("nb_habitants", 0),
            "language": region_data.get("language", "français"),
            "country": region_data.get("country", "France")
        }
        
        self._regions.append(new_region)
        self._next_id += 1
        
        return new_region
    
    async def update_region(self, region_id: int, region_data: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour une région existante (version mock)"""
        logger.info(f"Mock: Mise à jour de la région avec l'ID {region_id}")
        
        for i, region in enumerate(self._regions):
            if region["id"] == region_id:
                # Mise à jour des champs fournis
                for key, value in region_data.items():
                    if key in region and value is not None:
                        region[key] = value
                
                self._regions[i] = region
                return region
        
        return {}
    
    async def delete_region(self, region_id: int) -> bool:
        """Supprime une région (version mock)"""
        logger.info(f"Mock: Suppression de la région avec l'ID {region_id}")
        
        for i, region in enumerate(self._regions):
            if region["id"] == region_id:
                del self._regions[i]
                return True
        
        return False
