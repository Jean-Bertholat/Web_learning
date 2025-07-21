@echo off
REM Script PowerShell pour démarrer facilement la base de données PostgreSQL

echo === Démarrage de la base de données PostgreSQL ===

REM Vérifier si Docker est en cours d'exécution
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Erreur: Docker n'est pas en cours d'exécution
    echo Veuillez démarrer Docker Desktop et réessayer
    pause
    exit /b 1
)

REM Se déplacer dans le dossier database
cd /d "%~dp0"

echo 📁 Dossier actuel: %cd%

REM Démarrer les services Docker Compose
echo 🚀 Démarrage des conteneurs PostgreSQL et PgAdmin...
docker-compose up -d

REM Vérifier le statut des conteneurs
echo 📊 Statut des conteneurs:
docker-compose ps

echo.
echo ✅ Base de données démarrée avec succès!
echo.
echo 🔗 Connexions disponibles:
echo    PostgreSQL:
echo      Host: localhost
echo      Port: 5432
echo      Database: weather_app_db
echo      Username: weather_user
echo      Password: weather_password123
echo.
echo    PgAdmin (Interface Web):
echo      URL: http://localhost:8080
echo      Email: admin@weather.com
echo      Password: admin123
echo.
echo 📝 Pour arrêter la base de données:
echo    docker-compose down
echo.
echo 🔄 Pour réinitialiser complètement la base:
echo    docker-compose down -v
echo    docker-compose up -d

pause
