# WEB app learning project
Page about the presentation of this learning application to simple efficient web dev

This repo is an exemple of how to build simple efficient web app. The following methodology can be applied to any language for client-server app.

## Methodology

[[picture of the metodology - in comming ...]]

## Injection de dépendances
### 💡 Qu’est-ce qu’une dépendance ?
Une dépendance, c’est simplement un objet dont une autre partie de ton code a besoin pour fonctionner.

Par exemple :

```python
class UserService:
   def __init__(self, db: Database):
        self.db = db
```

Ici, UserService dépend de Database. Il ne peut pas fonctionner sans.

### 🛠️ Le problème sans injection
Dans une approche naïve, tu instancies manuellement les dépendances :

```python 
    db = Database()
    user_service = UserService(db)
```
C’est simple, mais :

- Tu cables fort tes classes entre elles.
- Tu perds en testabilité (pas facile de "faker" la base).
- Tu perds en modularité (difficile de remplacer la base ou de réutiliser le service ailleurs).
- Tu dois manuellement orchestrer la construction des objets.

### ✅ L’injection de dépendances : la solution
L'injection de dépendances, c’est un design pattern qui consiste à externaliser la création des dépendances et à les injecter automatiquement là où elles sont nécessaires, sans que les classes les instancient elles-mêmes.

Il y a trois formes classiques d’injection :

- Par constructeur (le plus courant en Python)
- Par méthode
- Par propriété (moins courant en Python)

[The Clean Code Talks - Don’t Look For Things! (a talk by Miško Hevery)](https://www.youtube.com/watch?v=RlfLCWKxHJ0)

[Inversion of Control Containers and the Dependency Injection pattern (an article by Martin Fowler)](https://martinfowler.com/articles/injection.html)

### 🧪 Exemple en Python pur avec injection par constructeur
```python
class Database:
    ...

class UserService:
    def __init__(self, db: Database):
        self.db = db
```

Ensuite, avec un injecteur, tu n’as plus besoin d’écrire :

```python
db = Database()
user_service = UserService(db)
```

Tu fais simplement :

```python
injector.get(UserService)
```

Et l’injecteur construit Database pour toi et l’injecte automatiquement dans UserService.

### 🔄 Avantages concrets
#### ✅ Découplage
Tes classes ne savent pas comment leurs dépendances sont construites. Elles se contentent de les utiliser.

#### ✅ Testabilité
Tu peux facilement injecter des fakes, mocks ou mocks inversés :

```python
user_service = UserService(FakeDatabase())
```

#### ✅ Lisibilité et extensibilité
Tu sépares clairement la construction (bootstrapping) du code métier. Ton app est plus modulaire, plus clairement structurée.


## Notes about programming good practices
### Package import
1. Use package Manager
2. For the import always use the global path to the package 
```python
from packageName.path.to.module import function
```
Do not use relative import like:
```python
from ..path.to.module import function
```



## Scripts to launch frontend

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.