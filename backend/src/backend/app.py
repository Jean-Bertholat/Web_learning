from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from backend.controllers.region_info_controller import router as country_router
from backend.controllers.weather_info_controller import router as weather_router
from backend.database.connection import init_database, close_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire du cycle de vie de l'application.
    Initialise la base de données au démarrage et la ferme à l'arrêt.
    """

app = FastAPI(
    title="Weather & Region Info API",
    description="API pour les informations météorologiques et régionales",
    version="1.0.0",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL de votre frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(country_router, prefix="/api/v1", tags=["regions"])
app.include_router(weather_router, prefix="/api/v1", tags=["weather"])

@app.get("/")
async def root():
    """Endpoint de base pour vérifier que l'API fonctionne"""
    return {
        "message": "Weather & Region Info API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Endpoint de vérification de santé de l'API"""
    return {
        "status": "healthy",
        "message": "API is running properly"
    }

def startup():
    """Fonction de démarrage de l'application"""
    uvicorn.run(
        "backend.app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )