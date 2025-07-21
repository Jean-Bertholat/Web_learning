import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { RegionInfoDisplay } from '../components/region_info_display';
import './RegionInfoPage.css';

export const RegionInfoPage: React.FC = () => {
    const [selectedRegionId, setSelectedRegionId] = useState<number>(1);
    const [customRegionId, setCustomRegionId] = useState<string>('');

    // Exemple de régions prédéfinies (vous pouvez ajuster selon vos données)
    const predefinedRegions = [
        { id: 1, name: 'Île-de-France' },
        { id: 2, name: 'Provence-Alpes-Côte d\'Azur' },
        { id: 3, name: 'Auvergne-Rhône-Alpes' },
        { id: 4, name: 'Nouvelle-Aquitaine' },
        { id: 5, name: 'Occitanie' },
        { id: 10, name: 'Normandie' }
    ];

    const handleRegionChange = (regionId: number) => {
        setSelectedRegionId(regionId);
        setCustomRegionId('');
    };

    const handleCustomRegionSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const id = parseInt(customRegionId);
        if (!isNaN(id) && id > 0) {
            setSelectedRegionId(id);
        }
    };

    return (
        <div className="region-page">
            <header className="page-header">
                <Link to="/" className="back-button">← Retour à l'accueil</Link>
                <h1>Informations Régionales</h1>
            </header>

            <div className="region-selector">
                <h2>Sélectionnez une région</h2>
                
                <div className="predefined-regions">
                    <h3>Régions prédéfinies</h3>
                    <div className="region-grid">
                        {predefinedRegions.map((region) => (
                            <button
                                key={region.id}
                                className={`region-card ${selectedRegionId === region.id ? 'active' : ''}`}
                                onClick={() => handleRegionChange(region.id)}
                            >
                                <span className="region-id">#{region.id}</span>
                                <span className="region-name">{region.name}</span>
                            </button>
                        ))}
                    </div>
                </div>

                <div className="custom-region">
                    <h3>ID de région personnalisé</h3>
                    <form onSubmit={handleCustomRegionSubmit} className="custom-region-form">
                        <input
                            type="number"
                            value={customRegionId}
                            onChange={(e) => setCustomRegionId(e.target.value)}
                            placeholder="Entrez un ID de région..."
                            min="1"
                            className="region-input"
                        />
                        <button type="submit" className="search-btn">
                            Rechercher
                        </button>
                    </form>
                </div>
            </div>

            <div className="region-content">
                <RegionInfoDisplay regionId={selectedRegionId} />
            </div>
        </div>
    );
};
