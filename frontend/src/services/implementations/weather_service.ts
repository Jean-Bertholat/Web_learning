import { IWeatherService } from '../interfaces/Iweather_service';
import { WeatherForecast, WeatherInfo } from '../schemas/weather_resp_schema';

export class WeatherService implements IWeatherService {
    private baseUrl: string;

    constructor(baseUrl: string = 'http://localhost:8000/api/v1') {
        this.baseUrl = baseUrl;
    }

    async get_current_weather(region: string): Promise<WeatherInfo> {
        const response = await fetch(`${this.baseUrl}/weather/${region}`);
        if (!response.ok) {
            throw new Error('Failed to call backend');
        }
        return response.json();
    }

    async get_weather_forecast(region: string, days: number): Promise<WeatherForecast> {
        const response = await fetch(`${this.baseUrl}/weather/forecast/${region}?day=${days}`);
        console.log(response);
        if (!response.ok) {
            throw new Error('Failed to call backend');
        }
        return response.json();
    }
}

export class WeatherService1 implements IWeatherService {
    private baseUrl: string;

    constructor(baseUrl: string = 'http://localhost:8000/api/v1') {
        this.baseUrl = baseUrl;
    }

    async get_current_weather(region: string): Promise<WeatherInfo> {
        const response = {
            region: region,
            temperature: 25,
            condition: 'Sunny',
            humidity: 60
        };
        return response as WeatherInfo;
    }

    async get_weather_forecast(region: string, days: number): Promise<WeatherForecast> {
        const response = await fetch(`${this.baseUrl}/weather/forecast/${region}?day=${days}`);
        if (!response.ok) {
            throw new Error('Failed to call backend');
        }
        return response.json();
    }
}