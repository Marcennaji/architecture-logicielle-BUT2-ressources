# TD01 — Modélisation du domaine (Ticketing)

🎯 **Objectifs**

- Identifier les entités principales du domaine métier.
- Lister les règles métier (invariants) de base.
- Implémenter les classes du domaine en Python.

---

## 1. Compréhension du domaine

En petits groupes, répondez aux questions suivantes :

- Qu'est-ce qu'un **ticket** dans un système de support ?
- Quelles informations minimales doit-il contenir ?
- Quels **statuts** peut-il prendre au cours de sa vie ?
- Quels rôles d'utilisateur existe-t-il (simple user, support, admin…) ?

📝 **Livrable** : Notez vos réponses dans un fichier `docs/domain-notes.md` de votre dépôt.

---

## 2. Structure des fichiers du domaine

Le domaine est organisé en fichiers séparés (une entité par fichier) :

```
src/domain/
├── __init__.py      # Package du domaine
├── status.py        # Énumération des statuts (TODO)
├── user.py          # Classe User (TODO)  
├── ticket.py        # Classe Ticket (TODO)
└── exceptions.py    # Erreurs métier (fourni)
```

---

## 3. Implémenter l'énumération Status

Ouvrez `src/domain/status.py` et complétez l'énumération `Status`.

**Indice** : Un ticket suit généralement le cycle de vie suivant :
- `OPEN` → ouvert, en attente de traitement
- `IN_PROGRESS` → en cours de résolution
- `RESOLVED` → résolu, en attente de validation
- `CLOSED` → fermé définitivement

---

## 4. Implémenter la classe User

Ouvrez `src/domain/user.py` et complétez la classe `User`.

**Attributs suggérés** :
- `id` : identifiant unique
- `username` : nom d'affichage
- `is_agent` : peut traiter des tickets ?
- `is_admin` : droits administrateur ?

---

## 5. Implémenter la classe Ticket

Ouvrez `src/domain/ticket.py` et complétez la classe `Ticket`.

**Attributs obligatoires** :
- `id`, `title`, `description`
- `status` (avec valeur par défaut `Status.OPEN`)
- `creator_id`

**Attributs optionnels** :
- `assignee_id` (agent assigné, peut être `None`)
- `created_at`, `updated_at` (dates)

**Méthodes métier à implémenter** :
- `assign(user_id)` : assigne le ticket à un agent
- `close()` : ferme le ticket

---

## 6. Règles métier (invariants)

Implémentez au moins **3 règles métier** dans vos classes :

| Règle | Où l'implémenter |
|-------|------------------|
| Un ticket doit avoir un titre non vide | `__post_init__` de Ticket |
| Un ticket fermé ne peut plus être assigné | Méthode `assign()` |
| Un ticket déjà fermé ne peut pas être re-fermé | Méthode `close()` |

💡 **Conseil** : Utilisez `raise ValueError("message")` pour signaler les violations.

---

## 7. Activer les tests

Une fois vos classes implémentées :

1. Ouvrez `tests/domain/test_ticket.py`
2. Supprimez la ligne `pytest.skip(...)` au début
3. Décommentez les imports
4. Lancez les tests : `pytest tests/domain/`

---

## 8. Critères de validation

- [ ] `Status` contient au moins 4 valeurs (OPEN, IN_PROGRESS, RESOLVED, CLOSED)
- [ ] `User` a les attributs `id`, `username`, `is_agent`, `is_admin`
- [ ] `Ticket` a tous les attributs obligatoires
- [ ] Les méthodes `assign()` et `close()` sont implémentées
- [ ] Au moins 3 règles métier sont codées
- [ ] Les tests du domaine passent (`pytest tests/domain/`)
- [ ] Le fichier `docs/domain-notes.md` existe avec vos réflexions
- [ ] **Aucune dépendance externe** dans le dossier `domain/` (pas de FastAPI, SQLAlchemy, etc.)
