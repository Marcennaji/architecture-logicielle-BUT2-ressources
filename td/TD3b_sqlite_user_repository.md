# TD3b — UserRepository : Répéter le pattern

**⏰ Durée : 2h** | **🏷️ Tag (pour feedback) : `TD3b`** | **📋 Prérequis : TD3a**

---

## 🎯 Objectifs

1. Créer le port `UserRepository`
2. Implémenter un **premier adaptateur simple** (InMemory)
3. Implémenter un **second adaptateur** (SQLite)
4. Constater : **1 port = N adaptateurs interchangeables**

> 💡 **Principe** : On part du simple (InMemory) vers le complexe (SQLite) pour bien comprendre le pattern.

---

## 📦 Code fourni (à télécharger)

**`src/adapters/db/schema.sql`** (à ajouter au fichier existant) :
```sql
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    is_agent INTEGER NOT NULL DEFAULT 0,
    is_admin INTEGER NOT NULL DEFAULT 0
);
```

**`src/adapters/db/mappers.py`** (code fourni - copier-coller et ajouter au fichier existant) :
```python
def user_to_row(user: User) -> dict:
    """
    Convertit une entité User en dictionnaire pour SQLite.
    
    Args:
        user: L'utilisateur à convertir
    
    Returns:
        Dictionnaire avec les colonnes SQL
    """
    return {
        "id": user.id,
        "username": user.username,
        "is_agent": 1 if user.is_agent else 0,
        "is_admin": 1 if user.is_admin else 0,
    }


def row_to_user(row: dict) -> User:
    """
    Convertit une ligne SQL en entité User.
    
    Args:
        row: Dictionnaire représentant une ligne de la table users
    
    Returns:
        L'entité User reconstituée
    """
    return User(
        id=row["id"],
        username=row["username"],
        is_agent=bool(row["is_agent"]),
        is_admin=bool(row["is_admin"]),
    )
```

---

## 📋 Partie 1 : Port UserRepository 

### 🎯 Analyse du domaine

**Ouvrez `src/domain/user.py`** :
- Quels attributs a la classe `User` ?
- Y a-t-il des validations métier ?

### 🎯 Concevoir le Port

Créez `src/ports/user_repository.py` avec le code suivant :

```python
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.user import User

class UserRepository(ABC):
    """
    Port pour la persistance des utilisateurs.
     """
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Sauvegarde un utilisateur (création ou mise à jour)."""
        ...
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Récupère un utilisateur par son ID."""
        ...
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """Recherche un utilisateur par username."""
        ...
    
    @abstractmethod
    def list_all(self) -> list[User]:
        """Retourne tous les utilisateurs."""
        ...
```

---

## 📋 Partie 2 : Premier adaptateur - InMemoryUserRepository (25 min)

### 🎯 Objectif

Créer un **adaptateur simple** en mémoire. Cela permet de :
- Valider rapidement que le port fonctionne
- Avoir un exemple simple avant d'attaquer SQLite
- Tester les use cases sans base de données

### 📝 À faire

Créez `src/adapters/db/user_repository_inmemory.py` en copiant le code fourni ci-dessous :

```python
"""
Adaptateur InMemory pour le repository d'utilisateurs.
"""

from typing import Optional

from src.domain.user import User
from src.ports.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    """Repository en mémoire pour les tests rapides."""

    def __init__(self):
        self._users: dict[str, User] = {}

    def save(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def find_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def list_all(self) -> list[User]:
        return list(self._users.values())

    def clear(self):
        self._users.clear()
```

### 🧪 Test rapide (optionnel)

Créez `tests/application/test_inmemory_user_repo.py` pour valider :

```python
from src.domain.user import User
from src.adapters.db.user_repository_inmemory import InMemoryUserRepository

def test_inmemory_user_repo():
    repo = InMemoryUserRepository()
    user = User(id="u1", username="alice")
    
    repo.save(user)
    retrieved = repo.get_by_id("u1")
    
    assert retrieved is not None
    assert retrieved.username == "alice"
```

> 💡 **Constat** : InMemory implémente `UserRepository` → le port fonctionne !

---

## 📋 Partie 3 : Second adaptateur - SQLiteUserRepository (50 min)

### 🎯 Objectif

Implémenter l'**adaptateur SQLite** pour User, en combinant :
- La **logique métier** d'`InMemoryUserRepository` (que vous venez de créer)
- La **structure SQL** de `SQLiteTicketRepository` (vu en TD3a)

### 📝 À faire

Créez `src/adapters/db/user_repository_sqlite.py` :

**Structure** :
```python
from typing import Optional
from src.ports.user_repository import UserRepository
from src.domain.user import User
from .database import get_connection
from .mappers import user_to_row, row_to_user

class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str = "ticketing.db"):
        self.db_path = db_path
    
    def save(self, user: User) -> User:
        # TODO: INSERT OR REPLACE INTO users
        pass
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        # TODO: SELECT * FROM users WHERE id = ?
        pass
    
    def find_by_username(self, username: str) -> Optional[User]:
        # TODO: SELECT * FROM users WHERE username = ?
        pass
    
    def list_all(self) -> list[User]:
        # TODO: SELECT * FROM users
        pass
```

### 💡 Stratégie

1. **Inspirez-vous d'`InMemoryUserRepository`** pour la logique métier (find_by_username)
2. **Copiez `SQLiteTicketRepository`** pour la structure SQL
3. **Adaptez les noms** : `tickets` → `users`, `ticket_to_row` → `user_to_row`

### 🧪 Tests basiques

**📍 Fixture dans `tests/conftest.py`** (mutualisé) :
```python
@pytest.fixture
def sqlite_user_repo(tmp_path):
    """Crée un UserRepository SQLite avec une base temporaire."""
    db_path = tmp_path / "test_users.db"
    init_database(str(db_path))
    return SQLiteUserRepository(str(db_path))
```

> 💡 **Pourquoi dans `conftest.py` ?** Pour la réutiliser dans tous les tests (use cases, intégration).

Créez `tests/application/test_user_repository_sqlite.py` :

```python
"""
Tests du repository SQLite pour les utilisateurs.

Ces tests vérifient l'adaptateur SQLite en isolation.
"""

from src.domain.user import User


class TestSQLiteUserRepository:
    """Suite de tests pour le SQLiteUserRepository."""

    def test_save_and_retrieve_user(self, sqlite_user_repo):
        """Doit sauvegarder et récupérer un utilisateur."""
        user = User(id="user-1", username="alice", is_agent=True, is_admin=False)
        
        saved = sqlite_user_repo.save(user)
        assert saved.id == "user-1"
        
        retrieved = sqlite_user_repo.get_by_id("user-1")
        assert retrieved is not None
        assert retrieved.username == "alice"
        assert retrieved.is_agent is True

    def test_find_by_username(self, sqlite_user_repo):
        """Doit trouver un utilisateur par username."""
        user = User(id="user-2", username="bob_agent", is_agent=True)
        sqlite_user_repo.save(user)
        
        found = sqlite_user_repo.find_by_username("bob_agent")
        assert found is not None
        assert found.id == "user-2"
        
    def test_find_by_username_returns_none_when_not_found(self, sqlite_user_repo):
        """Doit retourner None si username introuvable."""
        result = sqlite_user_repo.find_by_username("nonexistent")
        assert result is None

    def test_list_all_returns_all_users(self, sqlite_user_repo):
        """Doit lister tous les utilisateurs."""
        user1 = User(id="u1", username="charlie", is_agent=False)
        user2 = User(id="u2", username="diane_admin", is_agent=True, is_admin=True)
        
        sqlite_user_repo.save(user1)
        sqlite_user_repo.save(user2)
        
        all_users = sqlite_user_repo.list_all()
        assert len(all_users) == 2
```

> 📁 **Note** : Les tests sont dans `tests/application/` (cohérent avec `test_sqlite_repository.py` pour tickets).

### ✅ Constat

- [ ] Port `UserRepository` créé
- [ ] **2 adaptateurs** : InMemory (simple) + SQLite (production)
- [ ] Même interface, implémentations différentes → **interchangeabilité**

---

## 📋 Partie 4 : Use case CreateUser 

### 🎯 Créer le use case

Créez `src/application/usecases/create_user.py` :

```python
"""
Use case : Créer un utilisateur.

Ce use case orchestre la création d'un utilisateur en utilisant les entités du domaine
et le port UserRepository, sans dépendre d'une implémentation concrète.
"""

import uuid

from src.domain.user import User
from src.ports.user_repository import UserRepository


class CreateUserUseCase:
    """
    Cas d'usage pour créer un nouvel utilisateur.

    Reçoit le repository via injection de dépendances (principe d'inversion).
    """

    def __init__(self, user_repo: UserRepository):
        """
        Initialise le use case avec ses dépendances.

        Args:
            user_repo: Le repository (via son interface)
        """
        self.user_repo = user_repo

    def execute(self, username: str, is_agent: bool = False, is_admin: bool = False) -> User:
        """
        Exécute la création d'un utilisateur.

        Args:
            username: Nom d'utilisateur
            is_agent: Si l'utilisateur peut gérer des tickets
            is_admin: Si l'utilisateur a les droits admin

        Returns:
            L'utilisateur créé

        Raises:
            ValueError: Si les données sont invalides ou si le username existe déjà
        """
        # Vérifier que le username n'existe pas déjà
        existing_user = self.user_repo.find_by_username(username)
        if existing_user:
            raise ValueError(f"Username '{username}' already exists")

        # Générer un ID unique
        user_id = str(uuid.uuid4())

        # Créer l'entité User (la validation se fait dans __post_init__)
        user = User(
            id=user_id,
            username=username,
            is_agent=is_agent,
            is_admin=is_admin
        )

        # Persister via le repository
        self.user_repo.save(user)

        return user
```
5
### 🧪 Tester le use case

Créez `tests/application/test_create_user.py` :

```python
"""
Tests du use case CreateUser.

Ces tests vérifient que le use case orchestre correctement
le domaine et le repository.
"""

import pytest

from src.adapters.db.user_repository_inmemory import InMemoryUserRepository
from src.application.usecases.create_user import CreateUserUseCase


class TestCreateUserUseCase:
    """Suite de tests pour la création d'utilisateurs."""

    def setup_method(self):
        """Initialise le repository et le use case avant chaque test."""
        self.repo = InMemoryUserRepository()
        self.use_case = CreateUserUseCase(self.repo)

    def test_create_user_success(self):
        """Doit créer un utilisateur avec les bonnes propriétés."""
        username = "alice"
        
        user = self.use_case.execute(username)
        
        assert user.id is not None
        assert user.username == username
        assert user.is_agent is False
        assert user.is_admin is False

    def test_create_agent_user(self):
        """Doit créer un utilisateur agent."""
        user = self.use_case.execute("bob_agent", is_agent=True)
        
        assert user.is_agent is True
        assert user.is_admin is False

    def test_create_user_with_duplicate_username_raises_error(self):
        """Doit lever une erreur si le username existe déjà."""
        username = "duplicate_user"
        self.use_case.execute(username)
        
        with pytest.raises(ValueError, match="already exists"):
            self.use_case.execute(username)
```

> 💡 **Note** : Ces tests utilisent `InMemoryUserRepository` (plus rapide que SQLite pour les use cases).

### ✅ Constat

- [ ] Use case `CreateUser` implémenté
- [ ] Génération d'ID avec `uuid.uuid4()`
- [ ] Injection de dépendances : le use case ne dépend que du port

---

## 📋 Partie 4 : Git & documentation 

### 📝 Documentation

Mettez à jour `docs/architecture/adapters.md` :

```markdown
## UserRepository

**Implémentations disponibles** :
- `InMemoryUserRepository` : Stockage en mémoire (tests)
- `SQLiteUserRepository` : Stockage SQLite (production)

**Méthodes spécifiques** :
- `find_by_username(username)` : Recherche par username
```

### 🎯 Commit

```bash
git add .
git commit -m "feat: add UserRepository (port + SQLite adapter)"
git tag TD3b
git push --tags
```

---

## ✅ Critères de validation

**Architecture**
- [ ] Port `UserRepository` créé dans `ports/`
- [ ] Les adaptateurs `SQLiteUserRepository` et `InMemoryUserRepository` implémentent le port
- [ ] Utilise les helpers fournis (mappers, database)
- [ ] Aucune logique métier dans l'adaptateur

**Implémentation**
- [ ] `save()` fonctionnel
- [ ] `get_by_id()` fonctionnel
- [ ] `find_by_username()` fonctionnel
- [ ] `list_all()` fonctionnel

**Use case**
- [ ] Use case `CreateUser` créé et testé
- [ ] Validation du username unique
- [ ] Génération d'ID automatique
- [ ] Tests du use case passent

**Tests**
- [ ] 3-4 tests du repository SQLite
- [ ] DB temporaire isolée
- [ ] `pytest tests/` → 100% ✅

**Git**
- [ ] Tag `TD3b` créé

---

## 🎓 Bonus (si temps)

**1. Méthode bonus `clear()`** pour les repositories
- Ajouter `clear()` à `SQLiteUserRepository` : `DELETE FROM users`
- Utile pour nettoyer entre les tests

**2. find_agents()** : Filtrer par agents
```python
def find_agents(self) -> list[User]:
    # SELECT * FROM users WHERE is_agent = 1
    pass
```

**3. GetUserByUsernameUseCase** : Use case de recherche
```python
class GetUserByUsernameUseCase:
    def execute(self, username: str) -> Optional[User]:
        return self.user_repo.find_by_username(username)
```

---

**⬅️ Retour : [TD3a](TD3a_sqlite_ticket_repository.md)**
