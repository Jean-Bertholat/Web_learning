export interface WeatherInfo {
    region: string;
    temperature: number;
    condition: string;
    humidity: number;
}

export interface WeatherForecast extends WeatherInfo {
    day: number;
}