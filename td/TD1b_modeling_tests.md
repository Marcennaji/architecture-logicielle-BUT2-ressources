# TD1b — Tests unitaires du domaine

## 📦 Jalon TD1b (2h) → Tag `TD1b`

**⏰ Durée : 1 séance de 2h** (séance suivant TD1a)

### 🎯 Objectif

Écrire des tests unitaires qui couvrent **toutes les règles métier** du domaine, y compris les cas d'erreur. L'objectif est de garantir qu'on ne peut pas contourner les règles métier.

### Ce qui est attendu

- ✅ Chaque règle métier a un test qui vérifie le cas nominal
- ✅ Chaque règle métier a un test qui vérifie le cas d'erreur
- ✅ Tous les tests passent : `pytest tests/domain/` vert
- ✅ On ne peut pas contourner les règles métier

Voir [EVALUATION.md](EVALUATION.md) pour le système de notation.

---

## Étape 1 : Lister les règles métier (10 min)

Avant de tester, listez **toutes les règles métier** de votre domaine :

**Exemples de règles métier** :
- Un ticket doit avoir un titre non vide
- Un utilisateur doit avoir un username non vide
- Un ticket fermé ne peut plus être assigné
- Un ticket déjà fermé ne peut pas être re-fermé

📝 **Action** : Complétez cette liste avec vos propres règles.

---

## Étape 2 : Tester les cas nominaux (30 min)

Pour chaque règle métier, écrivez un test qui vérifie le **comportement normal** :

```python
def test_ticket_creation():
    """Un ticket peut être créé avec des valeurs valides."""
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    assert ticket.id == "t1"
    assert ticket.title == "Bug"
    assert ticket.status == Status.OPEN

def test_ticket_assign():
    """Un ticket ouvert peut être assigné."""
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    ticket.assign("agent1")
    assert ticket.assignee_id == "agent1"
    assert ticket.status == Status.IN_PROGRESS

def test_ticket_close():
    """Un ticket peut être fermé."""
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    ticket.close()
    assert ticket.status == Status.CLOSED
```

---

## Étape 3 : Tester les cas d'erreur (30 min)

Pour chaque règle métier, écrivez un test qui vérifie qu'on **ne peut pas violer la règle** :

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
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    ticket.close()
    with pytest.raises(ValueError):
        ticket.assign("agent1")

def test_cannot_close_already_closed_ticket():
    """Règle : Un ticket déjà fermé ne peut pas être re-fermé."""
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    ticket.close()
    with pytest.raises(ValueError):
        ticket.close()
```

---

## Étape 4 : Vérifier qu'on ne peut pas contourner (20 min)

Testez les tentatives de contournement :

```python
def test_cannot_modify_closed_ticket_status_directly():
    """On ne peut pas modifier le statut d'un ticket fermé en le réassignant."""
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    ticket.close()
    
    # Tentative de contournement
    with pytest.raises(ValueError):
        ticket.assign("agent1")  # Doit échouer même si assign() change le statut

def test_status_transitions_are_validated():
    """Les transitions de statut respectent les règles métier."""
    ticket = Ticket(id="t1", title="Bug", description="desc", creator_id="u1")
    
    # Transition valide : OPEN → IN_PROGRESS
    ticket.assign("agent1")
    assert ticket.status == Status.IN_PROGRESS
    
    # Transition valide : IN_PROGRESS → CLOSED
    ticket.close()
    assert ticket.status == Status.CLOSED
```

---

## Étape 5 : Valider (10 min)

Vérifiez que tout fonctionne :

```bash
# Tous les tests passent
pytest tests/domain/

# Vérifier la couverture (optionnel)
pytest tests/domain/ --cov=src/domain
```

---

## ✅ Checklist avant de soumettre

**Tests** :
- [ ] Toutes les règles métier sont listées
- [ ] Chaque règle a un test pour le cas nominal
- [ ] Chaque règle a un test pour le cas d'erreur
- [ ] Tests de non-contournement écrits
- [ ] `pytest tests/domain/` vert (tous les tests passent)

**Git** :
- [ ] Commits réguliers pendant la séance
- [ ] Tag `TD1b` poussé :
  ```bash
  git tag TD1b
  git push origin TD1b
  ```

---

💡 **Rappel** : L'objectif n'est pas la quantité de tests, mais la **qualité** : couvrir toutes les règles métier et s'assurer qu'on ne peut pas les contourner.
