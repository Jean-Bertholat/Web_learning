from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict, List
import logging

from backend.services.interfaces.Iregion_info_service import IRegionInformationService
from backend.services.schemas.region_resp_schema import RegionResponse
from backend.database.connection import get_database_session, AsyncSession
from backend.services.implementation.region_info_service import RegionInformationService

logger = logging.getLogger(__name__)

router = APIRouter()

# Configuration des providers pour l'injection de dépendances
async def get_region_service(session: AsyncSession = Depends(get_database_session)) -> IRegionInformationService:
    """
    Crée et retourne une instance du service de régions avec injection de dépendances.
    Utilise PostgreSQL si disponible, sinon se rabat sur les données mock.
    """
    return RegionInformationService()


# End points API
@router.get("/region/{region_id}", response_model=RegionResponse)
async def get_region_info_by_id(
    region_id: int,
    region_service: IRegionInformationService = Depends(get_region_service),
) -> RegionResponse:
    """
    Récupère les informations d'une région par son ID.
    
    Args:
        region_id: L'ID de la région à récupérer
        region_service: Service des régions (injecté automatiquement)
        
    Returns:
        RegionResponse: Informations de la région
        
    Raises:
        HTTPException: Si la région n'est pas trouvée ou en cas d'erreur
    """
    try:
        logger.info(f"Demande d'informations pour la région ID: {region_id}")
        region_info = await region_service.get_region_info_by_id(region_id)
        
        if not region_info or region_info.id == 0:
            raise HTTPException(status_code=404, detail=f"Région avec l'ID {region_id} non trouvée")
        
        return region_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la région {region_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/regions", response_model=List[RegionResponse])
async def get_all_regions(
    region_service: IRegionInformationService = Depends(get_region_service),
) -> List[RegionResponse]:
    """
    Récupère toutes les régions disponibles.
    
    Args:
        region_service: Service des régions (injecté automatiquement)
        
    Returns:
        List[RegionResponse]: Liste de toutes les régions
        
    Raises:
        HTTPException: En cas d'erreur lors de la récupération
    """
    try:
        logger.info("Demande de toutes les régions")
        regions = await region_service.get_all_regions()
        return regions
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de toutes les régions: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.post("/region", response_model=RegionResponse)
async def create_region(
    region_data: Dict[str, Any],
    region_service: IRegionInformationService = Depends(get_region_service),
) -> RegionResponse:
    """
    Crée une nouvelle région.
    
    Args:
        region_data: Données de la région à créer
        region_service: Service des régions (injecté automatiquement)
        
    Returns:
        RegionResponse: Informations de la région créée
        
    Raises:
        HTTPException: En cas d'erreur lors de la création
    """
    try:
        logger.info(f"Création d'une nouvelle région: {region_data.get('name')}")
        
        # Validation des données requises
        if not region_data.get('name'):
            raise HTTPException(status_code=400, detail="Le nom de la région est requis")
        
        new_region = await region_service.create_region(region_data)
        return new_region
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la création de la région: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur") 

### tmp
@router.get("/test/database")
async def test_database_connection():
    """
    Teste la connexion à la base de données PostgreSQL.
    
    Returns:
        Dictionnaire avec les résultats du test de connexion
    """
    try:
        from backend.database.connection import engine, db_config
        from sqlalchemy import text
        
        test_results = {
            "status": "success",
            "database_url": db_config.get_database_url().replace(db_config.password, "***"),
            "connection_test": False,
            "tables_exist": False,
            "message": "Test de connexion en cours..."
        }
        
        # Test de connexion basique
        async with engine.begin() as conn:
            # Test simple
            result = await conn.execute(text("SELECT 1 as test"))
            if result.fetchone()[0] == 1:
                test_results["connection_test"] = True
                test_results["message"] = "Connexion PostgreSQL réussie"
            
            # Vérification des tables
            tables_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name IN ('regions', 'weather_data', 'weather_forecasts')
            """)
            tables_result = await conn.execute(tables_query)
            tables = [row[0] for row in tables_result.fetchall()]
            
            test_results["existing_tables"] = tables
            test_results["tables_exist"] = len(tables) >= 2  # Au moins 2 tables sur 3
            
            if test_results["tables_exist"]:
                test_results["message"] += f" - Tables trouvées: {', '.join(tables)}"
            else:
                test_results["message"] += f" - Tables manquantes. Trouvées: {tables}"
        
        return test_results
        
    except Exception as e:
        logger.error(f"Erreur lors du test de connexion: {str(e)}")
        return {
            "status": "error",
            "connection_test": False,
            "tables_exist": False,
            "message": f"Erreur de connexion: {str(e)}",
            "error_details": str(e)
        }

@router.get("/test/repository")
async def test_repository_operations(session: AsyncSession = Depends(get_database_session)):
    """
    Teste les opérations du repository des régions.
    
    Returns:
        Résultats des tests du repository
    """
    try:
        region_service = await get_region_service(session)
        
        # Test de lecture de toutes les régions
        regions = await region_service.get_all_regions()
        
        # Test de lecture d'une région spécifique
        test_region = None
        if regions:
            test_region = await region_service.get_region_info(regions[0].id)
        
        return {
            "status": "success",
            "repository_type": type(region_service).__name__,
            "total_regions": len(regions),
            "test_region": {
                "id": test_region.id if test_region else None,
                "name": test_region.name if test_region else None
            } if test_region else None,
            "message": f"Repository fonctionne - {len(regions)} régions disponibles"
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du test du repository: {str(e)}")
        return {
            "status": "error",
            "message": f"Erreur du repository: {str(e)}",
            "error_details": str(e)
        } 