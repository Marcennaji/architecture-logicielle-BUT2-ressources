# TD4a — API REST avec FastAPI (tag: TD4a)

**Objectif** : Créer une API REST pour exposer votre application ticketing et comprendre le rôle du *composition root*.

---

## 🎯 Objectifs pédagogiques

À la fin de ce TD, vous serez capable de :

1. ✅ Comprendre le rôle du **composition root** (assemblage des dépendances)
2. ✅ Créer des **routes HTTP** avec FastAPI (GET, POST)
3. ✅ Définir des **schémas Pydantic** pour la validation des données
4. ✅ Câbler l'API avec vos **use cases** existants
5. ✅ Tester votre API avec **TestClient** (tests E2E)

---

## 🌐 Contexte : API REST et FastAPI

### Qu'est-ce qu'une API REST ?

Une **API REST** (Representational State Transfer) permet à des applications de communiquer via HTTP. Elle expose des **ressources** (tickets, utilisateurs...) accessibles par des **endpoints** (URLs) et manipulables avec des **verbes HTTP** :
- **GET** : Lire des données (`GET /tickets` → liste des tickets)
- **POST** : Créer une ressource (`POST /tickets` → créer un ticket)
- **PUT/PATCH** : Modifier une ressource
- **DELETE** : Supprimer une ressource

**Exemple** : Une application web (frontend) peut consommer votre API pour afficher et gérer des tickets, sans connaître votre base de données ni votre logique métier.

### Pourquoi FastAPI ?

**FastAPI** est un framework Python moderne pour créer des APIs. Ses atouts :
- ✅ **Validation automatique** : Pydantic vérifie les données entrantes/sortantes
- ✅ **Documentation auto-générée** : Swagger UI (`/docs`) et ReDoc (`/redoc`)
- ✅ **Performance** : Basé sur Starlette (async) et comparable à Node.js/Go
- ✅ **Type hints natifs** : Exploitation maximale des annotations Python

**Dans ce TD**, FastAPI sert d'**adaptateur d'entrée** : il reçoit les requêtes HTTP et appelle vos use cases (votre logique métier reste indépendante du framework).

---

## 📚 Rappel : Architecture hexagonale complète

Jusqu'à présent, vous avez construit :

```
✅ DOMAIN       → Entités (Ticket, User, Status...)
✅ PORTS        → Interfaces (TicketRepository, UserRepository)
✅ ADAPTERS(DB) → Implémentations (SQLite, InMemory)
✅ APPLICATION  → Use Cases (CreateTicket, AssignTicket...)
❌ ADAPTERS(API)→ Routes HTTP (à faire aujourd'hui !)
❌ COMPOSITION ROOT → Assemblage (à faire aujourd'hui !)
```

**Aujourd'hui**, vous complétez l'architecture avec :
- Les **routes HTTP** (adaptateur API)
- Le **composition root** (point d'assemblage)

---

## 🧩 Partie 1 : Comprendre le composition root 

Le **composition root** (`src/main.py`) est le seul endroit qui :
1. Connaît les implémentations concrètes (`SQLiteTicketRepository`, `InMemoryTicketRepository`...)
2. Instancie les adaptateurs
3. Injecte les dépendances dans les use cases

**Principe** :
```python
# ✅ Use case = reçoit les interfaces (ses dépendances)
class CreateTicketUseCase:
    def __init__(self, ticket_repository: TicketRepository, clock: Clock):
        self.repo = ticket_repository
        self.clock = clock

# ✅ Composition root = câble les implémentations concrètes
repo = SQLiteTicketRepository()
clock = SystemClock()
usecase = CreateTicketUseCase(ticket_repository=repo, clock=clock)
```

**👀 Regardez `src/main.py`** : repository instancié, clock instancié, factories pour les use cases (qui injectent toutes les dépendances nécessaires), routes incluses.

---

💡 **Point clé : Deux types d'adaptateurs**

Vous avez remarqué que `ticket_router.py` (API) n'implémente aucun port, contrairement à `SQLiteTicketRepository` qui implémente `TicketRepository`. C'est normal !

- **Adaptateurs de sortie** (DB, services externes) : Implémentent des ports définis par l'application
- **Adaptateurs d'entrée** (API, CLI) : Appellent directement les use cases

Les use cases sont déjà l'interface publique de votre application. Pas besoin de port supplémentaire !

---

## 🚀 Partie 2 : Lancer l'API et premier test 

### Étape 1 : Lancer le serveur

```bash
uvicorn src.main:app --reload
```

**Explications** :
- `src.main:app` → Module Python `src.main`, objet `app`
- `--reload` → Redémarre automatiquement quand le code change

Vous devriez voir :
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### Étape 2 : Tester la route racine

Ouvrez un autre terminal (laissez uvicorn tourner) et testez :

```bash
curl http://127.0.0.1:8000/
```

Réponse : `{"status":"ok"}` ✅

### Étape 3 : Documentation automatique

🌐 Ouvrez **http://127.0.0.1:8000/docs** (Swagger UI) → Documentation interactive avec `GET /`, `POST /tickets`, `GET /tickets`

💡 **Quand est-elle générée ?** FastAPI crée automatiquement cette documentation **au démarrage du serveur**, en analysant vos routes, type hints et schémas Pydantic. Avec `--reload`, elle se met à jour à chaque modification du code. Aucun fichier à écrire manuellement !

💡 **Lire Swagger correctement** : Dans la section "Responses", vous voyez TOUS les codes possibles (201, 422...). Quand vous testez une requête, seul le code correspondant à votre résultat est la vraie réponse. Les autres sont des exemples "si ça se passe mal".

🔍 **Alternative** : **http://127.0.0.1:8000/redoc** (ReDoc) offre une présentation plus claire de la documentation.

💡 **Astuce débogage** : Si vous obtenez une erreur 500, consultez la console où uvicorn tourne. Les exceptions Python complètes y sont affichées.

---

## 📝 Partie 3 : Schémas Pydantic 

**Fichier** : `src/adapters/api/ticket_router.py` (lignes 16-40)

Les schémas `TicketIn` et `TicketOut` sont déjà fournis. Ils définissent :
- **Entrée** : `title`, `description`, `creator_id` (ce que l'API reçoit)
- **Sortie** : `id`, `title`, `description`, `status` (ce que l'API retourne)

**💡 Point clé** : Schémas API ≠ entités domaine. La route convertit `Status.OPEN` (enum) → `"OPEN"` (string)

**💡 Note** : En production, `creator_id` viendrait d'un système d'authentification (JWT, session...). Pour simplifier le TD, on le passe dans la requête.

---

## 🔌 Partie 4 : Implémenter POST /tickets 

### Étape 1 : Comprendre le squelette

**Fichier** : `src/adapters/api/ticket_router.py`, fonction `create_ticket`

La route a :
- `@router.post("/")` → POST sur `/tickets/`
- `status_code=201` → HTTP Created
- `response_model=TicketOut` → Validation de sortie
- `ticket_data: TicketIn` → Validation d'entrée

### Étape 2 : Implémenter

Remplacez le `return TicketOut(id="TODO"...)` par :

```python
# 1. Récupérer le use case depuis le composition root
from src.main import get_create_ticket_usecase

usecase = get_create_ticket_usecase()

# 2. Appeler le use case
ticket = usecase.execute(
    title=ticket_data.title,
    description=ticket_data.description,
    creator_id=ticket_data.creator_id
)

# 3. Convertir l'entité domaine en schéma API
return TicketOut(
    id=ticket.id,
    title=ticket.title,
    description=ticket.description,
    status=ticket.status.value  # Enum → string
)
```

### Étape 3 : Tester l'API

🌐 Ouvrez http://127.0.0.1:8000/docs et testez avec l'interface Swagger :
1. Cliquez sur `POST /tickets` → "Try it out"
2. Modifiez le JSON : `{"title": "Bug urgent", "description": "Le serveur ne répond plus", "creator_id": "user-123"}`
3. Cliquez "Execute"
4. Vérifiez la réponse HTTP 201 avec le ticket créé

✅ **Votre première route POST fonctionne !**

---

## 📋 Partie 5 : Implémenter GET /tickets 

### Étape 1 : Créer le use case ListTickets

**Fichier** : `src/application/usecases/list_tickets.py` (à créer)

```python
"""Use case : Lister tous les tickets."""

from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class ListTicketsUseCase:
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository
    
    def execute(self) -> list[Ticket]:
        return self.ticket_repository.list_all()
```

### Étape 2 : Ajouter la factory dans main.py

**Fichier** : `src/main.py`

**Import** (en haut) :
```python
from src.application.usecases.list_tickets import ListTicketsUseCase
```

**Factory** (après `get_create_ticket_usecase()`) :
```python
def get_list_tickets_usecase() -> ListTicketsUseCase:
    return ListTicketsUseCase(ticket_repository)
```

### Étape 3 : Implémenter la route GET

**Fichier** : `src/adapters/api/ticket_router.py`

**Route** (remplacer la fonction `list_tickets`) :
```python
@router.get("/", response_model=list[TicketOut])
async def list_tickets():
    from src.main import get_list_tickets_usecase
    
    usecase = get_list_tickets_usecase()
    tickets = usecase.execute()
    
    return [
        TicketOut(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status.value
        )
        for ticket in tickets
    ]
```

### Étape 4 : Tester

🌐 Dans Swagger (http://127.0.0.1:8000/docs) :
1. Créez 2-3 tickets avec `POST /tickets`
2. Testez `GET /tickets` → Vous devez voir la liste de vos tickets

✅ **Vous avez maintenant une API REST complète !**

---

## 🧪 Partie 6 : Tests E2E

**Fichier** : `tests/e2e/test_api.py`

Décommentez les tests dans `TestTicketAPI` et complétez-les pour tester vos routes.

```bash
pytest tests/e2e/ -v
```

---

## 🎓 Synthèse

Vous avez complété l'architecture hexagonale :
- **Composition root** (`main.py`) : Câble les dépendances
- **Routes API** (`ticket_router.py`) : POST et GET /tickets
- **Schémas Pydantic** : Validation entrée/sortie
- **Tests E2E** : Validation complète de la stack

---

## 🚀 Bonus : Démonstration de l'architecture hexagonale

### Changer de repository en 3 lignes

**Fichier** : `src/main.py`

Remplacez `InMemoryTicketRepository()` par :
```python
from src.adapters.db.ticket_repository_sqlite import SQLiteTicketRepository
from src.adapters.db.database import get_connection

ticket_repository = SQLiteTicketRepository(get_connection("ticketing.db"))
```

Uvicorn détecte le changement et redémarre automatiquement → **Les tickets sont maintenant persistés en SQLite** ! Aucune ligne de code changée dans les routes ou use cases.

💡 **C'est ça, l'architecture hexagonale** : changer d'infrastructure sans toucher la logique métier.

### Implémenter les routes User (optionnel)

Vous avez créé le `UserRepository` au TD3b. Maintenant, créez l'API `/users` :

1. **Use case** : `CreateUserUseCase` (déjà fait au TD3b)
2. **Factory** : `get_create_user_usecase()` dans `main.py`
3. **Schémas** : `UserIn` et `UserOut` dans un nouveau fichier `user_router.py`
4. **Routes** : `POST /users` et `GET /users`
5. **Tests** : Décommentez les tests dans `test_api.py`

**Objectif** : Reproduire le pattern Ticket pour consolider votre compréhension !

---

## 📌 Finalisation : Commit final et tag Git

```bash
git add .
git commit -m "feat(api): Implement FastAPI routes and composition root"
git tag -a TD4a -m "TD4a: API REST avec FastAPI"
git push origin main --tags
```