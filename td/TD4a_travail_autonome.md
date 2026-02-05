# Travail autonome pendant le stage - Implémentation POST /users

**⏰ À réaliser avant le TD4b du 24/03/2026**

---

## 🎯 Objectif

Implémenter la route `POST /users/` pour créer des utilisateurs via l'API REST.

**Pourquoi ?** Le TD4b nécessite de pouvoir créer des utilisateurs (pour tester l'assignation de tickets à des utilisateurs). C'est un **prérequis obligatoire**.

---

## 📋 Ce que vous devez faire

Vous allez reproduire le pattern utilisé pour `POST /tickets/` (fait au TD4a) mais pour les utilisateurs.

### Fichiers à créer/modifier

1. ✅ **Use case** : `src/application/usecases/create_user.py` (déjà fait au TD3b normalement)
2. ✅ **Use case** : `src/application/usecases/list_users.py` (nouveau)
3. 🆕 **Router API** : `src/adapters/api/user_router.py` (nouveau)
4. 🔧 **Main** : Modifier `src/main.py` pour ajouter les factories et le router
5. ✅ **Tests** : `tests/e2e/test_api.py` - ajouter une classe `TestUserAPI`

---

## 📖 Instructions détaillées

### Étape 1 : Vérifier que CreateUserUseCase existe (TD3b)

**Fichier** : `src/application/usecases/create_user.py`

Si ce fichier n'existe pas, vous devez le créer. Sinon, passez à l'étape 2.

**Ce que doit faire ce use case :**
- Recevoir : `username` (string), `is_agent` (bool, optionnel), `is_admin` (bool, optionnel)
- Vérifier que le username n'existe pas déjà (via `user_repo.find_by_username()`)
- Générer un ID unique avec `uuid.uuid4()`
- Créer une entité `User` du domaine
- Sauvegarder avec `user_repo.save(user)`
- Retourner l'utilisateur créé

**💡 Inspirez-vous de** : `src/application/usecases/create_ticket.py`

---

### Étape 2 : Créer le use case ListUsers

**Fichier** : `src/application/usecases/list_users.py`

**Ce que doit faire ce use case :**
- Recevoir le `user_repository` dans `__init__`
- Méthode `execute()` sans paramètre
- Retourner `self.user_repo.list_all()`

**💡 Inspirez-vous de** : `src/application/usecases/list_tickets.py` (quasi identique)

---

### Étape 3 : Créer le router user_router.py

**Fichier** : `src/adapters/api/user_router.py`

C'est le fichier le plus important. Il suit exactement le même pattern que `ticket_router.py`.

#### 3.1 Imports

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
```

#### 3.2 Créer le router

```python
router = APIRouter(prefix="/users", tags=["users"])
```

#### 3.3 Définir les schémas Pydantic

**Schéma d'entrée `UserIn`** :
- Champs : `username` (str), `is_agent` (bool, défaut False), `is_admin` (bool, défaut False)
- Hérite de `BaseModel`

**Schéma de sortie `UserOut`** :
- Champs : `id` (str), `username` (str), `is_agent` (bool), `is_admin` (bool)
- Hérite de `BaseModel`

**💡 Astuce** : Comparez avec `TicketIn` et `TicketOut` dans `ticket_router.py`

#### 3.4 Route POST /users/

```python
@router.post("/", status_code=201, response_model=UserOut)
async def create_user(user_data: UserIn):
```

**Logique de la fonction :**
1. Importer `get_create_user_usecase` depuis `src.main`
2. Appeler `usecase.execute(username=..., is_agent=..., is_admin=...)`
3. Convertir l'entité `User` en `UserOut`
4. Gérer les exceptions :
   - Si `ValueError` → lever `HTTPException(status_code=400, detail=str(e))`

**💡 Structure identique à** : `create_ticket()` dans `ticket_router.py`

#### 3.5 Route GET /users/

```python
@router.get("/", response_model=list[UserOut])
async def list_users():
```

**Logique :**
1. Importer `get_list_users_usecase`
2. Appeler `usecase.execute()`
3. Convertir chaque `User` en `UserOut` avec une list comprehension

**💡 Structure identique à** : `list_tickets()` dans `ticket_router.py`

---

### Étape 4 : Mettre à jour main.py

**Fichier** : `src/main.py`

#### 4.1 Ajouter les imports

En haut du fichier, ajoutez :
```python
from src.adapters.api.user_router import router as user_router
from src.adapters.db.user_repository_sqlite import SQLiteUserRepository
from src.application.usecases.create_user import CreateUserUseCase
from src.application.usecases.list_users import ListUsersUseCase
```

#### 4.2 Instancier le repository

Vous avez déjà instancié un ticket_repository (de type SQLiteTicketRepository) dans le main.py. 
Il vous faut maintenant instancier un user_repository, de type SQLiteUserRepository, utilisant le même nom de database ("ticketing.db").
La database ticketing.db contiendra ainsi la table ticketing et la table user.

#### 4.3 Créer les factories

Après `get_list_tickets_usecase()`, ajoutez deux nouvelles fonctions :

**Factory pour CreateUser :**
```python
def get_create_user_usecase() -> CreateUserUseCase:
    """Factory pour le cas d'usage CreateUser."""
    return CreateUserUseCase(user_repository)
```

**Factory pour ListUsers :**
```python
def get_list_users_usecase() -> ListUsersUseCase:
    """Factory pour le cas d'usage ListUsers."""
    return ListUsersUseCase(user_repository)
```

#### 4.4 Inclure le router

Après `app.include_router(ticket_router)`, ajoutez :
```python
app.include_router(user_router)
```

---

### Étape 5 : Créer les tests E2E

**Fichier** : `tests/e2e/test_api.py`

Ajoutez une nouvelle classe après `TestTicketAPI` :

```python
class TestUserAPI:
    """Tests pour les routes /users."""

    def test_create_user(self):
        """POST /users/ doit créer un utilisateur."""
        # TODO: Implémenter le test
        # 1. Faire un POST sur /users/ avec un JSON contenant username
        # 2. Vérifier status_code == 201
        # 3. Vérifier que le JSON de réponse contient id, username, is_agent, is_admin

    def test_list_users(self):
        """GET /users/ doit retourner la liste des utilisateurs."""
        # TODO: Implémenter le test
        # 1. Faire un GET sur /users/
        # 2. Vérifier status_code == 200
        # 3. Vérifier que la réponse est une liste
```

**💡 Inspirez-vous de** : Les tests de `TestTicketAPI` juste au-dessus

---

## ✅ Vérification

### Tester manuellement avec Swagger

1. Lancer l'API :
   ```bash
   uvicorn src.main:app --reload
   ```

2. Ouvrir http://127.0.0.1:8000/docs

3. Tester `POST /users/` :
   ```json
   {
     "username": "alice",
     "is_agent": false,
     "is_admin": false
   }
   ```
   → Vous devez obtenir un HTTP 201 avec l'utilisateur créé

4. Tester `GET /users/` :
   → Vous devez voir la liste des utilisateurs créés

### Lancer les tests automatiques

```bash
pytest tests/e2e/test_api.py::TestUserAPI -v
```

Tous les tests doivent passer ✅

---

## 💡 Conseils

1. **Procédez par étapes** : Faites un fichier à la fois, testez au fur et à mesure
2. **Copiez le pattern tickets** : La structure est identique, changez juste les noms
3. **Attention aux imports** : Vérifiez que tous les imports sont corrects
4. **Testez avec Swagger d'abord** : C'est plus visuel que les tests automatiques
5. **Lisez les erreurs** : Si ça ne marche pas, lisez l'erreur dans la console uvicorn

---

## ❓ Difficultés ?

Si vous bloquez, contactez-moi **avant le 20/03** par mail en précisant :
- Où vous en êtes (quel fichier, quelle étape)
- L'erreur que vous rencontrez (copier-coller le message d'erreur)
- Ce que vous avez déjà essayé

Je vous débloquerai ou fournirai le code si nécessaire.

---

## 📚 Ressources

- **TD4a** : Relisez le guide, c'est le même pattern
- **Swagger UI** : Documentation interactive de votre API
- **FastAPI docs** : https://fastapi.tiangolo.com/tutorial/first-steps/

Bon courage ! 🚀
