"""
Script de test de connexion à la base de données PostgreSQL
Permet de vérifier si la connexion fonctionne correctement
"""

import asyncio
import logging
from typing import Dict, Any

from backend.database.connection import engine, AsyncSessionLocal, db_config
from backend.repositories.implementations.postgresql_region_repository import PostgreSQLRegionRepository
from backend.repositories.implementations.postgresql_weather_repository import PostgreSQLWeatherRepository
from sqlalchemy import text

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_database_connection() -> Dict[str, Any]:
    """
    Teste la connexion à la base de données PostgreSQL
    
    Returns:
        Dictionnaire avec les résultats des tests
    """
    results = {
        "database_url": db_config.get_database_url(),
        "connection_test": False,
        "tables_exist": False,
        "data_test": False,
        "regions_count": 0,
        "weather_data_count": 0,
        "error": None
    }
    
    try:
        logger.info("🔍 Test de connexion à la base de données...")
        
        # Test 1: Connexion de base
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            if result.fetchone()[0] == 1:
                results["connection_test"] = True
                logger.info("✅ Connexion à PostgreSQL réussie")
            
            # Test 2: Vérification des tables
            tables_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables_result = await conn.execute(tables_query)
            tables = [row[0] for row in tables_result.fetchall()]
            
            expected_tables = ['regions', 'weather_data', 'weather_forecasts']
            tables_exist = all(table in tables for table in expected_tables)
            
            results["tables_exist"] = tables_exist
            results["existing_tables"] = tables
            
            if tables_exist:
                logger.info("✅ Toutes les tables requises existent")
            else:
                logger.warning(f"⚠️ Tables manquantes. Trouvées: {tables}")
        
        # Test 3: Test des repositories avec session
        async with AsyncSessionLocal() as session:
            # Test repository des régions
            region_repo = PostgreSQLRegionRepository(session)
            regions = await region_repo.get_all_regions()
            results["regions_count"] = len(regions)
            
            # Test repository météo
            weather_repo = PostgreSQLWeatherRepository(session)
            paris_weather = await weather_repo.get_weather_by_region("Paris")
            
            if regions and paris_weather:
                results["data_test"] = True
                logger.info(f"✅ Données testées: {len(regions)} régions trouvées")
            else:
                logger.warning("⚠️ Aucune donnée trouvée dans les tables")
    
    except Exception as e:
        results["error"] = str(e)
        logger.error(f"❌ Erreur lors du test de connexion: {e}")
    
    return results

async def test_repository_operations() -> Dict[str, Any]:
    """
    Teste les opérations CRUD des repositories
    
    Returns:
        Résultats des tests CRUD
    """
    crud_results = {
        "create_test": False,
        "read_test": False,
        "update_test": False,
        "delete_test": False,
        "error": None
    }
    
    try:
        async with AsyncSessionLocal() as session:
            region_repo = PostgreSQLRegionRepository(session)
            
            # Test CREATE
            test_region_data = {
                "name": "Test Region",
                "nb_habitants": 1000,
                "language": "français",
                "country": "France Test"
            }
            
            created_region = await region_repo.create_region(test_region_data)
            if created_region and created_region.get("id"):
                crud_results["create_test"] = True
                test_region_id = created_region["id"]
                logger.info(f"✅ CREATE: Région test créée avec ID {test_region_id}")
                
                # Test READ
                read_region = await region_repo.get_region_by_id(test_region_id)
                if read_region and read_region.get("name") == "Test Region":
                    crud_results["read_test"] = True
                    logger.info("✅ READ: Région test lue avec succès")
                
                # Test UPDATE
                update_data = {"nb_habitants": 2000}
                updated_region = await region_repo.update_region(test_region_id, update_data)
                if updated_region and updated_region.get("nb_habitants") == 2000:
                    crud_results["update_test"] = True
                    logger.info("✅ UPDATE: Région test mise à jour")
                
                # Test DELETE
                delete_success = await region_repo.delete_region(test_region_id)
                if delete_success:
                    crud_results["delete_test"] = True
                    logger.info("✅ DELETE: Région test supprimée")
    
    except Exception as e:
        crud_results["error"] = str(e)
        logger.error(f"❌ Erreur lors des tests CRUD: {e}")
    
    return crud_results

async def main():
    """Fonction principale pour exécuter tous les tests"""
    logger.info("🚀 Démarrage des tests de base de données...")
    
    # Test de connexion
    connection_results = await test_database_connection()
    
    # Tests CRUD si la connexion fonctionne
    crud_results = {}
    if connection_results["connection_test"]:
        crud_results = await test_repository_operations()
    
    # Affichage des résultats
    logger.info("\n" + "="*50)
    logger.info("📊 RÉSULTATS DES TESTS")
    logger.info("="*50)
    
    logger.info(f"🔗 URL de connexion: {connection_results['database_url']}")
    logger.info(f"🔌 Connexion: {'✅' if connection_results['connection_test'] else '❌'}")
    logger.info(f"📋 Tables: {'✅' if connection_results['tables_exist'] else '❌'}")
    logger.info(f"📊 Données: {'✅' if connection_results['data_test'] else '❌'}")
    logger.info(f"📈 Régions: {connection_results['regions_count']}")
    
    if crud_results:
        logger.info(f"➕ CREATE: {'✅' if crud_results['create_test'] else '❌'}")
        logger.info(f"👁️ READ: {'✅' if crud_results['read_test'] else '❌'}")
        logger.info(f"✏️ UPDATE: {'✅' if crud_results['update_test'] else '❌'}")
        logger.info(f"🗑️ DELETE: {'✅' if crud_results['delete_test'] else '❌'}")
    
    if connection_results.get("error"):
        logger.error(f"❌ Erreur: {connection_results['error']}")
    
    logger.info("="*50)
    
    return {**connection_results, **crud_results}

if __name__ == "__main__":
    asyncio.run(main())
