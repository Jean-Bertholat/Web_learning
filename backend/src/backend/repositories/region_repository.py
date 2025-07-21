from backend.repositories.interfaces import IRegionRepository
from typing import Any, Dict, List

# Exemple d'implémentation avec une fausse base (à remplacer par du SQLAlchemy, etc.)
class RegionRepository(IRegionRepository):
    def __init__(self):
        self._regions = [
            {"id": 1, "name": "Paris", "nb_habitants": 2000000, "language": "français"},
            {"id": 2, "name": "Lyon", "nb_habitants": 500000, "language": "français"},
        ]

    async def get_region_by_id(self, region_id: int) -> Dict[str, Any]:
        for region in self._regions:
            if region["id"] == region_id:
                return region
        return {}

    async def get_all_regions(self) -> List[Dict[str, Any]]:
        return self._regions
