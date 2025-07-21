from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.controllers.country_info_controller import router as country_router
from backend.controllers.weather_info_controller import router as weather_router


app = FastAPI(title="AMADEUS")


# Inclusion du router
app.include_router(country_router, prefix="/api/v1", tags=["country"])
app.include_router(weather_router, prefix="/api/v1", tags=["weather"])


def startup():
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)


# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL de votre frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)