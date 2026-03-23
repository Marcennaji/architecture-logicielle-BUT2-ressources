# TD4b — API REST : Gestion d'erreurs (tag: TD4b)

**Objectif** : Améliorer votre API REST avec des routes PATCH et une gestion d'erreurs appropriée.

---

## 🎯 Objectifs pédagogiques

À la fin de ce TD, vous serez capable de :

1. ✅ Implémenter des routes **PATCH** pour modifier des ressources
2. ✅ Gérer les **erreurs HTTP** avec les codes appropriés (404, 400, 422)
3. ✅ Traduire les **exceptions du domaine** en réponses HTTP cohérentes
4. ✅ Utiliser **HTTPException** de FastAPI pour structurer les erreurs
5. ✅ Tester la gestion d'erreurs avec **TestClient**

---

## 🎬 Rappel du contexte

**Avant de commencer** : Prenons 15-20 minutes pour rafraîchir la mémoire.

### Où en êtes-vous dans le projet ?

| Jalon | Contenu | Tag | Statut |
|-------|---------|-----|--------|
| **TD1** | Modélisation domaine (Ticket, User, Status) | `TD1` | ✅ |
| **TD2** | Use cases + ports (CreateTicket, StartTicket) | `TD2` | ✅ |
| **TD3** | Repositories SQLite (persistence) | `TD3` | ✅ |
| **TD4a** | API REST (POST/GET /tickets) | `TD4a` | ✅ |
| **TD4b** | **API REST (PATCH + erreurs)** | `TD4b` | ⏳ **Aujourd'hui** |

### Architecture actuelle

Vous avez construit une architecture hexagonale complète :

```
src/
├── domain/           → Entités (Ticket, User, Status)
├── application/      → Use cases (CreateTicket, StartTicket, ListTickets)
├── ports/           → Interfaces (TicketRepository, UserRepository, Clock)
└── adapters/
    ├── db/          → SQLiteTicketRepository, SQLiteUserRepository
    └── api/         → Routes FastAPI (POST/GET /tickets)
```

**Petit quiz rapide** (réfléchissez, puis cliquez sur les flèches pour afficher les réponses):

<details>
<summary>❓ Où se trouve la logique métier "un ticket ne peut être assigné que s'il est OPEN" ?</summary>

**Réponse** : Dans le **domaine** (`src/domain/ticket.py`), pas dans l'API ni le repository.

💡 **Pourquoi ?** Règle métier = indépendante de l'infrastructure (BDD, API).

</details>

<details>
<summary>❓ Quel rôle joue le fichier `src/main.py` ?</summary>

**Réponse** : C'est le **composition root** qui :
- Instancie les adaptateurs (repository SQLite, clock système)
- Injecte les dépendances dans les use cases
- Configure FastAPI et inclut les routes

💡 **Principe** : C'est le seul fichier qui connaît les implémentations concrètes.

</details>

<details>
<summary>❓ Pourquoi `TicketOut` n'est pas la même classe que `Ticket` ?</summary>

**Réponse** : **Séparation des responsabilités** :
- `Ticket` (domaine) = logique métier (règles, comportements)
- `TicketOut` (API) = schéma de sortie (validation, sérialisation JSON)

💡 **Avantage** : On peut changer l'API sans toucher au domaine (ex: ajouter un champ `created_at` dans l'API sans modifier l'entité).

</details>

---

## 🌐 Partie 1 : Les codes HTTP et la gestion d'erreurs

### Codes HTTP : Rappel rapide

Une API REST communique via des **codes de statut HTTP** :

| Code | Signification | Quand l'utiliser ? |
|------|---------------|-------------------|
| **2xx (Succès)** | | |
| 200 | OK | Requête réussie (GET, PUT) |
| 201 | Created | Ressource créée (POST) |
| 204 | No Content | Succès sans corps de réponse (DELETE) |
| **4xx (Erreur client)** | | |
| 400 | Bad Request | Requête malformée (logique invalide) |
| 404 | Not Found | Ressource inexistante |
| 422 | Unprocessable Entity | Données invalides (validation Pydantic échouée) |
| **5xx (Erreur serveur)** | | |
| 500 | Internal Server Error | Bug/exception non gérée côté serveur |

**💡 Principe REST** : Les codes HTTP portent du sens métier. Un client bien conçu doit pouvoir réagir différemment selon le code reçu.

### Gestion d'erreurs avec FastAPI

FastAPI propose **HTTPException** pour lever des erreurs HTTP :

```python
from fastapi import HTTPException

# Ressource inexistante → 404
raise HTTPException(status_code=404, detail="Ticket not found")

# Opération métier invalide → 400
raise HTTPException(status_code=400, detail="Cannot assign closed ticket")
```

**💡 Différence avec les exceptions Python** :
- `raise ValueError("...")` → Exception Python (500 Internal Server Error si non gérée)
- `raise HTTPException(...)` → Réponse HTTP structurée avec code + message JSON

**Exemple de réponse JSON** quand on lève `HTTPException(404, detail="Ticket not found")` :
```json
{
  "detail": "Ticket not found"
}
```

---

## 🧩 Partie 2 : Traduire les exceptions domaine en codes HTTP

### Le problème

Votre **domaine** lève des exceptions Python quand une règle métier est violée :

```python
# src/domain/ticket.py
def assign(self, user: User):
    if self.status != Status.OPEN:
        raise ValueError("Cannot assign a ticket that is not open")
    self.assigned_to = user
```

Si cette exception remonte jusqu'à FastAPI **sans être interceptée**, le client reçoit :
- **HTTP 500 Internal Server Error** (bug serveur)
- Message d'erreur technique illisible pour un utilisateur

**❌ Problème** : Le client ne peut pas distinguer :
- Une vraie erreur serveur (bug)
- Une erreur métier (règle violée)

### La solution : Intercepter et traduire

**Principe** : L'adaptateur API doit attraper les exceptions (du domaine et de l'application) et les convertir en `HTTPException`.

```python
# src/adapters/api/ticket_router.py

@router.patch("/{ticket_id}/assign")
async def assign_ticket(ticket_id: str, assignment: AssignmentIn):
    try:
        usecase = get_assign_ticket_usecase()
        ticket = usecase.execute(ticket_id=ticket_id, user_id=assignment.user_id)
        return TicketOut(...)
    
    except TicketNotFoundError as e:  # Exception application
        # Traduire en HTTP 404 (Not Found)
        raise HTTPException(status_code=404, detail=str(e))
    
    except ValueError as e:  # Exception domaine
        # Traduire en HTTP 400 (Bad Request)
        raise HTTPException(status_code=400, detail=str(e))
```

**💡 Responsabilités dans l'architecture hexagonale** :
- **Domaine** : Règles métier pures (lève `ValueError`, `InvalidTicketStateError`, etc.)
- **Application** (use cases) : Orchestre le domaine, vérifie l'existence des ressources (lève `TicketNotFoundError`, etc.)
- **Adaptateurs API** : Traduisent exceptions → codes HTTP, convertissent entités domaine → schémas Pydantic

**💡 Séparation des préoccupations** : Le domaine et l'application ne connaissent pas HTTP. Seul l'adaptateur API fait le pont avec le protocole HTTP.

---

## 🔌 Partie 3 : Implémenter les routes PATCH

**🎯 Objectif** : Implémenter deux routes PATCH pour assigner et démarrer des tickets, en gérant correctement les erreurs.

**💡 Stratégie** : Nous allons d'abord implémenter **PATCH /assign**, puis **PATCH /start**, car un ticket doit être assigné avant d'être démarré.

**📝 Note importante sur les IDs utilisateurs** : Dans ce TD, nous utilisons des IDs fictifs ("user-123", "agent-456"). Par choix de simplicité, les use cases ne vérifient pas l'existence de ces utilisateurs en base (via un UserRepository). En production, `AssignTicketUseCase` devrait vérifier que l'agent existe avant l'assignation, et lever une exception appropriée (ex: `UserNotFoundError` → HTTP 404). Cela nous permet de nous concentrer sur la gestion d'erreurs REST sans dépendre d'un système de gestion des utilisateurs.

---

### 📦 Setup préalable : Le use case AssignTicket

**Important** : Le use case `AssignTicket` est nécessaire pour ce TD mais n'a pas forcément été implémenté dans les TDs précédents (c'était un bonus optionnel au TD2).

#### Si vous avez déjà implémenté AssignTicket (bonus TD2) :

✅ **Passez directement à la section 3.1** - Vous êtes déjà prêts !

#### Si vous n'avez PAS encore AssignTicket :

📋 **Copiez le code ci-dessous** pour gagner du temps et vous concentrer sur REST/erreurs (cœur du TD4b).

<details>
<summary><strong>👉 Cliquez ici pour voir le code complet d'AssignTicket à copier-coller</strong></summary>

**Fichier** : `src/application/usecases/assign_ticket.py` (à créer)

```python
"""
Use case : Assigner un ticket à un agent.

Ce use case gère l'assignation d'un ticket existant à un agent.
"""

from src.domain.exceptions import TicketNotFoundError
from src.domain.ticket import Ticket
from src.ports.clock import Clock
from src.ports.ticket_repository import TicketRepository


class AssignTicketUseCase:
    """
    Cas d'usage pour assigner un ticket à un agent.
    """

    def __init__(self, ticket_repo: TicketRepository, clock: Clock):
        """
        Initialise le use case.

        Args:
            ticket_repo: Le repository de tickets
            clock: L'horloge pour obtenir le temps actuel
        """
        self.ticket_repo = ticket_repo
        self.clock = clock

    def execute(self, ticket_id: str, agent_id: str) -> Ticket:
        """
        Assigne un ticket à un agent.

        Args:
            ticket_id: ID du ticket à assigner
            agent_id: ID de l'agent assigné

        Returns:
            Le ticket mis à jour

        Raises:
            TicketNotFoundError: Si le ticket n'existe pas
        """
        # Récupérer le ticket depuis le repository
        ticket = self.ticket_repo.get_by_id(ticket_id)

        # Vérifier que le ticket existe
        if ticket is None:
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")

        # Obtenir le temps actuel
        current_time = self.clock.now()

        # Appeler la méthode métier du domaine
        ticket.assign(agent_id, current_time)

        # Sauvegarder le ticket modifié
        updated_ticket = self.ticket_repo.save(ticket)

        # Retourner le ticket mis à jour
        return updated_ticket
```

**Dans `src/main.py`**, ajoutez :

```python
# Import (avec les autres imports)
from src.application.usecases.assign_ticket import AssignTicketUseCase

# Factory (avec les autres factories)
def get_assign_ticket_usecase() -> AssignTicketUseCase:
    return AssignTicketUseCase(
        ticket_repository=ticket_repository,
        clock=clock
    )
```

**💡 Point clé** : Le use case lève `TicketNotFoundError` (exception de l'application) si le ticket n'existe pas, et laisse remonter les `ValueError` du domaine pour les règles métier (ex: ticket déjà assigné, statut invalide).

</details>

---

### 3.1 — Implémenter PATCH /tickets/{id}/assign

💡 **Prérequis** : Le use case `AssignTicketUseCase` doit exister (voir section Setup ci-dessus).

#### Étape 1 : Créer le schéma Pydantic

**Fichier** : `src/adapters/api/ticket_router.py`

Ajoutez le schéma d'entrée :

```python
class AssignmentIn(BaseModel):
    """Schéma pour assigner un ticket à un agent."""
    agent_id: str
```

💡 **Pourquoi juste `agent_id` ?** Le `ticket_id` est déjà dans l'URL (`/tickets/{ticket_id}/assign`).

#### Étape 2 : Implémenter la route PATCH /assign

**Fichier** : `src/adapters/api/ticket_router.py`

Ajoutez cette nouvelle route :

```python
@router.patch("/{ticket_id}/assign", response_model=TicketOut)
async def assign_ticket(ticket_id: str, assignment: AssignmentIn):
    """
    Assigner un ticket à un agent.

    Args:
        ticket_id: L'identifiant du ticket à assigner
        assignment: Les données d'assignation contenant l'ID de l'agent

    Returns:
        Le ticket assigné

    Raises:
        HTTPException: 404 si le ticket n'existe pas
        HTTPException: 400 si la règle métier est violée
    """
    from src.domain.exceptions import TicketNotFoundError
    from src.main import get_assign_ticket_usecase

    try:
        usecase = get_assign_ticket_usecase()
        ticket = usecase.execute(ticket_id=ticket_id, agent_id=assignment.agent_id)

        return TicketOut(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status.value,
        )
    except TicketNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        # Règles métier violées (ticket déjà assigné, etc.)
        raise HTTPException(status_code=400, detail=str(e)) from e
```

**💡 Explication** :
- On intercepte `TicketNotFoundError` (exception personnalisée) → 404
- On intercepte `ValueError` (exceptions du domaine) → 400
- Le chaînage `from e` préserve la trace complète pour le débogage

#### Étape 3 : Tester PATCH /assign avec Swagger

🌐 Ouvrez **http://127.0.0.1:8000/docs** et testez :

**Scénario 1 : Assignation réussie**

1. Créez un ticket avec `POST /tickets` :
   ```json
   {
     "title": "Bug critique",
     "description": "Le serveur ne répond plus",
     "creator_id": "user-123"
   }
   ```
   → Notez l'`id` retourné (ex: `"ticket-abc"`)

2. Assignez-le avec `PATCH /tickets/{id}/assign` :
   ```json
   {
     "agent_id": "agent-456"
   }
   ```
   → ✅ **HTTP 200 OK** + ticket retourné avec `status: "OPEN"` (toujours ouvert, mais maintenant assigné)

**Scénario 2 : Ticket inexistant (404)**

Testez `PATCH /tickets/ticket-inexistant/assign` :
```json
{
  "agent_id": "agent-456"
}
```
→ ❌ **HTTP 404 Not Found** + `{"detail": "Ticket ticket-inexistant not found"}`

**Scénario 3 : Ticket déjà assigné (400)**

1. Assignez un ticket avec succès
2. Essayez de le réassigner
→ ❌ **HTTP 400 Bad Request** + message d'erreur selon votre domaine

💡 **Astuce** : Si vous obtenez une erreur 500, consultez la console uvicorn pour voir l'exception complète.

---

### 3.2 — Implémenter PATCH /tickets/{id}/start

#### Étape 1 : Rappel du use case StartTicket

💡 **Note** : Ce use case a été obligatoirement implémenté au TD2b. Vous devriez déjà avoir ce code dans votre projet.

<details>
<summary><strong>👉 Cliquez ici pour voir le rappel du code StartTicket (déjà implémenté au TD2b)</strong></summary>

**Fichier** : `src/application/usecases/start_ticket.py`

```python
from src.domain.exceptions import TicketNotFoundError
from src.domain.ticket import Ticket
from src.ports.clock import Clock
from src.ports.ticket_repository import TicketRepository


class StartTicketUseCase:
    """Cas d'usage pour démarrer le traitement d'un ticket."""

    def __init__(self, ticket_repo: TicketRepository, clock: Clock):
        """
        Initialise le use case.

        Args:
            ticket_repo: Le repository de tickets
            clock: L'horloge pour obtenir le temps actuel
        """
        self.ticket_repo = ticket_repo
        self.clock = clock

    def execute(self, ticket_id: str, agent_id: str) -> Ticket:
        """
        Démarre le traitement d'un ticket par un agent.

        Args:
            ticket_id: ID du ticket à démarrer
            agent_id: ID de l'agent qui démarre le ticket

        Returns:
            Le ticket mis à jour

        Raises:
            TicketNotFoundError: Si le ticket n'existe pas
        """
        # 1. Récupérer le ticket depuis le repository
        ticket = self.ticket_repo.get_by_id(ticket_id)
        
        # 2. Vérifier que le ticket existe
        if ticket is None:
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")
        
        # 3. Obtenir le temps actuel
        current_time = self.clock.now()
        
        # 4. Appeler la méthode métier du domaine
        ticket.start(agent_id, current_time)
        
        # 5. Sauvegarder le ticket modifié
        updated_ticket = self.ticket_repo.save(ticket)
        
        # 6. Retourner le ticket mis à jour
        return updated_ticket
```

**💡 Point clé** : Le use case lève `TicketNotFoundError` (exception de l'application) si le ticket n'existe pas, et laisse remonter les `ValueError` du domaine pour les règles métier (ex: ticket non assigné, mauvais agent, statut invalide).

</details>

---

#### Étape 2 : Vérifier la factory dans main.py

**Fichier** : `src/main.py`

💡 **Note** : Si vous avez bien suivi les TDs précédents, vous devriez déjà avoir cette factory. Vérifiez qu'elle existe :

**Import** (doit déjà être présent) :
```python
from src.application.usecases.start_ticket import StartTicketUseCase
```

**Factory** (doit déjà exister) :
```python
def get_start_ticket_usecase() -> StartTicketUseCase:
    return StartTicketUseCase(
        ticket_repository=ticket_repository,
        clock=clock
    )
```

💡 **Si cette factory n'existe pas**, créez-la maintenant.

#### Étape 3 : Créer le schéma Pydantic

**Fichier** : `src/adapters/api/ticket_router.py`

Ajoutez le schéma d'entrée pour démarrer un ticket :

```python
class StartTicketIn(BaseModel):
    """Schéma pour démarrer le traitement d'un ticket."""
    agent_id: str
```

💡 Le `ticket_id` est déjà dans l'URL (`/tickets/{ticket_id}/start`).

#### Étape 4 : Implémenter la route PATCH /start

**Fichier** : `src/adapters/api/ticket_router.py`

Ajoutez cette nouvelle route :

```python
@router.patch("/{ticket_id}/start", response_model=TicketOut)
async def start_ticket(ticket_id: str, data: StartTicketIn):
    """
    Démarrer le traitement d'un ticket.

    Args:
        ticket_id: L'identifiant du ticket à démarrer
        data: Les données contenant l'ID de l'agent qui démarre le ticket

    Returns:
        Le ticket démarré avec le statut IN_PROGRESS

    Raises:
        HTTPException: 404 si le ticket n'existe pas
        HTTPException: 400 si la règle métier est violée (ticket non assigné,
                       mauvais agent, ticket pas en statut OPEN)
    """
    from src.domain.exceptions import TicketNotFoundError
    from src.main import get_start_ticket_usecase

    try:
        usecase = get_start_ticket_usecase()
        ticket = usecase.execute(ticket_id=ticket_id, agent_id=data.agent_id)

        return TicketOut(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status.value,  # Devrait être "in_progress"
        )
    except TicketNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        # Règles métier violées (ticket non assigné, mauvais agent, statut invalide)
        raise HTTPException(status_code=400, detail=str(e)) from e
```

**💡 Explication du code** :

1. **`@router.patch("/{ticket_id}/start")`** : Définit une route PATCH sur `/tickets/{ticket_id}/start`
2. **`ticket_id: str`** : Paramètre d'URL (path parameter)
3. **`data: StartTicketIn`** : Corps de la requête (body), validé par Pydantic
4. **`try/except`** : Intercepte les exceptions et les traduit en codes HTTP
   - `TicketNotFoundError` → 404 Not Found
   - `ValueError` → 400 Bad Request (ticket non assigné, mauvais agent, statut invalide)
5. **`from e`** : Chaînage d'exceptions pour traçabilité (requis par les linters)

#### Étape 5 : Tester le workflow complet avec Swagger

🌐 Ouvrez **http://127.0.0.1:8000/docs** et testez le **scénario complet** :

**Scénario 1 : Workflow complet Créer → Assigner → Démarrer**

1. **Créez** un ticket avec `POST /tickets` :
   ```json
   {
     "title": "Bug critique",
     "description": "Le serveur ne répond plus",
     "creator_id": "user-123"
   }
   ```
   → Notez l'`id` retourné (ex: `"ticket-abc"`)

2. **Assignez-le** avec `PATCH /tickets/{id}/assign` :
   ```json
   {
     "agent_id": "agent-456"
   }
   ```
   → ✅ **HTTP 200 OK** + `status: "OPEN"`

3. **Démarrez-le** avec `PATCH /tickets/{id}/start` :
   ```json
   {
     "agent_id": "agent-456"
   }
   ```
   → ✅ **HTTP 200 OK** + `status: "IN_PROGRESS"`

**Scénario 2 : Ticket inexistant (404)**

Testez `PATCH /tickets/ticket-inexistant/start` :
```json
{
  "agent_id": "agent-456"
}
```
→ ❌ **HTTP 404 Not Found**

**Scénario 3 : Règles métier violées (400)**

**3a. Ticket non assigné** :
1. Créez un ticket (sans l'assigner)
2. Essayez de le démarrer directement
→ ❌ **HTTP 400 Bad Request** + `{"detail": "...unassigned..."}`

**3b. Mauvais agent** :
1. Créez et assignez un ticket à `agent-456`
2. Essayez de le démarrer avec `agent-789`
→ ❌ **HTTP 400 Bad Request** + message indiquant le mauvais agent

**3c. Ticket déjà démarré** :
1. Démarrez un ticket avec succès
2. Essayez de le démarrer à nouveau
→ ❌ **HTTP 400 Bad Request** + message sur le statut invalide

💡 **Astuce débogage** : Si vous obtenez une erreur 500, consultez la console où uvicorn tourne. Les exceptions Python complètes y sont affichées.

---

## 📋 Partie 4 : Autres cas d'erreur

### Validation Pydantic → HTTP 422

FastAPI gère automatiquement les erreurs de validation :

**Exemple** : Si vous envoyez un corps de requête invalide à `PATCH /tickets/{id}/start` :
```json
{
  "agent_id": 123
}
```

Pydantic attend une **string**, pas un **int**.

→ **HTTP 422 Unprocessable Entity** avec un message détaillé :
```json
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["body", "user_id"],
      "msg": "Input should be a valid string",
      "input": 123
    }
  ]
}
```

💡 **Vous n'avez rien à coder** : Pydantic et FastAPI gèrent automatiquement la validation et retournent 422.

### Gérer les erreurs globalement (optionnel)

Si vous voulez éviter de répéter les `try/except` dans chaque route, vous pouvez créer un **gestionnaire d'exception global** :

**Fichier** : `src/main.py`

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Convertir toutes les ValueError en HTTP 400."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

@app.exception_handler(KeyError)
async def key_error_handler(request: Request, exc: KeyError):
    """Convertir toutes les KeyError en HTTP 404."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )
```

**💡 Avantage** : Vos routes deviennent plus simples (pas de `try/except` partout).

**⚠️ Inconvénient** : Toutes les `ValueError` sont traduites en 400, même si certaines devraient être des 500. À utiliser avec discernement.

---

## 🧪 Partie 5 : Tester la gestion d'erreurs

### Étape 1 : Comprendre TestClient

**TestClient** de FastAPI permet de tester votre API **sans lancer le serveur** :

```python
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Faire une requête
response = client.get("/tickets")

# Vérifier le code de statut
assert response.status_code == 200

# Vérifier le corps de la réponse
data = response.json()
assert isinstance(data, list)
```

💡 **Avantage** : Tests rapides, isolation complète, pas besoin de `uvicorn`.

### Étape 2 : Créer les tests de la route PATCH

**Fichier** : `tests/e2e/test_api.py`

Ajoutez ces tests :

```python
class TestStartTicket:
    """Tests de la route PATCH /tickets/{id}/start"""
    
    def test_start_ticket_success(self, client: TestClient):
        """Démarrer un ticket assigné doit retourner 200."""
        # ARRANGE : Créer et assigner un ticket
        # Note: Vous devrez adapter selon votre implémentation
        # Option 1: Si vous avez PATCH /assign, utilisez-la
        # Option 2: Modifiez CreateTicket pour créer un ticket déjà assigné
        ticket_data = {
            "title": "Bug critique",
            "description": "Le serveur crash",
            "creator_id": "user-123",
            "assigned_to": "agent-456"  # Si votre CreateTicket supporte ce champ
        }
        create_response = client.post("/tickets/", json=ticket_data)
        assert create_response.status_code == 201
        ticket_id = create_response.json()["id"]
        
        # ACT : Démarrer le ticket
        start_data = {"agent_id": "agent-456"}
        response = client.patch(f"/tickets/{ticket_id}/start", json=start_data)
        
        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ticket_id
        assert data["status"] == "IN_PROGRESS"
    
    def test_start_nonexistent_ticket_returns_404(self, client: TestClient):
        """Démarrer un ticket inexistant doit retourner 404."""
        # ACT
        start_data = {"agent_id": "agent-456"}
        response = client.patch("/tickets/ticket-inexistant/start", json=start_data)
        
        # ASSERT
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_start_unassigned_ticket_returns_400(self, client: TestClient):
        """Démarrer un ticket non assigné doit retourner 400."""
        # ARRANGE : Créer un ticket NON assigné
        ticket_data = {
            "title": "Bug critique",
            "description": "Le serveur crash",
            "creator_id": "user-123"
        }
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]
        
        # ACT : Essayer de démarrer sans assignation
        start_data = {"agent_id": "agent-456"}
        response = client.patch(f"/tickets/{ticket_id}/start", json=start_data)
        
        # ASSERT
        assert response.status_code == 400
        assert "assigned" in response.json()["detail"].lower()
    
    def test_start_with_wrong_agent_returns_400(self, client: TestClient):
        """Démarrer avec un agent différent de celui assigné doit retourner 400."""
        # ARRANGE : Créer un ticket assigné à agent-456
        ticket_data = {
            "title": "Bug critique",
            "description": "Le serveur crash",
            "creator_id": "user-123",
            "assigned_to": "agent-456"
        }
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]
        
        # ACT : Démarrer avec un autre agent
        start_data = {"agent_id": "agent-789"}  # Mauvais agent
        response = client.patch(f"/tickets/{ticket_id}/start", json=start_data)
        
        # ASSERT
        assert response.status_code == 400
        assert "agent" in response.json()["detail"].lower()
    
    def test_start_with_invalid_data_returns_422(self, client: TestClient):
        """Envoyer des données invalides doit retourner 422."""
        # ARRANGE : Créer un ticket assigné
        ticket_data = {
            "title": "Bug critique",
            "description": "Le serveur crash",
            "creator_id": "user-123",
            "assigned_to": "agent-456"
        }
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]
        
        # ACT : Envoyer un agent_id de type invalide
        start_data = {"agent_id": 123}  # int au lieu de string
        response = client.patch(f"/tickets/{ticket_id}/start", json=start_data)
        
        # ASSERT
        assert response.status_code == 422
```

### Étape 3 : Lancer les tests

```bash
pytest tests/e2e/test_api.py::TestStartTicket -v
```

✅ **Vérification** : Tous les tests doivent passer.

---

## 🎓 Synthèse

Vous avez appris à :

1. ✅ **Traduire les exceptions domaine en codes HTTP** appropriés (404, 400)
2. ✅ **Implémenter une route PATCH** pour modifier une ressource
3. ✅ **Utiliser HTTPException** pour lever des erreurs structurées
4. ✅ **Tester la gestion d'erreurs** avec TestClient

**💡 Principe clé** : L'adaptateur API fait le pont entre le protocole HTTP et votre logique métier. Il traduit :
- Requêtes HTTP → appels de use cases
- Exceptions domaine → codes HTTP + messages JSON

---

## 📌 Finalisation : Commit final et tag Git

```bash
git add .
git commit -m "feat(api): Add PATCH /tickets/{id}/start with error handling"
git tag -a TD4b -m "TD4b: API REST - Gestion d'erreurs"
git push origin main --tags
```

---

## 📖 Ressources complémentaires

- [Documentation FastAPI - Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [HTTP Status Codes - Mozilla MDN](https://developer.mozilla.org/fr/docs/Web/HTTP/Status)
- [REST API Best Practices - Microsoft](https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design)
