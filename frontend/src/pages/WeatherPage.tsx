import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { WeatherDisplay } from '../components/weather_display';
import './WeatherPage.css';

export const WeatherPage: React.FC = () => {
    const [selectedRegion, setSelectedRegion] = useState<string>('Paris');
    const [customRegion, setCustomRegion] = useState<string>('');

    const predefinedRegions = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Nantes'];

    const handleRegionChange = (region: string) => {
        setSelectedRegion(region);
        setCustomRegion('');
    };

    const handleCustomRegionSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (customRegion.trim()) {
            setSelectedRegion(customRegion.trim());
        }
    };

    return (
        <div className="weather-page">
            <header className="page-header">
                <Link to="/" className="back-button">← Retour à l'accueil</Link>
                <h1>Informations Météorologiques</h1>
            </header>

            <div className="region-selector">
                <h2>Sélectionnez une région</h2>
                
                <div className="predefined-regions">
                    <h3>Régions prédéfinies</h3>
                    <div className="region-buttons">
                        {predefinedRegions.map((region) => (
                            <button
                                key={region}
                                className={`region-btn ${selectedRegion === region ? 'active' : ''}`}
                                onClick={() => handleRegionChange(region)}
                            >
                                {region}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="custom-region">
                    <h3>Région personnalisée</h3>
                    <form onSubmit={handleCustomRegionSubmit} className="custom-region-form">
                        <input
                            type="text"
                            value={customRegion}
                            onChange={(e) => setCustomRegion(e.target.value)}
                            placeholder="Entrez le nom d'une ville..."
                            className="region-input"
                        />
                        <button type="submit" className="search-btn">
                            Rechercher
                        </button>
                    </form>
                </div>
            </div>

            <div className="weather-content">
                <WeatherDisplay region={selectedRegion} />
            </div>
        </div>
    );
};
