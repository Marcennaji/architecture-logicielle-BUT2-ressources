# TD1 — Modélisation du domaine (Ticketing)

## 🎯 Vue d'ensemble

Ce TD couvre la modélisation du domaine métier du système de ticketing. Il est divisé en **2 jalons de 2h** :
- **TD1a** : Création des entités et règles métier de base
- **TD1b** : Écriture des tests unitaires complets

**Objectifs globaux** :
- Identifier les entités principales du domaine métier
- Lister et implémenter les règles métier (invariants)
- Tester le domaine de manière exhaustive
- Garantir l'indépendance du domaine (pas de dépendances externes)

---

## 📦 Jalon TD1a (2h) → Tag `TD1a`

**⏰ Durée : 1 séance de 2h**

> **Note** : Pour la plupart des groupes, c'est la séance 2. Un groupe particulier fait cette séance juste après TD0 le même jour.

### Objectif du jalon
Créer les entités du domaine (Status, User, Ticket) avec les règles métier de base.

### 📊 Barème de notation (sur 20)

**Critères obligatoires (15 pts)** :
- **Fichiers présents** (8 pts) : `status.py`, `user.py`, `ticket.py`
- **Classes de base** (5 pts) : Status, User, Ticket, DomainError
- **Indépendance technique** (2 pts) : Aucun import externe (fastapi, sqlite3, requests...)

**Bonus domaine riche** (max +5 pts) :
- Entités supplémentaires : +1 pt par classe (Comment, Priority, Project...)
- Exceptions métier : +0.5 pt par classe (*Error, *Exception)
- Maximum cumulé : 5 pts bonus

**Coefficient présentiel** :
- Voir [evaluation_jalons.md](evaluation_jalons.md#1-coefficient-présentiel) pour le détail des coefficients
- En résumé : ×1.0 si tag pendant séance, sinon réduit selon le délai

**Conseils qualité** (0 pt, feedback uniquement) :
- Qualité du code : TODO/FIXME, code commenté, conventions Python
- Ces aspects sont signalés dans le rapport mais ne pénalisent pas la note

💡 **Exemple de calcul** : 15/15 (base) + 3/5 (bonus) = 18/20 brut × 1.0 (présentiel) = **18/20 final**

### 1. Compréhension du domaine (15 min)

Individuellement ou en binôme, répondez aux questions suivantes :

- Qu'est-ce qu'un **ticket** dans un système de support ?
- Quelles informations minimales doit-il contenir ?
- Quels **statuts** peut-il prendre au cours de sa vie ?
- Quels rôles un utilisateur peut-il prendre ?

📝 **Livrable** : Notez vos réponses dans un fichier `docs/domain-notes.md` de votre dépôt.

### 2. Structure des fichiers du domaine

Le domaine est organisé en fichiers séparés (une entité par fichier) :

```
src/domain/
├── __init__.py      # Package du domaine
├── status.py        # Énumération des statuts (TODO)
├── user.py          # Classe User (TODO)  
├── ticket.py        # Classe Ticket (TODO)
└── exceptions.py    # Erreurs métier (fourni)
```

💡 **Note sur les dataclasses** : 
Les classes du domaine utilisent `@dataclass`, une fonctionnalité Python qui simplifie la création de classes :

```python
from dataclasses import dataclass

@dataclass
class User:
    id: str
    username: str
    is_agent: bool = False  # Valeur par défaut

    def __post_init__(self):
        """Validation après création."""
        if not self.username:
            raise ValueError("Username cannot be empty")
```

### 3. Implémenter l'énumération Status (20 min)

Ouvrez `src/domain/status.py` et complétez l'énumération `Status`.

**Indice** : Un ticket suit généralement le cycle de vie suivant :
- `OPEN` → ouvert, en attente de traitement
- `IN_PROGRESS` → en cours de résolution
- `RESOLVED` → résolu, en attente de validation
- `CLOSED` → fermé définitivement

💡 **Commit** : Une fois terminé, commitez vos changements :
```bash
git add src/domain/status.py
git commit -m "Add Status enum with lifecycle values"
git push
```

### 4. Implémenter la classe User (25 min)

Ouvrez `src/domain/user.py` et complétez la classe `User`.

**Attributs suggérés** :
- `id` : identifiant unique
- `username` : nom d'affichage
- `is_agent` : peut traiter des tickets ?
- `is_admin` : droits administrateur ?

💡 **Commit** : Commitez régulièrement :
```bash
git add src/domain/user.py
git commit -m "Add User class with attributes"
git push
```

### 5. Implémenter la classe Ticket (30 min)

Ouvrez `src/domain/ticket.py` et complétez la classe `Ticket`.

**Attributs obligatoires** :
- `id`, `title`, `description`
- `status` (avec valeur par défaut `Status.OPEN`)
- `creator_id`
- `assignee_id` (agent assigné, peut être `None`)

**Méthode métier à implémenter** :
- `assign(user_id)` : assigne le ticket à un agent

💡 **Note** : La méthode `close()` sera implémentée dans TD1b (avec ses tests).

### 6. Règles métier (invariants) (15 min)

Implémentez au moins **2 règles métier** dans vos classes :

| Règle | Où l'implémenter |
|-------|------------------|
| Un ticket doit avoir un titre non vide | `__post_init__` de Ticket |
| Un utilisateur doit avoir un username non vide | `__post_init__` de User |

💡 **Conseil** : Utilisez `raise ValueError("message")` pour signaler les violations.

💡 **Note** : D'autres règles seront ajoutées dans TD1b (ex: ticket fermé non modifiable).

💡 **Commit final** :
```bash
git add src/domain/
git commit -m "Add business rules to Ticket class"
git push
```

---

## 🎁 Bonus (facultatif)

**Si vous avez terminé en avance**, enrichissez votre modèle de domaine.
Par exemple, ajoutez des règles métier supplémentaires :
- Le username doit être alphanumérique
- Seul un admin peut créer un ticket avec statut différent de OPEN
- etc...

---

### ✅ Checklist avant de soumettre

**Code** :
- [ ] Fichiers : `status.py`, `user.py`, `ticket.py` créés
- [ ] Classes : Status (enum), User, Ticket implémentées
- [ ] Méthode `assign()` dans Ticket
- [ ] Règles métier : titre non vide, username non vide
- [ ] **Aucun import externe** (fastapi, sqlite3, requests)

**Git** :
- [ ] ≥ 3 commits pendant la séance
- [ ] Tag `TD1a` poussé :
  ```bash
  git tag TD1a
  git push origin TD1a
  ```

---

## 📦 Jalon TD1b (2h) → Tag `TD1b`

**⏰ Durée : 1 séance de 2h** (séance suivant TD1a)

### Objectif du jalon
Écrire des tests unitaires complets pour valider le comportement du domaine.

### 📊 Barème de notation (sur 20)

**Critères obligatoires (15 pts)** :
- **Tests passent** (8 pts) : `pytest tests/domain/` vert
- **Couverture** (5 pts) : ≥ 80% sur `src/domain/`
- **Tests des règles métier** (2 pts) : Chaque règle a son test

**Bonus tests avancés** (max +5 pts) :
- Tests paramétriques : +1 pt
- Fixtures complexes : +1 pt
- Messages d'erreur testés : +1 pt
- Couverture 100% : +2 pts

**Coefficient présentiel** :
- Voir [evaluation_jalons.md](evaluation_jalons.md#1-coefficient-présentiel) pour le détail
- En résumé : ×1.0 si tag pendant séance, sinon réduit selon le délai

💡 **Exemple** : 15/15 + 2/5 (bonus) = 17/20 × 1.0 = **17/20 final**

### 1. Compléter la classe Ticket (10 min)

Avant d'écrire les tests, ajoutons la méthode `close()` qui manque :

**Dans `src/domain/ticket.py`**, ajoutez :
```python
def close(self):
    """Ferme le ticket."""
    if self.status == Status.CLOSED:
        raise ValueError("Cannot close an already closed ticket")
    self.status = Status.CLOSED
```

💡 **Commit** :
```bash
git add src/domain/ticket.py
git commit -m "Add close() method to Ticket"
git push
```

### 2. Comprendre la structure des tests (10 min)

Explorez le fichier `tests/domain/test_ticket.py` :
- Exemples de tests commentés
- Organisation par fonctionnalité
- Utilisation de pytest

### 3. Activer les tests (5 min)

Dans `tests/domain/test_ticket.py` :
1. Supprimez la ligne `pytest.skip(...)` au début
2. Décommentez les imports
3. Lancez les tests : `pytest tests/domain/`

Les tests vont probablement échouer au début, c'est normal !

### 4. Écrire les tests de base (25 min)

Décommentez et complétez les tests fournis :

**Tests de création** :
```python
def test_status_values_exist():
    """Vérifie que les 4 statuts existent."""
    
def test_user_creation():
    """Vérifie la création d'un utilisateur."""
    
def test_ticket_creation():
    """Vérifie la création d'un ticket avec valeurs par défaut."""
```

💡 **Commit** :
```bash
git add tests/domain/test_ticket.py
git commit -m "Add basic domain tests"
git push
```

### 5. Écrire les tests des règles métier (35 min)

Implémentez les tests pour **chaque règle métier** :

```python
def test_ticket_title_cannot_be_empty():
    """Règle : Un ticket doit avoir un titre non vide."""
    with pytest.raises(ValueError):
        Ticket(id="t1", title="", description="desc", creator_id="u1")

def test_user_username_cannot_be_empty():
    """Règle : Un utilisateur doit avoir un username non vide."""
    with pytest.raises(ValueError):
        User(id="u1", username="", is_agent=False, is_admin=False)

def test_cannot_assign_closed_ticket():
    """Règle : Un ticket fermé ne peut plus être assigné."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.close()
    with pytest.raises(ValueError):
        ticket.assign("agent1")

def test_cannot_close_already_closed_ticket():
    """Règle : Un ticket déjà fermé ne peut pas être re-fermé."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.close()
    with pytest.raises(ValueError):
        ticket.close()
```

💡 **Note** : Vous devrez aussi implémenter la règle "ticket fermé non assignable" dans la méthode `assign()` pour que le test passe.

### 6. Tests des méthodes métier (25 min)

Testez le comportement normal des méthodes :

```python
def test_ticket_assign():
    """Vérifie l'assignation d'un ticket."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.assign("agent1")
    assert ticket.assignee_id == "agent1"

def test_ticket_close():
    """Vérifie la fermeture d'un ticket."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.close()
    assert ticket.status == Status.CLOSED
```

### 7. Vérifier la couverture (5 min)

Lancez les tests avec couverture :
```bash
pytest tests/domain/ --cov=src/domain --cov-report=term-missing
```

Objectif : **≥ 80% de couverture** sur le domaine.

💡 **Commit final** :
```bash
git add tests/domain/
git commit -m "Complete domain tests with business rules"
git push
```

---

## 🎁 Bonus (facultatif)

**Si vous avez terminé en avance**, perfectionnez vos tests.

💡 **Note** : Ces bonus réalisés **pendant la séance** (avec commits horodatés) peuvent améliorer votre note.

### Option 1 : Tests paramétriques

Utilisez `@pytest.mark.parametrize` pour tester plusieurs cas :
```python
@pytest.mark.parametrize("title,should_raise", [
    ("", True),           # Titre vide
    ("   ", True),        # Seulement espaces
    ("OK", False),        # Titre valide court
    ("A" * 200, False),   # Titre très long
])
def test_ticket_title_validation(title, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            Ticket(id="t1", title=title, description="desc", creator_id="u1")
    else:
        ticket = Ticket(id="t1", title=title, description="desc", creator_id="u1")
        assert ticket.title == title
```

### Option 2 : Fixtures complexes

Créez des fixtures réutilisables dans `conftest.py` :
```python
@pytest.fixture
def sample_user():
    return User(id="u1", username="john", is_agent=False, is_admin=False)

@pytest.fixture
def sample_agent():
    return User(id="a1", username="agent_smith", is_agent=True, is_admin=False)

@pytest.fixture
def open_ticket(sample_user):
    return Ticket(
        id="t1",
        title="Bug report",
        description="Something is broken",
        creator_id=sample_user.id
    )
```

### Option 3 : Tester les messages d'erreur

Vérifiez les messages exacts :
```python
def test_empty_title_error_message():
    with pytest.raises(ValueError, match="Ticket title cannot be empty"):
        Ticket(id="t1", title="", description="desc", creator_id="u1")
```

### Option 4 : Viser 100% de couverture

Ajoutez des tests pour :
- Tous les edge cases (None, valeurs extrêmes)
- Toutes les branches conditionnelles
- Les méthodes `__str__()`, `__repr__()` si implémentées
- Les propriétés calculées

### Option 5 : Tests de documentation

Ajoutez des doctests dans vos classes :
```python
class Ticket:
    """Représente un ticket du système.
    
    Examples:
        >>> ticket = Ticket(id="t1", title="Bug", description="Broken", creator_id="u1")
        >>> ticket.status
        <Status.OPEN: 'open'>
        >>> ticket.assign("agent1")
        >>> ticket.assignee_id
        'agent1'
    """
```

---

### ✅ Checklist avant de soumettre

**Tests** :
- [ ] Méthode `close()` implémentée
- [ ] Règle "ticket fermé non assignable" dans `assign()`
- [ ] `pytest tests/domain/` vert (tous les tests passent)
- [ ] Couverture ≥ 80% : `pytest --cov=src/domain`
- [ ] Chaque règle métier a son test (4 minimum)

**Git** :
- [ ] ≥ 3 commits pendant la séance
- [ ] Tag `TD1b` poussé :
  ```bash
  git tag TD1b
  git push origin TD1b
  ```

---

## 🎯 Validation globale TD1

À la fin des 2 jalons :
- ✅ Domaine complet : Status, User, Ticket + règles métier
- ✅ Tests passent : `pytest tests/domain/` vert
- ✅ Couverture ≥ 80%
- ✅ Indépendance : aucun import externe
- ✅ Tags poussés : `TD1a` et `TD1b`

💡 **Coefficient présentiel** : Voir [evaluation_jalons.md](evaluation_jalons.md#1-coefficient-présentiel) pour le barème complet
