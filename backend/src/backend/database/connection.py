from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Base(DeclarativeBase):
    """Base class pour tous les modèles SQLAlchemy"""
    pass

class DatabaseConfig:
    """Configuration de la base de données"""
    
    def __init__(self):
        # Configuration par défaut (peut être surchargée par les variables d'environnement)
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.database = os.getenv("DB_NAME", "weather_app_db")
        self.username = os.getenv("DB_USER", "weather_user")
        self.password = os.getenv("DB_PASSWORD", "weather_password123")
        
        # Construction de l'URL de connexion
        self.database_url = f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def get_database_url(self) -> str:
        return self.database_url

# Instance globale de configuration
db_config = DatabaseConfig()

# Création du moteur async
engine = create_async_engine(
    db_config.get_database_url(),
    echo=True,  # Log des requêtes SQL (désactiver en production)
    future=True
)

# Factory pour créer des sessions
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_database_session() -> AsyncSession:
    """
    Fonction générateur pour obtenir une session de base de données.
    À utiliser avec FastAPI Depends.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_database():
    """
    Initialise la base de données en créant toutes les tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_database():
    """
    Ferme proprement la connexion à la base de données.
    """
    await engine.dispose()
