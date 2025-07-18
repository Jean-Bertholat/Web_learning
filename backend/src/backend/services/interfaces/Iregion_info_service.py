from abc import ABC, abstractmethod
from typing import Dict, Any

class IRegionInformationService(ABC):
    @abstractmethod
    async def get_region_info(self, region_id: int) -> Dict[str, Any]:
        """Récupère les informations d'une région"""
        pass