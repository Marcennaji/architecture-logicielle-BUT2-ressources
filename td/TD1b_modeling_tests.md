
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
