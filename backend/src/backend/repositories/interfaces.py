from abc import ABC, abstractmethod
from typing import Any, Dict, List

class IRegionRepository(ABC):
    @abstractmethod
    async def get_region_by_id(self, region_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_all_regions(self) -> List[Dict[str, Any]]:
        pass

class IWeatherRepository(ABC):
    @abstractmethod
    async def get_weather_by_region(self, region_name: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_weather_forecast(self, region_name: str, days: int) -> List[Dict[str, Any]]:
        pass
