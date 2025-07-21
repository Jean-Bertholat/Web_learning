#!/bin/bash

# Script pour démarrer facilement la base de données PostgreSQL

echo "=== Démarrage de la base de données PostgreSQL ==="

# Vérifier si Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Erreur: Docker n'est pas en cours d'exécution"
    echo "Veuillez démarrer Docker Desktop et réessayer"
    exit 1
fi

# Se déplacer dans le dossier database
cd "$(dirname "$0")"

echo "📁 Dossier actuel: $(pwd)"

# Démarrer les services Docker Compose
echo "🚀 Démarrage des conteneurs PostgreSQL et PgAdmin..."
docker-compose up -d

# Vérifier le statut des conteneurs
echo "📊 Statut des conteneurs:"
docker-compose ps

echo ""
echo "✅ Base de données démarrée avec succès!"
echo ""
echo "🔗 Connexions disponibles:"
echo "   PostgreSQL:"
echo "     Host: localhost"
echo "     Port: 5432"
echo "     Database: weather_app_db"
echo "     Username: weather_user"
echo "     Password: weather_password123"
echo ""
echo "   PgAdmin (Interface Web):"
echo "     URL: http://localhost:8080"
echo "     Email: admin@weather.com"
echo "     Password: admin123"
echo ""
echo "📝 Pour arrêter la base de données:"
echo "   docker-compose down"
echo ""
echo "🔄 Pour réinitialiser complètement la base:"
echo "   docker-compose down -v"
echo "   docker-compose up -d"
