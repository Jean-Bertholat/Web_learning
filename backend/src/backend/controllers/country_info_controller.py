from fastapi import APIRouter, Depends

from ..services.interfaces.Iregion_info_service import IRegionInformationService
from ..services.implementation.region_info_service import RegionInformationService
from ..services.schemas.region_resp_schema import RegionResponse


router = APIRouter()


# Configuration des providers pour l'injection de dépendances
def get_region_service() -> IRegionInformationService:
    return RegionInformationService()


@router.get("/region/{region_id}", response_model=RegionResponse)
async def get_region(
    region_id: int,
    region_service: IRegionInformationService = Depends(get_region_service),
) -> RegionResponse:
    
    region_info = await region_service.get_region_info(region_id)
    return region_info