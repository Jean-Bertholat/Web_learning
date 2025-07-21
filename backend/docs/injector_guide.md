# Guide d'utilisation de l'injection de dépendances avec la lib `injector`

## 🎯 Pourquoi utiliser la bibliothèque `injector` ?

### Avantages par rapport à l'injection manuelle

#### 1. **Configuration centralisée**
```python
# AVANT (injection manuelle)
def get_region_service(session):
    if should_use_postgresql():
        repo = PostgreSQLRegionRepository(session)
    else:
        repo = RegionRepository()
    return RegionInformationService(repo)

# APRÈS (avec injector)
class DatabaseModule(Module):
    def configure(self, binder):
        if self._should_use_postgresql():
            binder.bind(IRegionRepository, to=PostgreSQLRegionRepository)
        else:
            binder.bind(IRegionRepository, to=RegionRepository)
```

#### 2. **Gestion automatique des dépendances**
```python
# AVANT
class RegionInformationService:
    def __init__(self, region_repository):
        self.region_repository = region_repository

# APRÈS
class RegionInformationService:
    @inject
    def __init__(self, region_repository: IRegionRepository):
        self.region_repository = region_repository
        # injector résout automatiquement IRegionRepository
```

#### 3. **Singleton et cycle de vie**
```python
@provider
@singleton
def provide_database_session(self) -> AsyncSession:
    return AsyncSessionLocal()
    # Une seule instance partagée dans toute l'application
```

## 🏗️ Architecture avec injector

### Structure des modules

```
backend/di/
├── container.py           # Configuration principale
├── modules/
│   ├── database.py       # Module base de données
│   ├── services.py       # Module services
│   └── repositories.py   # Module repositories
```

### Types de bindings

#### 1. **Binding d'interface à implémentation**
```python
binder.bind(IRegionRepository, to=PostgreSQLRegionRepository)
```

#### 2. **Binding avec provider**
```python
@provider
def provide_config(self) -> DatabaseConfig:
    return DatabaseConfig()
```

#### 3. **Binding avec singleton**
```python
@provider
@singleton
def provide_session(self) -> AsyncSession:
    return AsyncSessionLocal()
```

## 🔧 Utilisation pratique

### 1. Installation
```bash
pip install injector
# ou dans pyproject.toml
injector = ">=0.22.0,<1.0.0"
```

### 2. Configuration de base
```python
from injector import Module, Injector, inject

class MyModule(Module):
    def configure(self, binder):
        binder.bind(Interface, to=Implementation)

injector = Injector([MyModule()])
```

### 3. Injection dans les classes
```python
class MyService:
    @inject
    def __init__(self, repo: IRepository, config: Config):
        self.repo = repo
        self.config = config
```

### 4. Récupération d'instances
```python
# Via l'injector
service = injector.get(IService)

# Via des helpers
from backend.di.container import get_region_service
service = get_region_service()
```

## 🧪 Tests avec injector

### Configuration pour les tests
```python
class TestModule(Module):
    def configure(self, binder):
        binder.bind(IRepository, to=MockRepository)

def test_service():
    test_injector = Injector([TestModule()])
    service = test_injector.get(IService)
    # service utilise automatiquement MockRepository
```

### Mocking facile
```python
class MockRegionRepository(IRegionRepository):
    async def get_region_by_id(self, id):
        return {"id": id, "name": "Test Region"}

# Dans les tests
binder.bind(IRegionRepository, to=MockRegionRepository)
```

## 🎛️ Configuration avancée

### Conditional binding
```python
class DatabaseModule(Module):
    def configure(self, binder):
        if os.getenv("USE_POSTGRESQL") == "true":
            binder.bind(IRepository, to=PostgreSQLRepository)
        else:
            binder.bind(IRepository, to=MockRepository)
```

### Multiple implementations
```python
class ServiceModule(Module):
    def configure(self, binder):
        binder.multibind(IPlugin, to=PluginA)
        binder.multibind(IPlugin, to=PluginB)

# Utilisation
@inject
def __init__(self, plugins: List[IPlugin]):
    self.plugins = plugins  # [PluginA(), PluginB()]
```

## 📈 Avantages dans votre projet

### 1. **Flexibilité environnement**
- **Développement** : Utilise des mocks pour développer sans DB
- **Test** : Injection automatique de mocks
- **Production** : Utilise PostgreSQL automatiquement

### 2. **Maintenance simplifiée**
- Changement d'implémentation sans modifier le code métier
- Configuration centralisée dans les modules
- Dépendances explicites et typées

### 3. **Performance**
- Singletons automatiques pour les ressources coûteuses
- Lazy loading des dépendances
- Réutilisation d'instances

### 4. **Testabilité**
- Mocking automatique et propre
- Isolation complète des tests
- Configuration spécifique par test

## 🚀 Migration de votre code existant

### Étape 1: Installer injector
```bash
poetry add injector
```

### Étape 2: Créer les modules
```python
# backend/di/container.py
from injector import Module, Injector

class ApplicationModule(Module):
    def configure(self, binder):
        # Vos bindings ici
        pass

_injector = Injector([ApplicationModule()])
```

### Étape 3: Modifier les services
```python
# Avant
class Service:
    def __init__(self, repo):
        self.repo = repo

# Après
class Service:
    @inject
    def __init__(self, repo: IRepository):
        self.repo = repo
```

### Étape 4: Utiliser dans les contrôleurs
```python
# Avant
def get_service():
    return ServiceFactory.create()

# Après
def get_service():
    return get_injector().get(IService)
```

## 🔍 Debug et monitoring

### Vérification des bindings
```python
def check_bindings():
    injector = get_injector()
    
    # Tester chaque binding
    region_service = injector.get(IRegionInformationService)
    weather_service = injector.get(IWeatherService)
    
    print(f"Region service: {type(region_service).__name__}")
    print(f"Weather service: {type(weather_service).__name__}")
```

### Graphe des dépendances
```python
def print_dependency_graph():
    # Affiche toutes les dépendances configurées
    logger.info("Dependency graph:")
    logger.info("IRegionRepository -> Implementation")
    logger.info("IWeatherRepository -> Implementation")
    # etc.
```

Cette approche avec `injector` rend votre code plus maintenable, testable et flexible ! 🎉
