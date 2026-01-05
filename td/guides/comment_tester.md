# Guide des tests

## Objectif

Dans ce module, les tests servent à **valider que votre architecture fonctionne** :
- Les tests garantissent que votre code fait ce qu'il doit faire
- Ils permettent de refactorer sans casser
- Ils documentent l'usage de votre code

## Les 3 niveaux de tests 

L'architecture hexagonale se reflète dans **3 niveaux de tests** qui ciblent différents composants :

### 1. Tests domain (unitaires)

**Où** : `tests/domain/`  
**Quoi** : Tester la logique métier pure (entités, value objects, règles métier)  
**Comment** : Pas de mocks, pas de dépendances externes, instanciation directe

**Exemple** :
```python
def test_ticket_cannot_be_closed_if_not_resolved():
    """Un ticket doit être résolu avant d'être clôturé."""
    ticket = Ticket(id=1, title="Bug critique", status=Status.OPEN)
    
    with pytest.raises(ValueError, match="doit être résolu"):
        ticket.close()
```

**Caractéristiques** :
- ✅ Rapides à exécuter (pas d'I/O)
- ✅ Testent les règles métier isolément
- ✅ Pas de dépendances externes (BDD, API, etc.)

---

### 2. Tests application (use cases)

**Où** : `tests/application/`  
**Quoi** : Tester les cas d'usage qui orchestrent le domain et les ports  
**Comment** : Injection de dépendances avec des implémentations in-memory

**Exemple** :
```python
def test_create_ticket_use_case():
    """Cas d'usage de création de ticket."""
    # Arrange : préparation avec repository in-memory
    repo = InMemoryTicketRepository()
    use_case = CreateTicket(ticket_repository=repo)
    
    # Act : exécution du use case
    ticket = use_case.execute(
        title="Bug critique",
        description="L'application plante au démarrage"
    )
    
    # Assert : vérifications
    assert ticket.id is not None
    assert ticket.status == Status.OPEN
    assert repo.get(ticket.id) == ticket
```

**Caractéristiques** :
- ✅ Testent l'orchestration entre domain et ports
- ✅ Utilisent des adapters "fake" (InMemory)
- ✅ Vérifient les interactions sans dépendances réelles

---

### 3. Tests e2e (API / intégration)

**Où** : `tests/e2e/`  
**Quoi** : Tester l'API complète (requête HTTP → routeur → use case → repository)  
**Comment** : TestClient FastAPI qui fait des requêtes HTTP

**Exemple** :
```python
def test_create_ticket_via_api(client):
    """Test end-to-end de création de ticket via l'API."""
    response = client.post("/tickets", json={
        "title": "Bug critique",
        "description": "L'application plante"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Bug critique"
    assert data["status"] == "OPEN"
```

**Caractéristiques** :
- ✅ Testent **toute la stack** : API + use cases + domain
- ✅ Valident le routeur FastAPI, validation Pydantic, sérialisation JSON
- ✅ Valident les codes HTTP et contrats d'API
- 💡 Peuvent toutefois utiliser une base in-memory (pour la rapidité)

**Différence avec tests application** :
- Tests application : appellent le use case **directement** (fonction Python)
- Tests e2e : passent par une **requête HTTP** (testent l'adapter API en plus)

---

## Workflow recommandé

Pour chaque TD, suivez cette approche simple :

1. **Écrivez le code** (fonction domain, use case, route API)
2. **Écrivez les tests** pour valider le comportement
3. **Lancez pytest** pour vérifier que tout passe
4. **Refactorez** si nécessaire (les tests vous protègent)
5. **Commitez** code + tests ensemble

> **Important** : L'essentiel n'est pas **quand** vous écrivez les tests (avant ou après le code), mais **que vous les écriviez** systématiquement.

---

## ✅ Critères de qualité d'un test

Un bon test :

| Critère | Exemple |
|---------|---------|
| **Nom explicite** | `test_ticket_cannot_be_closed_if_not_resolved` |
| **Structure AAA** | Arrange (préparer) → Act (agir) → Assert (vérifier) |
| **Une seule chose** | Teste un seul comportement à la fois |
| **Déterministe** | Passe ✅ ou échoue ❌ de façon reproductible |
| **Indépendant** | Ne dépend pas de l'ordre d'exécution des tests |

**Exemple de structure AAA** :
```python
def test_assign_ticket():
    # ARRANGE : préparation des données
    ticket = Ticket(id=1, title="Bug", status=Status.OPEN)
    user = User(id=10, name="Alice")
    
    # ACT : exécution de l'action à tester
    ticket.assign(user)
    
    # ASSERT : vérification du résultat
    assert ticket.assigned_to == user
    assert ticket.status == Status.IN_PROGRESS
```

---

## Commandes pytest utiles

```bash
# Lancer tous les tests
pytest

# Tests d'une couche spécifique
pytest tests/domain/            # Tests domain uniquement
pytest tests/application/       # Tests use cases uniquement
pytest tests/e2e/               # Tests API uniquement

# Options utiles
pytest -v                       # Mode verbose (détails de chaque test)
pytest -k "test_create"         # Tests contenant "create" dans le nom
pytest tests/domain/test_ticket.py  # Un fichier spécifique

```

---

## Pourquoi 3 niveaux ?

L'architecture hexagonale **facilite** les tests en séparant les responsabilités :

| Niveau | Ce qu'on teste | Rapidité | Complexité |
|--------|----------------|----------|------------|
| **Domain** | Règles métier pures | ⚡⚡⚡ Très rapide | Simple |
| **Application** | Orchestration use cases | ⚡⚡ Rapide | Moyenne |
| **E2E** | Système complet | ⚡ Plus lent | Complexe |

---

## Ressources

- [Documentation pytest](https://docs.pytest.org/)
- Tests fournis dans le projet comme exemples
