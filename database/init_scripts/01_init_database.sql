-- Script d'initialisation de la base de données
-- Ce script sera exécuté automatiquement lors du premier démarrage du conteneur PostgreSQL

-- Création des tables

-- Table des régions
CREATE TABLE IF NOT EXISTS regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    nb_habitants INTEGER NOT NULL DEFAULT 0,
    language VARCHAR(50) NOT NULL DEFAULT 'français',
    country VARCHAR(100) NOT NULL DEFAULT 'France',
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des données météorologiques
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    condition VARCHAR(100) NOT NULL,
    humidity INTEGER NOT NULL CHECK (humidity >= 0 AND humidity <= 100),
    pressure DECIMAL(6,2),
    wind_speed DECIMAL(5,2),
    wind_direction VARCHAR(3),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_forecast BOOLEAN DEFAULT FALSE,
    forecast_day INTEGER DEFAULT 0
);

-- Table des prévisions météorologiques (structure plus détaillée)
CREATE TABLE IF NOT EXISTS weather_forecasts (
    id SERIAL PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL,
    forecast_date DATE NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    temperature_min DECIMAL(5,2),
    temperature_max DECIMAL(5,2),
    temperature_avg DECIMAL(5,2),
    condition VARCHAR(100) NOT NULL,
    humidity INTEGER NOT NULL CHECK (humidity >= 0 AND humidity <= 100),
    pressure DECIMAL(6,2),
    wind_speed DECIMAL(5,2),
    wind_direction VARCHAR(3),
    precipitation_probability INTEGER DEFAULT 0 CHECK (precipitation_probability >= 0 AND precipitation_probability <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_regions_name ON regions(name);
CREATE INDEX IF NOT EXISTS idx_weather_data_region_name ON weather_data(region_name);
CREATE INDEX IF NOT EXISTS idx_weather_data_recorded_at ON weather_data(recorded_at);
CREATE INDEX IF NOT EXISTS idx_weather_forecasts_region_name ON weather_forecasts(region_name);
CREATE INDEX IF NOT EXISTS idx_weather_forecasts_date ON weather_forecasts(forecast_date);

-- Insertion de données d'exemple pour les régions
INSERT INTO regions (name, nb_habitants, language, country, latitude, longitude) VALUES
    ('Paris', 2165423, 'français', 'France', 48.856614, 2.352222),
    ('Lyon', 515695, 'français', 'France', 45.764043, 4.835659),
    ('Marseille', 863310, 'français', 'France', 43.296482, 5.369780),
    ('Toulouse', 479553, 'français', 'France', 43.604652, 1.444209),
    ('Nice', 342295, 'français', 'France', 43.710173, 7.261953),
    ('Nantes', 314138, 'français', 'France', 47.218371, -1.553621),
    ('Strasbourg', 280966, 'français', 'France', 48.573405, 7.752111),
    ('Montpellier', 285121, 'français', 'France', 43.610769, 3.876716),
    ('Bordeaux', 254436, 'français', 'France', 44.837789, -0.579180),
    ('Lille', 232787, 'français', 'France', 50.629250, 3.057256)
ON CONFLICT (name) DO NOTHING;

-- Insertion de données d'exemple pour la météo actuelle
INSERT INTO weather_data (region_name, temperature, condition, humidity, pressure, wind_speed, wind_direction, is_forecast) VALUES
    ('Paris', 22.5, 'Partly Cloudy', 65, 1013.25, 15.2, 'NW', FALSE),
    ('Lyon', 25.1, 'Sunny', 58, 1015.80, 8.7, 'S', FALSE),
    ('Marseille', 28.3, 'Sunny', 52, 1016.90, 12.3, 'SE', FALSE),
    ('Toulouse', 24.7, 'Cloudy', 70, 1012.45, 10.1, 'W', FALSE),
    ('Nice', 26.8, 'Sunny', 60, 1014.20, 18.5, 'E', FALSE)
ON CONFLICT DO NOTHING;

-- Insertion de données d'exemple pour les prévisions
INSERT INTO weather_forecasts (region_name, forecast_date, day_name, temperature_min, temperature_max, temperature_avg, condition, humidity, pressure, wind_speed, wind_direction, precipitation_probability) VALUES
    ('Paris', CURRENT_DATE + INTERVAL '1 day', 'Demain', 18.0, 26.0, 22.0, 'Partly Cloudy', 68, 1012.0, 12.0, 'NW', 20),
    ('Paris', CURRENT_DATE + INTERVAL '2 days', 'Après-demain', 19.0, 24.0, 21.5, 'Rainy', 75, 1008.0, 15.0, 'W', 80),
    ('Lyon', CURRENT_DATE + INTERVAL '1 day', 'Demain', 20.0, 28.0, 24.0, 'Sunny', 55, 1016.0, 8.0, 'S', 10),
    ('Lyon', CURRENT_DATE + INTERVAL '2 days', 'Après-demain', 22.0, 30.0, 26.0, 'Sunny', 50, 1017.0, 6.0, 'SE', 5),
    ('Marseille', CURRENT_DATE + INTERVAL '1 day', 'Demain', 24.0, 32.0, 28.0, 'Sunny', 48, 1018.0, 14.0, 'SE', 0),
    ('Marseille', CURRENT_DATE + INTERVAL '2 days', 'Après-demain', 25.0, 33.0, 29.0, 'Sunny', 45, 1019.0, 16.0, 'E', 0)
ON CONFLICT DO NOTHING;

-- Fonction pour mettre à jour automatiquement le champ updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger pour mettre à jour automatiquement updated_at dans la table regions
CREATE TRIGGER update_regions_updated_at 
    BEFORE UPDATE ON regions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

COMMIT;
