# Configuration de la Base de Données

Ce dossier contient la configuration PostgreSQL pour l'application Weather App.

## Structure

```
database/
├── docker-compose.yml          # Configuration Docker Compose
├── init_scripts/              # Scripts d'initialisation
│   └── 01_init_database.sql   # Script de création des tables et données
└── README.md                  # Ce fichier
```

## Démarrage

1. **Démarrer la base de données** :
   ```bash
   cd database
   docker-compose up -d
   ```

2. **Arrêter la base de données** :
   ```bash
   docker-compose down
   ```

3. **Réinitialiser complètement la base** :
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

## Accès

### Base de données PostgreSQL
- **Host** : localhost
- **Port** : 5432
- **Database** : weather_app_db
- **Username** : weather_user
- **Password** : weather_password123

### PgAdmin (Interface Web)
- **URL** : http://localhost:8080
- **Email** : admin@weather.com
- **Password** : admin123

## Configuration de connexion pour le backend

```python
DATABASE_URL = "postgresql://weather_user:weather_password123@localhost:5432/weather_app_db"
```

## Tables créées

1. **regions** : Informations sur les régions/villes
2. **weather_data** : Données météorologiques actuelles
3. **weather_forecasts** : Prévisions météorologiques

## Données d'exemple

Le script d'initialisation insère automatiquement :
- 10 régions françaises avec leurs informations
- Données météo actuelles pour 5 villes
- Prévisions sur 2 jours pour 3 villes
