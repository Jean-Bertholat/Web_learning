from pydantic import BaseModel

class WeatherResponse(BaseModel):
    region: str
    temperature: int
    condition: str
    humidity: int
    
class WeatherForecastResponse(BaseModel):
    region: str
    temperature: int
    condition: str
    humidity: int
    day: int