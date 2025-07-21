from typing import Dict, Any

from backend.services.schemas.region_resp_schema import RegionResponse
from backend.services.interfaces.Iregion_info_service import IRegionInformationService


class RegionInformationService(IRegionInformationService):
    async def get_region_info(self, region_id: int) -> RegionResponse:
        region_data = {
            "id": region_id,
            "name": "Île-de-France",
            "nb_habitants": 1000000,
            "language": "French",
        }
        return RegionResponse(**region_data)
