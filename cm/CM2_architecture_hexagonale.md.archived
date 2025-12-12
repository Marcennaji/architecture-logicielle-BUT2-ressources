---
marp: true
theme: default
paginate: true
title: CM2 — Architecture hexagonale (Ports & Adapters)
style: |
  section {
    font-family: "Liberation Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #1f1f1f;
  }
  h1, h2, h3 {
    color: #004f9f;
  }
  h1 {
    border-bottom: 2px solid #d0d7de;
    padding-bottom: 0.3em;
  }
  code {
    background: #f6f8fa;
    padding: 0.1em 0.3em;
    border-radius: 3px;
  }
  table {
    font-size: 0.9em;
  }
  pre {
    font-size: 0.75em;
  }
---

# 🛡️ CM2 : Architecture hexagonale (Ports & Adapters)

🎓 BUT Informatique — Ressource R4.01 « Architecture logicielle »  
👨‍🏫 Enseignant·e : _à compléter_  

🛠 Objectif du cours :  
Comprendre les principes de l'**architecture hexagonale** et savoir les appliquer au projet *ticketing*.

---

## 🧩 Plan du CM2

1. Rappel : problèmes des architectures « framework-first »
2. Principes de l'architecture hexagonale
3. Les briques : Domain / Application / Ports / Adapters
4. Exemple concret avec du code Python
5. Stratégie de tests
6. Comparaison avec Clean Architecture et MVC
7. Application au projet ticketing
8. Mini-exercices

---

## 🔄 Rappel du CM1 : les principes fondamentaux

| Principe | Application dans l'hexagonale |
|----------|------------------------------|
| **Cohésion** | Chaque couche a une responsabilité claire |
| **Couplage faible** | Les couches communiquent via des interfaces |
| **Inversion de dépendances** | Le domaine définit les interfaces, la technique les implémente |
| **Séparation des responsabilités** | Métier ≠ Technique ≠ Orchestration |

👉 L'architecture hexagonale est une **application concrète** de ces principes.

---

## 1. Le problème : quand le framework dicte tout

### Code typique "framework-first"

```python
# ❌ Tout est mélangé dans le controller
@app.post("/tickets")
def create_ticket(request: Request, db: Session = Depends(get_db)):
    data = request.json()
    
    # Validation métier dans le controller 😬
    if len(data["title"]) < 3:
        raise HTTPException(400, "Titre trop court")
    
    # Accès direct à la DB 😬
    ticket = TicketModel(title=data["title"], status="open")
    db.add(ticket)
    db.commit()
    
    # Envoi d'email directement ici 😬
    send_email(data["author_email"], "Ticket créé", f"ID: {ticket.id}")
    
    return {"id": ticket.id}
```

---

## 1.1 Pourquoi c'est problématique ?

❌ **Testabilité** : pour tester la règle "titre min 3 caractères", il faut :
- Lancer FastAPI
- Avoir une base de données
- Mocker le serveur email

❌ **Maintenabilité** : changer de framework = tout réécrire

❌ **Lisibilité** : où sont les règles métier ? Dispersées partout.

❌ **Réutilisabilité** : impossible d'utiliser la logique ailleurs (CLI, autre API…)

> **Le métier est prisonnier de la technique.**

---

## 2. L'idée clé de l'architecture hexagonale

> **Le domaine (métier) au centre, la technique à la périphérie.**

Inventée par **Alistair Cockburn** (2005), aussi appelée **Ports & Adapters**.

### Principe fondamental

```text
┌─────────────────────────────────────────────────────────┐
│                    MONDE EXTÉRIEUR                      │
│  (HTTP, CLI, bases de données, emails, APIs externes)   │
└───────────────────────────┬─────────────────────────────┘
                            │
                    ┌───────▼───────┐
                    │   ADAPTERS    │  ← Traducteurs
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │    PORTS      │  ← Interfaces/Contrats
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │   DOMAINE     │  ← Règles métier pures
                    │   (CŒUR)      │     Aucune dépendance technique
                    └───────────────┘
```

---

## 2.1 Pourquoi "hexagonale" ?

Le schéma classique est un hexagone pour montrer les **multiples faces** par lesquelles on peut interagir avec le domaine :

```text
                    ┌─── API REST ───┐
                   /                  \
          ┌── CLI ──┐                  ┌── Tests ──┐
         /           \                /             \
        │             │              │               │
        │             └──────────────┘               │
        │                 DOMAINE                    │
        │             ┌──────────────┐               │
        │             │              │               │
         \           /                \             /
          └── DB ───┘                  └── Email ──┘
                   \                  /
                    └─── Message ───┘
```

👉 Le domaine ne sait pas **qui** l'appelle ni **comment** les données sont stockées.

---

## 2.2 Ports & Adapters : le vocabulaire

| Terme | Définition | Exemple |
|-------|------------|---------|
| **Port** | Interface définissant un besoin | `TicketRepository`, `Notifier` |
| **Adapter** | Implémentation concrète d'un port | `SqlTicketRepository`, `SmtpNotifier` |
| **Port entrant** | Comment on entre dans le domaine | API REST, CLI, Tests |
| **Port sortant** | Ce dont le domaine a besoin | Persistance, Notifications |

---

## 3. Les couches de l'architecture hexagonale

```text
┌────────────────────────────────────────────────────────────┐
│                      ADAPTERS (externe)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ API FastAPI │  │ CLI Typer   │  │ SqlTicketRepository │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
├─────────┼────────────────┼────────────────────┼────────────┤
│         │     PORTS      │                    │            │
│         │  (interfaces)  │                    │            │
│  ┌──────▼──────────────▼─────┐    ┌──────────▼──────────┐ │
│  │     Ports Entrants        │    │   Ports Sortants    │ │
│  │   (Use Case interfaces)   │    │  (Repository, etc.) │ │
│  └───────────┬───────────────┘    └──────────▲──────────┘ │
├──────────────┼───────────────────────────────┼────────────┤
│              │       APPLICATION             │            │
│       ┌──────▼──────────────────────────────┴───┐        │
│       │            Use Cases                     │        │
│       │  (CreateTicket, AssignTicket, etc.)     │        │
│       └─────────────────┬───────────────────────┘        │
├─────────────────────────┼────────────────────────────────┤
│                         │      DOMAIN                     │
│              ┌──────────▼──────────┐                      │
│              │  Entities, Value    │                      │
│              │  Objects, Rules     │                      │
│              └─────────────────────┘                      │
└────────────────────────────────────────────────────────────┘
```

---

## 3.1 La couche DOMAIN (le cœur)

C'est le **cœur** de l'application. Elle contient :

- **Entités** : objets avec une identité (`Ticket`, `User`)
- **Value Objects** : objets définis par leurs valeurs (`TicketStatus`, `Email`)
- **Règles métier** : invariants, validations métier
- **Services de domaine** : logique métier complexe impliquant plusieurs entités

### Règle d'or

> **Le domaine n'importe RIEN de technique.**  
> Pas de FastAPI, SQLAlchemy, JWT, requests, etc.

---

## 3.1 Domain — Exemple de code

```python
# domain/ticket.py
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

@dataclass
class Ticket:
    id: str
    title: str
    description: str
    status: TicketStatus
    author_id: str
    assignee_id: str | None
    created_at: datetime
    
    def assign_to(self, user_id: str) -> None:
        """Règle métier : on ne peut assigner que si le ticket est ouvert."""
        if self.status != TicketStatus.OPEN:
            raise ValueError("Impossible d'assigner un ticket non ouvert")
        self.assignee_id = user_id
        self.status = TicketStatus.IN_PROGRESS
```

---

## 3.1 Domain — Value Objects

```python
# domain/value_objects.py
from dataclasses import dataclass
import re

@dataclass(frozen=True)  # Immutable
class Email:
    value: str
    
    def __post_init__(self):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.value):
            raise ValueError(f"Email invalide: {self.value}")

@dataclass(frozen=True)
class TicketTitle:
    value: str
    
    def __post_init__(self):
        if len(self.value) < 3:
            raise ValueError("Le titre doit faire au moins 3 caractères")
        if len(self.value) > 200:
            raise ValueError("Le titre ne peut pas dépasser 200 caractères")
```

👉 Les règles de validation sont **dans le domaine**, pas dans le controller.

---

## 3.2 Les PORTS (interfaces)

Les ports sont des **interfaces** (en Python : classes abstraites ou Protocols).

### Port sortant : Repository

```python
# domain/ports/ticket_repository.py
from abc import ABC, abstractmethod
from domain.ticket import Ticket

class TicketRepository(ABC):
    """Port de sortie pour la persistance des tickets."""
    
    @abstractmethod
    def save(self, ticket: Ticket) -> None:
        """Sauvegarde un ticket."""
        pass
    
    @abstractmethod
    def find_by_id(self, ticket_id: str) -> Ticket | None:
        """Retrouve un ticket par son ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> list[Ticket]:
        """Retourne tous les tickets."""
        pass
```

---

## 3.2 Ports — Autres exemples

```python
# domain/ports/notifier.py
from abc import ABC, abstractmethod

class Notifier(ABC):
    """Port de sortie pour les notifications."""
    
    @abstractmethod
    def notify(self, recipient: str, subject: str, message: str) -> None:
        pass

# domain/ports/id_generator.py
class IdGenerator(ABC):
    """Port de sortie pour la génération d'identifiants."""
    
    @abstractmethod
    def generate(self) -> str:
        pass
```

👉 Le domaine **définit** ce dont il a besoin, sans savoir comment ce sera fait.

---

## 3.3 La couche APPLICATION (Use Cases)

Les **use cases** orchestrent les interactions :
- Reçoivent une commande (créer un ticket, assigner…)
- Utilisent le domaine (entités, règles)
- Appellent les ports sortants (repository, notifier…)

```python
# application/create_ticket.py
from dataclasses import dataclass
from domain.ticket import Ticket, TicketStatus
from domain.ports.ticket_repository import TicketRepository
from domain.ports.id_generator import IdGenerator
from datetime import datetime

@dataclass
class CreateTicketCommand:
    title: str
    description: str
    author_id: str
```

---

## 3.3 Application — Use Case complet

```python
# application/create_ticket.py (suite)

class CreateTicketUseCase:
    def __init__(
        self, 
        repository: TicketRepository,
        id_generator: IdGenerator
    ):
        self.repository = repository
        self.id_generator = id_generator
    
    def execute(self, command: CreateTicketCommand) -> Ticket:
        # Création de l'entité (les règles sont dans le domaine)
        ticket = Ticket(
            id=self.id_generator.generate(),
            title=command.title,  # La validation peut être dans un Value Object
            description=command.description,
            status=TicketStatus.OPEN,
            author_id=command.author_id,
            assignee_id=None,
            created_at=datetime.now()
        )
        
        # Persistance via le port
        self.repository.save(ticket)
        
        return ticket
```

---

## 3.3 Application — Use Case avec notification

```python
# application/assign_ticket.py
class AssignTicketUseCase:
    def __init__(
        self,
        repository: TicketRepository,
        notifier: Notifier,
        user_repository: UserRepository
    ):
        self.repository = repository
        self.notifier = notifier
        self.user_repository = user_repository
    
    def execute(self, ticket_id: str, assignee_id: str) -> Ticket:
        ticket = self.repository.find_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)
        
        # Règle métier (dans le domaine)
        ticket.assign_to(assignee_id)
        
        self.repository.save(ticket)
        
        # Notification via le port
        user = self.user_repository.find_by_id(assignee_id)
        self.notifier.notify(
            user.email,
            f"Ticket #{ticket_id} assigné",
            f"Le ticket '{ticket.title}' vous a été assigné."
        )
        
        return ticket
```

---

## 3.4 Les ADAPTERS (implémentations)

Les adapters implémentent les ports avec des technologies concrètes.

### Adapter SQL pour le Repository

```python
# adapters/db/sql_ticket_repository.py
from sqlalchemy.orm import Session
from domain.ticket import Ticket, TicketStatus
from domain.ports.ticket_repository import TicketRepository

class SqlTicketRepository(TicketRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, ticket: Ticket) -> None:
        model = TicketModel(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status.value,
            author_id=ticket.author_id,
            assignee_id=ticket.assignee_id,
            created_at=ticket.created_at
        )
        self.session.merge(model)
        self.session.commit()
```

---

## 3.4 Adapters — Suite du Repository SQL

```python
# adapters/db/sql_ticket_repository.py (suite)

    def find_by_id(self, ticket_id: str) -> Ticket | None:
        model = self.session.query(TicketModel).filter_by(id=ticket_id).first()
        if not model:
            return None
        return self._to_domain(model)
    
    def find_all(self) -> list[Ticket]:
        models = self.session.query(TicketModel).all()
        return [self._to_domain(m) for m in models]
    
    def _to_domain(self, model: TicketModel) -> Ticket:
        """Convertit le modèle SQL en entité du domaine."""
        return Ticket(
            id=model.id,
            title=model.title,
            description=model.description,
            status=TicketStatus(model.status),
            author_id=model.author_id,
            assignee_id=model.assignee_id,
            created_at=model.created_at
        )
```

---

## 3.4 Adapters — Notifier Email

```python
# adapters/notifications/smtp_notifier.py
import smtplib
from email.mime.text import MIMEText
from domain.ports.notifier import Notifier

class SmtpNotifier(Notifier):
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    def notify(self, recipient: str, subject: str, message: str) -> None:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = recipient
        
        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
```

---

## 3.4 Adapters — Adapter d'entrée (API REST)

```python
# adapters/api/ticket_router.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from application.create_ticket import CreateTicketCommand, CreateTicketUseCase

router = APIRouter(prefix="/tickets", tags=["tickets"])

class CreateTicketRequest(BaseModel):
    title: str
    description: str
    author_id: str

@router.post("/")
def create_ticket(
    request: CreateTicketRequest,
    use_case: CreateTicketUseCase = Depends(get_create_ticket_use_case)
):
    try:
        command = CreateTicketCommand(
            title=request.title,
            description=request.description,
            author_id=request.author_id
        )
        ticket = use_case.execute(command)
        return {"id": ticket.id, "status": ticket.status.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## 3.5 L'injection de dépendances

Comment assembler tout ça ? Avec l'**injection de dépendances**.

```python
# main.py
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.db.sql_ticket_repository import SqlTicketRepository
from adapters.notifications.smtp_notifier import SmtpNotifier
from adapters.id.uuid_generator import UuidIdGenerator
from application.create_ticket import CreateTicketUseCase

# Configuration
engine = create_engine("sqlite:///tickets.db")
SessionLocal = sessionmaker(bind=engine)

def get_create_ticket_use_case():
    session = SessionLocal()
    return CreateTicketUseCase(
        repository=SqlTicketRepository(session),
        id_generator=UuidIdGenerator()
    )

app = FastAPI()
app.include_router(ticket_router)
```

---

## 4. La puissance : les tests

### Test du domaine (AUCUNE dépendance)

```python
# tests/domain/test_ticket.py
import pytest
from domain.ticket import Ticket, TicketStatus
from datetime import datetime

def test_assign_ticket_when_open():
    ticket = Ticket(
        id="1", title="Bug", description="...", 
        status=TicketStatus.OPEN,
        author_id="user1", assignee_id=None,
        created_at=datetime.now()
    )
    
    ticket.assign_to("user2")
    
    assert ticket.assignee_id == "user2"
    assert ticket.status == TicketStatus.IN_PROGRESS

def test_cannot_assign_closed_ticket():
    ticket = Ticket(
        id="1", title="Bug", description="...",
        status=TicketStatus.CLOSED,  # Déjà fermé
        author_id="user1", assignee_id=None,
        created_at=datetime.now()
    )
    
    with pytest.raises(ValueError):
        ticket.assign_to("user2")
```

---

## 4.1 Tests du Use Case avec Fakes

```python
# tests/application/test_create_ticket.py
from application.create_ticket import CreateTicketUseCase, CreateTicketCommand
from domain.ticket import Ticket

class FakeTicketRepository:
    """Fake : implémentation en mémoire pour les tests."""
    def __init__(self):
        self.tickets: dict[str, Ticket] = {}
    
    def save(self, ticket: Ticket) -> None:
        self.tickets[ticket.id] = ticket
    
    def find_by_id(self, ticket_id: str) -> Ticket | None:
        return self.tickets.get(ticket_id)

class FakeIdGenerator:
    def __init__(self, fixed_id: str = "test-123"):
        self.fixed_id = fixed_id
    
    def generate(self) -> str:
        return self.fixed_id
```

---

## 4.1 Tests du Use Case (suite)

```python
# tests/application/test_create_ticket.py (suite)

def test_create_ticket():
    # Arrange
    repository = FakeTicketRepository()
    id_generator = FakeIdGenerator("ticket-001")
    use_case = CreateTicketUseCase(repository, id_generator)
    
    command = CreateTicketCommand(
        title="Mon premier ticket",
        description="Description détaillée",
        author_id="user-42"
    )
    
    # Act
    ticket = use_case.execute(command)
    
    # Assert
    assert ticket.id == "ticket-001"
    assert ticket.title == "Mon premier ticket"
    assert ticket.status.value == "open"
    assert repository.find_by_id("ticket-001") is not None
```

👉 **Aucun framework, aucune base de données, aucun réseau.** Test instantané !

---

## 4.2 La pyramide de tests

```text
                    ┌───────────────┐
                    │    E2E        │  Peu nombreux
                    │  (optionnel)  │  Lents, fragiles
                    └───────┬───────┘
                            │
                   ┌────────▼────────┐
                   │   Intégration   │  Quelques-uns
                   │  (API + DB)     │  Vérifient l'assemblage
                   └────────┬────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │         Tests Unitaires           │  Nombreux
          │   (Domaine + Use Cases + Fakes)   │  Rapides, fiables
          └───────────────────────────────────┘
```

**L'architecture hexagonale permet d'avoir beaucoup de tests unitaires rapides.**

---

## 4.3 Test d'intégration

```python
# tests/integration/test_api_tickets.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_ticket_via_api():
    response = client.post("/tickets/", json={
        "title": "Bug critique",
        "description": "L'application plante",
        "author_id": "user-1"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "open"

def test_create_ticket_with_short_title():
    response = client.post("/tickets/", json={
        "title": "AB",  # Trop court
        "description": "...",
        "author_id": "user-1"
    })
    
    assert response.status_code == 400
```

---

## 5. Comparaison avec d'autres architectures

### Hexagonale vs MVC

| Aspect | MVC | Hexagonale |
|--------|-----|------------|
| Focus | Interface utilisateur | Domaine métier |
| Scope | Pattern UI | Architecture complète |
| Testabilité | Moyenne (dépend du framework) | Excellente |
| Où est le métier ? | Dans le Model (souvent gonflé) | Dans le Domain (isolé) |

👉 **MVC et Hexagonale ne sont pas opposés** — on peut avoir une API MVC comme adapter entrant d'une architecture hexagonale.

---

## 5.1 Hexagonale vs Clean Architecture

La **Clean Architecture** (Uncle Bob) est très similaire :

```text
Clean Architecture              Hexagonale
─────────────────              ────────────
Entities                   ≈   Domain
Use Cases                  ≈   Application
Interface Adapters         ≈   Ports
Frameworks & Drivers       ≈   Adapters
```

**Différences subtiles :**
- Clean Architecture insiste sur les "cercles concentriques"
- L'hexagonale met l'accent sur les "ports et adapters"
- En pratique : **très similaires**, même philosophie

---

## 5.2 Hexagonale vs Architecture en couches

| Architecture en couches | Architecture hexagonale |
|-------------------------|-------------------------|
| UI → Service → DAO → DB | Adapter → Port → Domain ← Port ← Adapter |
| Dépendances vers le bas | Dépendances vers le centre |
| Le métier dépend de la DB | La DB dépend du métier |
| Tests difficiles | Tests faciles |

```text
Couches (problème) :              Hexagonale (solution) :
                                  
UI ──────► Service               Adapter ────► Port
              │                                  │
              ▼                                  ▼
           DAO/DB                            DOMAIN
                                                 ▲
Le métier dépend                                 │
de la technique                  Adapter ────► Port
                                  
                                 La technique dépend
                                 du métier
```

---

## 6. Application au projet Ticketing

### Structure du projet

```text
ticketing/
├── src/
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── ticket.py              # Entité Ticket
│   │   ├── user.py                # Entité User
│   │   ├── value_objects.py       # TicketStatus, Email, etc.
│   │   └── ports/
│   │       ├── ticket_repository.py
│   │       ├── user_repository.py
│   │       └── notifier.py
│   ├── application/
│   │   ├── create_ticket.py
│   │   ├── assign_ticket.py
│   │   └── close_ticket.py
│   ├── adapters/
│   │   ├── db/
│   │   │   └── sql_ticket_repository.py
│   │   ├── api/
│   │   │   └── ticket_router.py
│   │   └── notifications/
│   │       └── console_notifier.py
│   └── main.py
└── tests/
    ├── domain/
    ├── application/
    └── integration/
```

---

## 6.1 Les règles métier du projet

Pour le projet ticketing, voici des exemples de règles métier :

1. **Un ticket doit avoir un titre** d'au moins 3 caractères
2. **Un ticket ne peut être assigné** que s'il est "ouvert"
3. **Un ticket ne peut être fermé** que s'il a été résolu
4. **Seul un admin ou l'assigné** peut changer le statut
5. **Une notification est envoyée** quand un ticket est assigné

👉 Ces règles vivent dans le **domaine**, pas dans l'API ou la DB.

---

## 6.2 Flux d'une requête

```text
1. Requête HTTP POST /tickets
         │
         ▼
2. Adapter API (FastAPI) traduit JSON → CreateTicketCommand
         │
         ▼
3. Use Case CreateTicketUseCase.execute(command)
         │
         ├──► Crée l'entité Ticket (règles validées dans le domaine)
         │
         └──► Appelle TicketRepository.save(ticket) [PORT]
                    │
                    ▼
4. Adapter SQL (SqlTicketRepository) persiste en base
         │
         ▼
5. Use Case retourne le Ticket créé
         │
         ▼
6. Adapter API traduit Ticket → JSON Response
         │
         ▼
7. Réponse HTTP 200 {"id": "...", "status": "open"}
```

---

## 7. Mini-exercice 1 : Identifier les couches

> Classez chaque élément dans la bonne couche :

1. `class Ticket` avec une méthode `close()`
2. `class SqlTicketRepository(TicketRepository)`
3. `class CloseTicketUseCase`
4. `@router.post("/tickets/{id}/close")`
5. `class TicketRepository(ABC)`
6. `class TicketStatus(Enum)`

**Couches :** Domain / Application / Port / Adapter

---

## 7.1 Mini-exercice 1 : Réponses

| Élément | Couche |
|---------|--------|
| `class Ticket` avec `close()` | **Domain** (entité + règle métier) |
| `SqlTicketRepository` | **Adapter** (implémentation concrète) |
| `CloseTicketUseCase` | **Application** (orchestration) |
| `@router.post(...)` | **Adapter** (entrée HTTP) |
| `TicketRepository(ABC)` | **Port** (interface) |
| `TicketStatus(Enum)` | **Domain** (value object) |

---

## 7.2 Mini-exercice 2 : Concevoir un port

> **Nouvelle fonctionnalité** : quand un ticket est créé, on veut logger l'événement (pour audit).

**Questions :**
1. Faut-il modifier le domaine ?
2. Quel port créer ?
3. Quels adapters possibles ?
4. Où appeler ce port ?

---

## 7.2 Mini-exercice 2 : Réponse

1. **Domaine** : non, le logging n'est pas une règle métier

2. **Port** :
```python
class AuditLogger(ABC):
    @abstractmethod
    def log(self, event: str, data: dict) -> None:
        pass
```

3. **Adapters possibles** :
   - `ConsoleAuditLogger` (dev)
   - `FileAuditLogger` (fichier)
   - `ElasticsearchAuditLogger` (prod)

4. **Appel dans le Use Case** (Application) :
```python
class CreateTicketUseCase:
    def __init__(self, repository, id_generator, audit_logger):
        ...
    
    def execute(self, command):
        ticket = ...
        self.repository.save(ticket)
        self.audit_logger.log("ticket_created", {"id": ticket.id})
        return ticket
```

---

## 🎯 Récapitulatif du CM2

### Ce que vous devez retenir :

✅ **Principe clé** : le domaine au centre, la technique en périphérie

✅ **Vocabulaire** : Port (interface) vs Adapter (implémentation)

✅ **Couches** : Domain → Application → Ports → Adapters

✅ **Bénéfice principal** : testabilité et indépendance technique

✅ **Application** : structure du projet ticketing

---

## 🎯 Les questions à se poser

Quand vous codez, demandez-vous :

1. **Est-ce une règle métier ?** → Domain
2. **Est-ce une orchestration d'actions ?** → Application (Use Case)
3. **Est-ce une interface/contrat ?** → Port
4. **Est-ce une implémentation technique ?** → Adapter

> **Si vous importez FastAPI ou SQLAlchemy dans le domaine, c'est une erreur.**

---

# 🏁 Fin du CM2

### Prochaines étapes (TD) :

- **TD1** : Modéliser le domaine (Ticket, User, règles)
- **TD2** : Créer les use cases et ports
- **TD3** : Implémenter les adapters (SQLite)
- **TD4** : Connecter l'API REST

📂 Slides et code exemple sur le dépôt GitHub.

❓ Questions ?
