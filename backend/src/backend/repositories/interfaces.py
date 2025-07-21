from abc import ABC, abstractmethod
from typing import Any, Dict, List

class IRegionRepository(ABC):
    @abstractmethod
    async def get_region_info_by_id(self, region_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_all_regions(self) -> List[Dict[str, Any]]:
        pass

###
    @abstractmethod
    async def get_region_by_name(self, region_name: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def create_region(self, region_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def update_region(self, region_id: int, region_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def delete_region(self, region_id: int) -> bool:
        pass

class IWeatherRepository(ABC):
    @abstractmethod
    async def get_weather_by_region(self, region_name: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_weather_forecast(self, region_name: str, days: int) -> List[Dict[str, Any]]:
        pass

###    
    @abstractmethod
    async def create_weather_data(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def create_weather_forecast(self, forecast_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_weather_history(self, region_name: str, days: int = 7) -> List[Dict[str, Any]]:
        pass
