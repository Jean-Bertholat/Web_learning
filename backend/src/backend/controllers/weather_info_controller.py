from fastapi.params import Depends
from backend.services.interfaces.Iweather_service import IWeatherService
from backend.services.implementation.weather_service import WeatherService, WeatherService1
from fastapi import APIRouter, Query
from backend.services.schemas.weather_resp_schema import WeatherResponse, WeatherForecastResponse

router = APIRouter()


# Choix de l'implémentation du service météo pour cette route
def get_weather_service() -> IWeatherService:
    return WeatherService1()

# End points API
@router.get("/weather/{region_name}", response_model=WeatherResponse)
async def get_weather_info(
    region_name: str,
    weather_service: IWeatherService = Depends(get_weather_service)
) -> WeatherResponse:
    
    resp = await weather_service.get_current_weather(region_name)
    return resp

@router.get("/weather/forecast/{region_name}", response_model=WeatherForecastResponse)
async def get_weather_forecast(
    region_name: str,
    day: int = Query(..., description="Nombre de jours de prévision"),
    weather_service: IWeatherService = Depends(get_weather_service)
) -> WeatherForecastResponse:
    
    response = await weather_service.get_weather_forecast(region_name=region_name, days=day)
    return response