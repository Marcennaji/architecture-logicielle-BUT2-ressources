# TD3a — SQLiteTicketRepository : Le pattern

**⏰ Durée : 2h** | **🏷️ Tag (pour feedback) : `TD3a`** | **📋 Prérequis : TD2a, TD2b validés**

---

## 🎯 Objectifs

1. Remplacer `InMemoryTicketRepository` par `SQLiteTicketRepository`
2. Comprendre l'**interchangeabilité des adaptateurs**
3. Constater que les use cases ne changent **pas**

> 💡 **Focus architecture** : Un adaptateur SQLite, c'est juste une autre implémentation du port !

---

## 📦 Code fourni (à copier-coller)

⚠️ **Important** : Copiez-collez les fichiers suivants dans votre projet. Ne perdez pas de temps à les coder vous-même !

### **Fichier 1 : `src/adapters/db/schema.sql`**

Créez le fichier et copiez ce contenu :

```sql
-- Schéma de la base de données ticketing
-- Base de données SQLite

CREATE TABLE IF NOT EXISTS tickets (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    creator_id TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    assignee_id TEXT,
    project_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    started_at TEXT,
    closed_at TEXT
);
```

### **Fichier 2 : `src/adapters/db/database.py`**

Créez le fichier et copiez ce contenu :

```python
"""
Utilitaires helper pour SQLite.

Ce module fournit des fonctions pour gérer les connexions SQLite,
l'initialisation de la base de données et la création du schéma.
"""

import sqlite3
from pathlib import Path
from typing import Optional


def get_connection(db_path: str = "ticketing.db") -> sqlite3.Connection:
    """
    Obtient une connexion à la base de données SQLite.

    Args:
        db_path: Chemin vers le fichier de base de données

    Returns:
        Connexion SQLite avec Row factory activé
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Active l'accès type dictionnaire aux lignes
    return conn


def init_database(db_path: str = "ticketing.db", schema_path: Optional[str] = None):
    """
    Initialise la base de données en créant les tables depuis schema.sql.

    Args:
        db_path: Chemin vers le fichier de base de données
        schema_path: Chemin vers le fichier schema.sql (optionnel, auto-détecté si non fourni)
    """
    if schema_path is None:
        # Auto-détection de schema.sql dans le même répertoire
        schema_path = Path(__file__).parent / "schema.sql"

    if not Path(schema_path).exists():
        raise FileNotFoundError(f"Fichier schema non trouvé : {schema_path}")

    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Lecture et exécution du schéma
    with open(schema_path, encoding="utf-8") as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)

    conn.commit()
    conn.close()


def close_connection(conn: sqlite3.Connection):
    """
    Ferme une connexion à la base de données.

    Args:
        conn: La connexion à fermer
    """
    if conn:
        conn.close()
```

### **Fichier 3 : `src/adapters/db/mappers.py`**

Créez le fichier et copiez ce contenu :

```python
"""
Mappers pour la conversion entre entités du domaine et lignes de base de données.

Ce module fournit des fonctions pour convertir les entités Ticket vers/depuis
les représentations de lignes SQLite.
"""

from datetime import datetime

from src.domain.priority import Priority
from src.domain.status import Status
from src.domain.ticket import Ticket


def ticket_to_row(ticket: Ticket) -> dict:
    """
    Convertit une entité Ticket du domaine en dictionnaire pour la base de données.

    Args:
        ticket: L'entité ticket à convertir

    Returns:
        Dictionnaire avec les noms de colonnes et valeurs prêts pour insertion SQL
    """
    return {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "creator_id": ticket.creator_id,
        "status": ticket.status.value,
        "priority": ticket.priority.value,
        "assignee_id": ticket.assignee_id,
        "project_id": ticket.project_id,
        "created_at": ticket.created_at.isoformat(),
        "updated_at": ticket.updated_at.isoformat(),
        "started_at": ticket.started_at.isoformat() if ticket.started_at else None,
        "closed_at": ticket.closed_at.isoformat() if ticket.closed_at else None,
    }


def row_to_ticket(row: dict) -> Ticket:
    """
    Convertit une ligne de base de données en entité Ticket du domaine.

    Args:
        row: Dictionnaire représentant une ligne de base de données (avec noms de colonnes comme clés)

    Returns:
        Entité Ticket du domaine
    """
    # Conversion des chaînes datetime
    created_at = datetime.fromisoformat(row["created_at"])
    updated_at = datetime.fromisoformat(row["updated_at"])
    started_at = datetime.fromisoformat(row["started_at"]) if row["started_at"] else None
    closed_at = datetime.fromisoformat(row["closed_at"]) if row["closed_at"] else None

    # Création du ticket sans status (il a une valeur par défaut)
    ticket = Ticket(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        creator_id=row["creator_id"],
        created_at=created_at,
        updated_at=updated_at,
        priority=Priority(row["priority"]),
        assignee_id=row["assignee_id"],
        project_id=row["project_id"],
        started_at=started_at,
        closed_at=closed_at,
    )

    # Restauration du status réel depuis la base de données avec la méthode dédiée
    ticket._restore_status_from_db(Status(row["status"]))

    return ticket
```

### **Fichier 4 : `tests/conftest.py`** (à compléter)

Ajoutez cette fixture à votre fichier `conftest.py` existant (ou créez-le) :

```python
import pytest

from src.adapters.db.database import init_database
from src.adapters.db.ticket_repository_sqlite import SQLiteTicketRepository


@pytest.fixture
def sqlite_ticket_repo(tmp_path):
    """
    Fixture fournissant un repository SQLite de tickets avec une base de données temporaire.

    Crée une base de données fraîche et isolée pour chaque test afin de garantir
    l'indépendance des tests. La base de données est automatiquement nettoyée
    après le test par pytest.

    Args:
        tmp_path: Répertoire temporaire fourni par pytest (auto-nettoyage)

    Returns:
        SQLiteTicketRepository: Instance du repository avec base de données temporaire

    Exemple:
        def test_save_ticket(sqlite_ticket_repo):
            ticket = Ticket(...)
            sqlite_ticket_repo.save(ticket)
            assert sqlite_ticket_repo.get_by_id(ticket.id) is not None
    """
    # Création d'un fichier de base de données dans le répertoire temporaire
    db_path = tmp_path / "test.db"

    # Initialisation de la base de données avec le schéma
    init_database(str(db_path))

    # Création et retour du repository
    repo = SQLiteTicketRepository(str(db_path))
    return repo
    # Pas de nettoyage nécessaire : pytest supprime automatiquement tmp_path après le test
```

---

### ✅ Vérification rapide

Après avoir copié ces 4 fichiers, vérifiez que votre structure est correcte :

```
src/adapters/db/
├── __init__.py          # Vide ou existant
├── database.py          # ✅ Copié
├── mappers.py           # ✅ Copié
└── schema.sql           # ✅ Copié

tests/
└── conftest.py          # ✅ Fixture ajoutée
```

---

## 📋 Partie 1 : Comprendre l'architecture (20 min)

### ✅ Installation des helpers (5 min)

⚠️ **À faire MAINTENANT** : Copiez-collez les 4 fichiers de la section précédente dans votre projet.

**Checklist** :
- [ ] `schema.sql` copié dans `src/adapters/db/`
- [ ] `database.py` copié dans `src/adapters/db/`
- [ ] `mappers.py` copié dans `src/adapters/db/`
- [ ] Fixture ajoutée dans `tests/conftest.py`

### 🤔 Questions de compréhension (15 min)

**Q1.** Ouvrez `InMemoryTicketRepository`. Quelles méthodes implémente-t-il ?

**Q2.** Ouvrez `ports/ticket_repository.py`. Ce sont les mêmes méthodes ?

**Q3.** Si vous remplacez InMemory par SQLite dans un use case, que devez-vous modifier :
- a) Le code du use case ?
- b) Les tests du use case ?
- c) Uniquement l'instanciation du repository ?

**Q4.** Pourquoi les helpers `database.py` et `mappers.py` sont-ils dans `adapters/` et pas dans `domain/` ?

**Q5.** Lisez le code de `database.py` : comment fonctionne `get_connection()` ?

**Q6.** Lisez le code de `mappers.py` : comment `ticket_to_row()` convertit-il les `datetime` et les `Enum` ?

**Q7.** Dans la fixture `sqlite_ticket_repo`, pourquoi utilise-t-on `tmp_path` ? Comment cela garantit l'isolation des tests ?

---

## 📋 Partie 2 : Implémenter SQLiteTicketRepository (50 min)

### 🎯 À faire

Créez `src/adapters/db/ticket_repository_sqlite.py` :

**Structure attendue** :
```python
from src.ports.ticket_repository import TicketRepository
from src.domain.ticket import Ticket
from .database import get_connection
from .mappers import ticket_to_row, row_to_ticket

class SQLiteTicketRepository(TicketRepository):
    def __init__(self, db_path: str = "ticketing.db"):
        self.db_path = db_path
    
    def save(self, ticket: Ticket) -> Ticket:
        # TODO: INSERT OR REPLACE INTO tickets
        # Utilisez ticket_to_row() et get_connection()
        pass
    
    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        # TODO: SELECT * FROM tickets WHERE id = ?
        # Utilisez row_to_ticket()
        pass
    
    def list_all(self) -> list[Ticket]:
        # TODO: SELECT * FROM tickets
        pass
```

### 💡 Indices

<details>
<summary>Hint : save()</summary>

```python
conn = get_connection(self.db_path)
cursor = conn.cursor()
row = ticket_to_row(ticket)
cursor.execute("""
    INSERT OR REPLACE INTO tickets 
    (id, title, description, creator_id, status, priority, 
     assignee_id, project_id, created_at, updated_at, started_at, closed_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", tuple(row.values()))
conn.commit()
close_connection(conn)
return ticket
```

</details>

<details>
<summary>Hint : get_by_id()</summary>

```python
conn = get_connection(self.db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
row = cursor.fetchone()
close_connection(conn)

if row is None:
    return None
    
return row_to_ticket(dict(row))
```

</details>

---

## 📋 Partie 3 : Tests & validation (30 min)

### 🎯 Tests à adapter

Choisissez 2-3 tests existants de `test_create_ticket.py` ou `test_assign_ticket.py`.

**Exemple** :

```python
def test_create_ticket_with_sqlite(sqlite_ticket_repo):
    """Test CreateTicket avec SQLite (au lieu de InMemory)."""
    use_case = CreateTicketUseCase(ticket_repo=sqlite_ticket_repo)
    
    ticket = use_case.execute(
        title="Bug critique",
        description="Le système plante",
        priority=Priority.HIGH
    )
    
    assert ticket.id is not None
    assert ticket.status == Status.OPEN
    
    # Vérifier persistance : récupérer depuis la DB
    retrieved = sqlite_ticket_repo.get_by_id(ticket.id)
    assert retrieved.title == "Bug critique"
```

### ✅ Constats

- [ ] Les use cases n'ont **pas changé** (même code)
- [ ] Les tests ont **la même structure** (seul le repo change)
- [ ] InMemory et SQLite sont **interchangeables**
- [ ] Le port garantit le **contrat** d'interface

---

## 📋 Partie 4 : Réflexion architecturale (10 min)

### 💭 Questions finales

**Q6.** Pourquoi peut-on facilement passer de InMemory à SQLite ?

**Q7.** Si demain vous devez utiliser PostgreSQL, quels fichiers changent ?

**Q8.** Quel est l'avantage d'avoir InMemory **et** SQLite ?

### 📝 Documentation

Mettez à jour `docs/architecture/adapters.md` :

```markdown
## Adaptateurs de persistance

### TicketRepository

**Implémentations disponibles** :
- `InMemoryTicketRepository` : Stockage en mémoire (tests)
- `SQLiteTicketRepository` : Stockage SQLite (production)

**Interchangeabilité** : Les use cases utilisent uniquement le port `TicketRepository`.
Le choix de l'implémentation se fait à l'instanciation (injection de dépendances).
```

---

## ✅ Critères de validation

**Architecture**
- [ ] `SQLiteTicketRepository` implémente `TicketRepository`
- [ ] Utilise les helpers fournis (database.py, mappers.py)
- [ ] Aucune logique métier dans l'adaptateur
- [ ] Les use cases restent inchangés

**Implémentation**
- [ ] `save()` fonctionnel (INSERT OR REPLACE)
- [ ] `get_by_id()` fonctionnel (retourne None si absent)
- [ ] `list_all()` fonctionnel

**Tests**
- [ ] 2-3 tests adaptés pour SQLite
- [ ] Utilisation de la fixture `sqlite_ticket_repo`
- [ ] Tests isolés (DB temporaire par test)
- [ ] `pytest tests/` → 100% ✅

**Git**
- [ ] Commits réguliers en séance
- [ ] Tag `TD3a` poussé

---

## 🎓 Bonus (si temps)

**1. Méthode clear()** : Vider toute la DB
```python
def clear(self):
    """Supprime tous les tickets (utile pour tests)."""
    # DELETE FROM tickets
```

**2. Tests de performance** : Comparer InMemory vs SQLite
- Créer 1000 tickets
- Mesurer temps d'exécution
- Constater : InMemory = rapide, SQLite = persistent

**3. find_by_status()** : Filtrer par statut
```sql
SELECT * FROM tickets WHERE status = ?
```

---

**➡️ Suite : [TD3b](TD3b_sqlite_user_repository.md) - UserRepository**  
**⬅️ Retour : [TD2b](TD2b_adding_horodating.md)**
