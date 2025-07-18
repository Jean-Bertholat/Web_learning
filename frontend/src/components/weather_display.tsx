import React, { useEffect, useState } from 'react';
import { WeatherController } from '../controllers/weather_service_controller';
import { WeatherInfo, WeatherForecast } from '../services/schemas/weather_resp_schema';

interface WeatherDisplayProps {
    region: string;
}

export const WeatherDisplay: React.FC<WeatherDisplayProps> = ({ region }) => {
    const weatherService = WeatherController();
    const [weather, setWeather] = useState<WeatherInfo | null>(null);
    const [forecast, setForecast] = useState<WeatherForecast | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [currentWeather, forecastData] = await Promise.all([
                    weatherService.get_current_weather(region),
                    weatherService.get_weather_forecast(region, 5)
                ]);
                setWeather(currentWeather);
                setForecast(forecastData);
            } catch (err) {
                setError('Failed to fetch weather data');
            }
        };

        fetchData();
    }, [region]);

    if (error) return <div className="error">{error}</div>;
    if (!weather) return <div>Loading...</div>;
    if (!forecast) return <div>Loading forecast...</div>;

    return (
        <div className="weather-display">
            <h2>Weather in {region}</h2>
            <div className="current-weather">
                <h3>Current Weather</h3>
                <p>Temperature: {weather.temperature}°C</p>
                <p>Condition: {weather.condition}</p>
                <p>Humidity: {weather.humidity}%</p>
            </div>
            <div className="forecast">
                <h3>Forecast</h3>
                <p>Temperature: {forecast.temperature}°C</p>
                <p>Condition: {forecast.condition}</p>
                <p>Humidity: {forecast.humidity}%</p>
                <p>Day: {forecast.day}</p>
            </div>
        </div>
    );
};
