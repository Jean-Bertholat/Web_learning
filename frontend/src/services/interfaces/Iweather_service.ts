import { WeatherForecast, WeatherInfo } from "../schemas/weather_resp_schema";


export interface IWeatherService {
    get_current_weather(region: string): Promise<WeatherInfo>;
    get_weather_forecast(region: string, days: number): Promise<WeatherForecast>;
}
