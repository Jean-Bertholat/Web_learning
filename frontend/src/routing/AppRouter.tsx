import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { LandingPage } from '../pages/LandingPage';
import { WeatherPage } from '../pages/WeatherPage';
import { RegionInfoPage } from '../pages/RegionInfoPage';

export const AppRouter: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/weather" element={<WeatherPage />} />
                <Route path="/regions" element={<RegionInfoPage />} />
                {/* Route de fallback pour les URLs non trouvées */}
                <Route path="*" element={<LandingPage />} />
            </Routes>
        </Router>
    );
};
