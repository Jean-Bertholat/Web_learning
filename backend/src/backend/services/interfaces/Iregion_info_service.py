from abc import ABC, abstractmethod
from typing import Dict, Any

from backend.services.schemas.region_resp_schema import RegionResponse

class IRegionInformationService(ABC):
    @abstractmethod
    async def get_region_info_by_id(self, region_id: int) -> RegionResponse:
        """Récupère les informations d'une région"""
        pass
    
    @abstractmethod
    async def get_all_regions(self) -> list[RegionResponse]:
        """Récupère toutes les régions"""
        pass
    
    @abstractmethod
    async def create_region(self, region_data: Dict[str, Any]) -> RegionResponse:
        """Crée une nouvelle région"""
        pass