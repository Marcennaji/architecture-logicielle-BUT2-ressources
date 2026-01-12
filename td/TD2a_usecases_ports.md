# TD2a — Cas d'usage & ports (architecture hexagonale)

**⏰ Durée : 1 séance de 2h**  
**🏷️ Tag Git optionnel : `TD2a` (pour feedback)**

> ⏳ **Note importante** : Ce TD est dense et introduit de nombreux concepts architecturaux. Il est **normal de ne pas terminer en 2h**. Vous pouvez :
> - Continuer le travail en **autonomie** chez vous
> - Finir lors de la **séance TD2b** (temps prévu en début de séance)
> - Créer le tag `TD2a` quand vous êtes prêts pour obtenir un feedback

---

## 🎯 Objectifs de la séance

Après le TD1 où vous avez créé les **entités du domaine**, nous allons maintenant :

1. **Identifier les cas d'usage** principaux de notre système de ticketing
2. **Créer le composant application** avec 2 use cases de base
3. **Définir un port** (interface) pour la persistance des tickets
4. **Implémenter un adaptateur in-memory** pour tester nos use cases
5. **Écrire des tests** pour valider l'architecture

> 💡 **Point clé** : Ce TD introduit concrètement l'**architecture hexagonale** (ports & adapters).  
> Les use cases ne dépendent **que des interfaces (ports)**, jamais des implémentations concrètes !

---

## 📚 Rappel : Architecture hexagonale

Dans l'architecture hexagonale, nous organisons le code en **composants** avec des **dépendances unidirectionnelles** vers le centre :

```
           ┌──────────────────────────────┐
           │   COMPOSITION ROOT           │  ← Câble tout (main.py)
           │   (Instanciation)            │     Connaît TOUT
           └──┬────────────────────────┬──┘
              │                        │
              │ instancie              │ instancie
              ▼                        ▼
┌─────────────────────────┐    ┌──────────────────┐
│     ADAPTATEURS         │    │   USE CASES      │
│  (API, DB, CLI, etc.)   │    │  (Application)   │
└───────────┬─────────────┘    └────────┬─────────┘
            │                           │
            │                           │ utilisent
            │                           │
            └──────────►┌───────────────▼────┐
  implémentent          │    DOMAINE         │  ← Cœur (indépendant)
  les ports             │  • Entités         │
                        │  • Règles métier   │
                        │  • Ports           │  ← Interfaces (ports) ici !
                        └────────────────────┘
```

**Règles de dépendances** (CRUCIAL) :
- ✅ **USE CASES** dépendent **uniquement des PORTS** (interfaces), **JAMAIS des adaptateurs**
- ✅ **ADAPTATEURS** implémentent les **PORTS** et dépendent du **DOMAINE**
- ✅ **COMPOSITION ROOT** connaît et instancie les adaptateurs ET les use cases (câblage)
- ❌ **DOMAINE** ne dépend de RIEN (ni FastAPI, ni SQLite, ni pytest...)
- 💡 Les **PORTS** sont des interfaces définies dans le domaine (dans `src/ports/`)
- 🔑 **Inversion de dépendances** : les use cases manipulent les adaptateurs via leurs interfaces (ports)

> 📝 **Note** : Le **composition root** (ex: `main.py`) est le seul endroit qui connaît les implémentations concrètes. C'est lui qui instancie les adaptateurs et les injecte dans les use cases. Dans ce TD, nous nous concentrons sur les use cases et les ports. Le composition root sera vu au TD4 (API REST).

---

## 📋 Partie 1 : Lister les cas d'usage

### 🎯 Objectif
Identifier les actions métier principales que notre système doit supporter.

### 📝 À faire

**1.** Réfléchissez aux actions qu'un utilisateur peut effectuer sur un ticket. Par exemple :

- Créer un ticket
- Assigner un ticket à un agent
- Modifier le statut d'un ticket (démarrer, résoudre, clôturer...)
- etc.

**2.** Créez un fichier `docs/usecases.md` dans votre projet et listez **au minimum 6-8 cas d'usage** que vous jugez importants.

**Format suggéré** :

```markdown
# Cas d'usage du système de ticketing

## Use cases principaux

1. **Créer un ticket** : Un utilisateur crée un nouveau ticket avec titre, description
2. **Assigner un ticket** : Un agent assigne un ticket à lui-même ou un autre agent
3. **Démarrer le traitement** : Un agent démarre le travail sur un ticket assigné
4. ...
```

> 💡 **Note** : Dans ce TD, nous n'implémenterons que **2 use cases** pour bien comprendre le principe. Les autres seront ajoutés au TD2b.

---

## 📋 Partie 2 : Créer le port `TicketRepository`

### 🎯 Objectif
Définir l'**interface** (le contrat) que tout système de persistance devra respecter.

### 📚 Qu'est-ce qu'un port ?

Un **port** est une **interface abstraite** qui définit les opérations nécessaires, **sans spécifier comment elles sont implémentées**.

- Le port est défini dans `src/ports/` (fait partie du domaine)
- Il ne contient **que des signatures de méthodes** (pas d'implémentation)
- Les adaptateurs concrets (InMemory, SQLite, PostgreSQL) l'implémenteront et **dépendront** de ce port

### 📝 À faire

**1.** Créez le fichier `src/ports/ticket_repository.py` :

```python
"""
Port (interface) pour la persistance des tickets.

Ce module définit le contrat que tout adaptateur de stockage doit respecter.
Les use cases utilisent cette interface, sans connaître l'implémentation concrète.
"""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.ticket import Ticket


class TicketRepository(ABC):
    """
    Interface abstraite pour la persistance des tickets.
    
    Cette interface définit les opérations de base (CRUD) sur les tickets.
    Les adaptateurs concrets (InMemory, SQLite, etc.) implémenteront ces méthodes.
    """

    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        """
        Sauvegarde un ticket (création ou mise à jour).
        
        Args:
            ticket: Le ticket à sauvegarder
            
        Returns:
            Le ticket sauvegardé (avec éventuellement un ID généré)
        """
        ...

    @abstractmethod
    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son identifiant.
        
        Args:
            ticket_id: L'identifiant unique du ticket
            
        Returns:
            Le ticket trouvé, ou None s'il n'existe pas
        """
        ...

    @abstractmethod
    def list_all(self) -> list[Ticket]:
        """
        Récupère tous les tickets du système.
        
        Returns:
            Liste de tous les tickets (peut être vide)
        """
        ...
```

**2.** Vérifiez que votre classe `Ticket` du TD1 est bien importable et complète.

> 💡 **Note architecturale** : Les ports font **conceptuellement** partie du domaine ! Ils définissent ce dont le domaine a besoin (ses interfaces requises), sans imposer d'implémentation.
> 
> **Pourquoi `src/ports/` et pas `src/domain/ports/` ?**
> - **Conceptuellement** : les ports appartiennent au domaine (ils expriment ses besoins)
> - **Physiquement** : on les sépare dans `src/ports/` pour plus de clarté dans l'organisation du code
> - Cela permet de distinguer visuellement :
>   - `src/domain/` → entités et règles métier pures (Ticket, User, Status...)
>   - `src/ports/` → contrats d'infrastructure (TicketRepository, NotificationService...)
> - C'est une **convention courante** en architecture hexagonale (pas une obligation stricte)
> 
> **Séparation des responsabilités** :
> - Les **entités** (`Ticket`, `User`, `Status`, `Project`...) sont des objets métier purs qui ne s'occupent pas de leur propre persistance
> - Les **ports** (`TicketRepository`) définissent les opérations de persistance nécessaires
> - Les **use cases** dans `application/` orchestrent : ils manipulent les entités ET utilisent les ports
> 
> Concrètement : la classe `Ticket` ne doit pas importer `TicketRepository`, c'est le use case `CreateTicketUseCase` qui importe les deux.

---

## 📋 Partie 3 : Implémenter l'adaptateur InMemory

### 🎯 Objectif
Créer une **implémentation concrète** du port, stockant les tickets en mémoire (dans un dictionnaire).

### 📚 Pourquoi un adaptateur InMemory ?

Avant d'utiliser une vraie base de données (TD3), nous créons un adaptateur simple :
- Stocke les tickets dans un dictionnaire Python `{id: ticket}`
- Facile à tester (pas besoin de base de données)
- Permet de valider que notre architecture fonctionne

### 📝 À faire

**1.** Créez le fichier `src/adapters/db/ticket_repository_inmemory.py` :

```python
"""
Adaptateur InMemory pour le repository de tickets.

Implémentation simple du TicketRepository qui stocke les tickets en mémoire.
Utilisé principalement pour les tests et le développement.
"""

from typing import Optional

from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class InMemoryTicketRepository(TicketRepository):
    """
    Repository en mémoire utilisant un dictionnaire Python.
    
    Les données sont perdues à chaque redémarrage.
    Idéal pour les tests unitaires et l'apprentissage.
    """

    def __init__(self):
        """Initialise le repository avec un dictionnaire vide."""
        self._tickets: dict[str, Ticket] = {}

    def save(self, ticket: Ticket) -> Ticket:
        """
        Sauvegarde un ticket dans le dictionnaire.
        
        Args:
            ticket: Le ticket à sauvegarder
            
        Returns:
            Le ticket sauvegardé
        """
        self._tickets[ticket.id] = ticket
        return ticket

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son ID.
        
        Args:
            ticket_id: L'identifiant du ticket
            
        Returns:
            Le ticket ou None
        """
        return self._tickets.get(ticket_id)

    def list_all(self) -> list[Ticket]:
        """
        Retourne tous les tickets stockés.
        
        Returns:
            Liste de tous les tickets
        """
        return list(self._tickets.values())

    def clear(self):
        """
        Vide le repository (utile pour les tests).
        
        Note: Cette méthode n'est pas dans le port, elle est spécifique
        à l'implémentation InMemory pour faciliter les tests.
        """
        self._tickets.clear()
```

**2.** Créez le fichier `src/adapters/db/__init__.py` si nécessaire (peut être vide).

---

## 📋 Partie 4 : Créer deux use cases

### 🎯 Objectif
Implémenter 2 cas d'usage simples pour comprendre comment orchestrer le domaine et les ports.

> ⚠️ **Important** : Les exemples de code ci-dessous sont **à adapter** selon votre implémentation du domaine (TD1) :
> - Les **noms de méthodes** peuvent différer (ex: `assign()` vs `assign_to()`)
> - Les **noms d'attributs** peuvent différer (ex: `assignee_id` vs `assigned_to`)  
> - L'utilisation de **value objects** ou de types simples dépend de vos choix au TD1
> 
> Adaptez le code en fonction de **votre** modèle de domaine !

### 📝 Use Case 1 : Créer un ticket

**1.** Créez le fichier `src/application/usecases/create_ticket.py` :

```python
"""
Use case : Créer un ticket.

Ce use case orchestre la création d'un ticket en utilisant les entités du domaine
et le port TicketRepository, sans dépendre d'une implémentation concrète.
"""

import uuid

from src.domain.ticket import Ticket
from src.domain.priority import Priority
from src.ports.ticket_repository import TicketRepository


class CreateTicketUseCase:
    """
    Cas d'usage pour créer un nouveau ticket.
    
    Reçoit le repository via injection de dépendances (principe d'inversion).
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le use case avec ses dépendances.
        
        Args:
            ticket_repo: Le repository (via son interface)
        """
        self.ticket_repo = ticket_repo

    def execute(
        self, 
        title: str, 
        description: str, 
        creator_id: str
    ) -> Ticket:
        """
        Exécute la création d'un ticket.
        
        Args:
            title: Titre du ticket
            description: Description du problème
            creator_id: ID de l'utilisateur créateur
            
        Returns:
            Le ticket créé
            
        Raises:
            ValueError: Si les données sont invalides
        """
        # Créer le ticket avec les entités du domaine
        ticket = Ticket(
            id=str(uuid.uuid4()),  # Génère un UUID
            title=title,
            description=description,
            creator_id=creator_id,
            priority=Priority.MEDIUM
        )
        
        # Persister via le port (peu importe l'implémentation !)
        saved_ticket = self.ticket_repo.save(ticket)
        
        return saved_ticket
```

> 💡 **Notez bien** :
> - Le use case reçoit le repository via le constructeur (**injection de dépendances**)
> - Il utilise l'**interface** `TicketRepository`, pas une implémentation concrète
> - Il manipule les **entités du domaine** (`Ticket`, `Priority`, etc.)
> - La logique métier reste dans le domaine, le use case **orchestre**
> - **Adaptez les imports et attributs** selon votre implémentation du TD1

### 📝 Use Case 2 : Assigner un ticket

**2.** Créez le fichier `src/application/usecases/assign_ticket.py` :

À partir de l'exemple du use case précédent, créez maintenant le use case pour assigner un ticket à un agent.

**Spécifications** :
- Reçoit un `ticket_id` et un `agent_id` en paramètres
- Récupère le ticket via le repository
- Lève une exception `TicketNotFoundError` si le ticket n'existe pas
- Utilise la méthode `assign()` du ticket (créée au TD1b)
- Sauvegarde le ticket modifié
- Retourne le ticket mis à jour

**Squelette à compléter** :

```python
"""
Use case : Assigner un ticket à un agent.

Ce use case gère l'assignation d'un ticket existant à un agent.
"""

from src.domain.ticket import Ticket
from src.domain.exceptions import TicketNotFoundError
from src.ports.ticket_repository import TicketRepository


class AssignTicketUseCase:
    """
    Cas d'usage pour assigner un ticket à un agent.
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le use case.
        
        Args:
            ticket_repo: Le repository de tickets
        """
        # TODO: Stocker le repository en attribut

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
        # TODO: Récupérer le ticket depuis le repository
        
        # TODO: Vérifier que le ticket existe (lever TicketNotFoundError sinon)
        
        # TODO: Appeler la méthode assign() du ticket avec agent_id
        
        # TODO: Sauvegarder le ticket modifié
        
        # TODO: Retourner le ticket mis à jour
        pass
```

> 💡 **Aide** : Inspirez-vous du use case `CreateTicket` pour la structure générale !

**3.** N'oubliez pas d'ajouter `TicketNotFoundError` dans `src/domain/exceptions.py` si ce n'est pas déjà fait :

```python
class TicketNotFoundError(Exception):
    """Levée quand un ticket demandé n'existe pas."""
    pass
```

**4.** Assurez-vous que votre classe `Ticket` a une méthode `assign()` (normalement créée au TD1b).

---

## 📋 Partie 5 : Tester les use cases

### 🎯 Objectif
Écrire des tests pour valider que nos use cases fonctionnent correctement.

### 📚 Pourquoi tester les use cases ?

- Valider que l'architecture fonctionne (domaine + ports + adapters)
- Vérifier que l'injection de dépendances fonctionne
- Vérifier l'orchestration entre le domaine et les ports
- Les tests révèlent la qualité de l'architecture !

> 💡 **Note sur les tests** : Ces tests sont des **tests application** (ou tests de use cases). Ils testent l'orchestration entre plusieurs composants (use case + repository + entités) en utilisant des adaptateurs in-memory. Ils sont différents des tests domain (purement unitaires sur les entités) et des tests e2e (via requêtes HTTP). Voir le [guide des tests](guides/comment_tester.md) pour plus de détails.

### 📝 À faire

**1.** Créez le fichier `tests/application/test_create_ticket.py` :

```python
"""
Tests du use case CreateTicket.

Ces tests vérifient que le use case orchestre correctement
le domaine et le repository.
"""

import pytest

from src.application.usecases.create_ticket import CreateTicketUseCase
from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.domain.status import Status


class TestCreateTicketUseCase:
    """Suite de tests pour la création de tickets."""

    def setup_method(self):
        """Initialise le repository et le use case avant chaque test."""
        self.repo = InMemoryTicketRepository()
        self.use_case = CreateTicketUseCase(self.repo)

    def test_create_ticket_success(self):
        """Doit créer un ticket avec les bonnes propriétés."""
        # Arrange
        title = "Bug critique"
        description = "L'application plante au démarrage"
        creator_id = "user-123"

        # Act
        ticket = self.use_case.execute(title, description, creator_id)

        # Assert
        assert ticket.id is not None
        assert ticket.title == title
        assert ticket.description == description
        assert ticket.status == Status.OPEN
        assert ticket.creator_id == creator_id
        assert ticket.assignee_id is None

    def test_create_ticket_persists_in_repository(self):
        """Doit sauvegarder le ticket dans le repository."""
        # Arrange
        title = "Nouvelle fonctionnalité"
        description = "Ajouter un bouton export"
        creator_id = "user-456"

        # Act
        ticket = self.use_case.execute(title, description, creator_id)

        # Assert - Vérifier que le ticket est bien dans le repository
        saved_ticket = self.repo.get_by_id(ticket.id)
        assert saved_ticket is not None
        assert saved_ticket.id == ticket.id
        assert saved_ticket.title == title

    def test_create_multiple_tickets(self):
        """Doit pouvoir créer plusieurs tickets distincts."""
        # Arrange & Act
        ticket1 = self.use_case.execute("Bug 1", "Description 1", "user-1")
        ticket2 = self.use_case.execute("Bug 2", "Description 2", "user-2")

        # Assert
        assert ticket1.id != ticket2.id
        all_tickets = self.repo.list_all()
        assert len(all_tickets) == 2
```

> 💡 **Structure d'un test** :
> - `setup_method()` : initialise le contexte (repository, use case)
> - Chaque test suit le pattern **Arrange / Act / Assert**
> - Les assertions vérifient le comportement attendu

**2.** Créez le fichier `tests/application/test_assign_ticket.py` :

À votre tour ! En vous inspirant des tests de `CreateTicket`, créez les tests pour `AssignTicket`.

**Squelette à compléter** :

```python
"""
Tests du use case AssignTicket.
"""

import pytest

from src.application.usecases.create_ticket import CreateTicketUseCase
from src.application.usecases.assign_ticket import AssignTicketUseCase
from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.domain.exceptions import TicketNotFoundError


class TestAssignTicketUseCase:
    """Suite de tests pour l'assignation de tickets."""

    def setup_method(self):
        """Initialise le repository et les use cases."""
        self.repo = InMemoryTicketRepository()
        self.create_use_case = CreateTicketUseCase(self.repo)
        self.assign_use_case = AssignTicketUseCase(self.repo)

    def test_assign_ticket_success(self):
        """Doit assigner un ticket à un agent."""
        # Arrange - Créer un ticket d'abord
        ticket = self.create_use_case.execute(
            "Bug à corriger",
            "Description du bug",
            "user-123"
        )
        agent_id = "agent-456"

        # Act
        updated_ticket = self.assign_use_case.execute(ticket.id, agent_id)

        # Assert
        assert updated_ticket.assignee_id is not None
        assert updated_ticket.assignee_id == agent_id

    def test_assign_nonexistent_ticket_raises_error(self):
        """Doit lever une erreur si le ticket n'existe pas."""
        # Arrange
        fake_id = "ticket-inexistant"
        agent_id = "agent-789"

        # Act & Assert
        # TODO: Utiliser pytest.raises pour vérifier qu'une TicketNotFoundError est levée
        pass

    def test_assign_ticket_persists_change(self):
        """Doit persister l'assignation dans le repository."""
        # Arrange - Créer un ticket
        # TODO: Créer un ticket avec create_use_case
        
        agent_id = "agent-999"

        # Act
        # TODO: Assigner le ticket à l'agent
        
        # Assert - Récupérer depuis le repo pour vérifier la persistance
        # TODO: Récupérer le ticket depuis le repository
        # TODO: Vérifier que assignee_id n'est pas None
        # TODO: Vérifier que assignee_id correspond à agent_id
        pass
```

> 💡 **Indices** :
> - Pour tester une exception : `with pytest.raises(ExceptionType):`
> - N'oubliez pas de créer un ticket avant de l'assigner !
> - Vérifiez que l'assignation est bien persistée en récupérant le ticket du repository

**3.** Lancez les tests :

```bash
pytest tests/application/ -v
```

> 💡 **Adaptez les tests** selon votre implémentation du domaine (TD1) !  
> Par exemple :
> - Si vous avez utilisé des value objects pour les IDs : `str(ticket.creator_id)` au lieu de `ticket.creator_id`
> - Si votre attribut s'appelle `assigned_to` au lieu de `assignee_id` : adaptez les assertions
> - Si votre ticket a un attribut `status` qui est une propriété : vérifiez comment y accéder

---

## ✅ Points de vérification pour le tag `TD2a` (optionnel)

Le tag `TD2a` est **optionnel** et vous permet d'obtenir un **feedback** sur votre architecture. Si vous souhaitez créer ce tag pour marquer votre progression et recevoir des retours, voici les points à vérifier :

### Fichiers attendus

- [ ] `docs/usecases.md` avec au moins 6-8 cas d'usage listés
- [ ] `src/ports/ticket_repository.py` avec l'interface `TicketRepository`
- [ ] `src/adapters/db/ticket_repository_inmemory.py` avec l'implémentation
- [ ] `src/application/usecases/create_ticket.py` avec le use case
- [ ] `src/application/usecases/assign_ticket.py` avec le use case
- [ ] `tests/application/test_create_ticket.py` avec au moins 3 tests
- [ ] `tests/application/test_assign_ticket.py` avec au moins 3 tests

### Points architecturaux à vérifier

- [ ] Le port est dans `src/ports/`, **pas dans `src/domain/`**
- [ ] Les use cases reçoivent le repository par injection de dépendances
- [ ] Les use cases utilisent l'interface `TicketRepository`, pas l'implémentation
- [ ] Pas d'import de `InMemoryTicketRepository` dans `domain/` et `application/` (seulement dans les tests)

### Tests

- [ ] Tous les tests passent : `pytest tests/application/`
- [ ] Les tests utilisent l'adaptateur InMemory

### Git

- [ ] Commits atomiques avec messages explicites
- [ ] Tag `TD2a` créé sur un commit fonctionnel

---

## 📚 Ressources complémentaires

- [Annexe 01 : Dépendances et inversion](../cm/annexe_01_dependances_et_inversion.md)
- [Annexe 02 : Découpage et responsabilités](../cm/annexe_02_decoupage_et_responsabilites.md)
- [Guide des tests](guides/comment_tester.md)

---

## 🎓 Pour aller plus loin (optionnel)

Si vous finissez en avance, vous pouvez :

1. Ajouter un 3ème use case simple (ex: lister tous les tickets, filtrer les tickets par statut...)
2. Enrichir les tests avec plus de cas d'erreur
3. Ajouter des docstrings complètes sur toutes les méthodes

---
