// import { createContext, useContext } from 'react';
// import { IWeatherService } from '../interfaces/Iweather_service';
import { WeatherService, WeatherService1 } from '../services/implementations/weather_service';

// // Création du contexte pour l'injection de dépendances
// export const WeatherServiceContext = createContext<IWeatherService>(new WeatherService());

// Hook personnalisé pour utiliser le service
export const WeatherController = () => {
    return new WeatherService1();
};
