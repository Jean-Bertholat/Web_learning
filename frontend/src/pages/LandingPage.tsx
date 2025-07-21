import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

export const LandingPage: React.FC = () => {
    return (
        <div className="landing-page">
            <header className="landing-header">
                <h1>Weather & Region Info App</h1>
                <p>Bienvenue dans votre application météo et informations régionales</p>
            </header>
            
            <main className="landing-main">
                <div className="navigation-cards">
                    <div className="nav-card">
                        <h2>Informations Météorologiques</h2>
                        <p>Consultez les prévisions météo pour différentes régions</p>
                        <Link to="/weather" className="nav-button weather-button">
                            Voir la Météo
                        </Link>
                    </div>
                    
                    <div className="nav-card">
                        <h2>Informations Régionales</h2>
                        <p>Découvrez les détails et statistiques des régions</p>
                        <Link to="/regions" className="nav-button region-button">
                            Voir les Régions
                        </Link>
                    </div>
                </div>
            </main>
        </div>
    );
};
