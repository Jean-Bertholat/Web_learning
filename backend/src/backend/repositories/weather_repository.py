from backend.repositories.interfaces import IWeatherRepository
from typing import Any, Dict, List
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-or-service-key")

class WeatherRepository(IWeatherRepository):
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    async def get_weather_by_region(self, region_name: str) -> Dict[str, Any]:
        response = self.supabase.table("weather").select("*").eq("region", region_name).execute()
        data = response.data
        if data:
            return data[0]
        return {}

    async def get_weather_forecast(self, region_name: str, days: int) -> List[Dict[str, Any]]:
        response = self.supabase.table("weather_forecast").select("*").eq("region", region_name).lte("day", days).execute()
        return response.data or []
