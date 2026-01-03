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

### Objectif du jalon
Créer les entités du domaine (Status, User, Ticket) avec les règles métier de base.

### 1. Compréhension du domaine 

Individuellement ou en binôme, répondez aux questions suivantes :

- Qu'est-ce qu'un **ticket** dans un système de support ?
- Quelles informations minimales doit-il contenir ?
- Quels **statuts** peut-il prendre au cours de sa vie ?
- Quels rôles un utilisateur peut-il prendre ?
- Quelles autres entités métier seront certainement nécessaires, pour notre système de traçage des bugs ?

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

### 3. Implémenter l'énumération Status 

Ouvrez `src/domain/status.py` et complétez l'énumération `Status`.

**Indice** : Un ticket suit généralement le cycle de vie suivant :
- `OPEN` → ouvert, en attente de traitement
- `IN_PROGRESS` → en cours de résolution
- `RESOLVED` → résolu, en attente de validation
- `CLOSED` → fermé définitivement

💡 **Commit** : Une fois terminé, commitez vos changements :
```bash
git add src/domain/status.py
git commit -m "Ajout de l'enum Status, servant a gerer le cycle de vie d'un ticket"
git push
```

### 4. Implémenter la classe User

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

### 5. Implémenter la classe Ticket

Ouvrez `src/domain/ticket.py` et complétez la classe `Ticket`.

**Attributs obligatoires** :
- `id`, `title`, `description`
- `status` (avec valeur par défaut `Status.OPEN`)
- `creator_id`
- `assignee_id` (agent assigné, peut être `None`)

**Méthode métier à implémenter** :
- `assign(user_id)` : assigne le ticket à un agent

### 6. Règles métier (invariants) 

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
git commit -m "Ajout de regles metier a la classe Ticket "
git push
```

---

## 🎁 Bonus (facultatif)

**Si vous avez terminé en avance**, enrichissez votre modèle de domaine.
Par exemple, ajoutez des règles métier supplémentaires :
- Le username doit être alphanumérique
- Seul un admin peut créer un ticket avec statut différent de OPEN
- etc...

Vous pouvez également ajouter des entités métiers, autres que le groupe minimal (Status, User, Ticket, DomainError) qui a été donné.

---

### ✅ Checklist minimale avant de soumettre votre tag

**Code** :
- [ ] Fichiers : au minimum, `status.py`, `user.py`, `ticket.py` créés
- [ ] Classes : Status (enum), User, Ticket implémentées
- [ ] Méthode `assign()` dans Ticket
- [ ] Règles métier : titre non vide, username non vide

**Git** :
- [ ] ≥ 3 commits pendant la séance
- [ ] Tag `TD1a` poussé :
  ```bash
  git tag TD1a
  git push origin TD1a
  ```

---
