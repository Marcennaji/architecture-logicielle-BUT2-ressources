# TD0 — Prise en main du workflow Git/GitHub

> **Durée estimée** : 2h (extensible en autonomie)  
> **Prérequis** : [Guide de démarrage](guides/demarrage.md) suivi (repository cloné, `scripts/init.sh` exécuté)  
> **Objectif** : Maîtriser le workflow de développement Git/GitHub utilisé pour tous les TDs  
> **⚠️ Non noté** : Ce TD sert à valider le workflow, mais il est **obligatoire**

---

## 🎯 Objectifs de ce TD

À la fin de ce TD, vous saurez :

1. ✅ Travailler directement sur la branche `main`
2. ✅ Implémenter une fonction utilitaire simple avec ses tests
3. ✅ Utiliser pytest pour valider votre code
4. ✅ Faire des commits réguliers et les pousser sur GitHub
5. ✅ Créer un tag pour marquer votre soumission
6. ✅ Comprendre le cycle complet de développement du module

---

## ✋ Vérification des prérequis (5 min)

**Avant de commencer, vérifiez que vous avez bien suivi le [Guide de démarrage](guides/demarrage.md).**

Exécutez ces commandes dans un terminal :

```bash
# 1. Vous êtes dans le dossier du projet ?
pwd
# Devrait afficher : /home/votre-nom/ticketing (ou similaire)

# 2. L'environnement virtuel est activé ?
which python
# Devrait afficher : /home/votre-nom/ticketing/.venv/bin/python

# 3. Les tests passent ?
pytest
# Devrait afficher : "X passed" en vert
```

**Checklist** :
- [ ] Mon repository `ticketing` existe sur mon compte GitHub
- [ ] J'ai ajouté `Marcennaji` comme collaborateur
- [ ] Le projet est cloné sur ma machine
- [ ] La commande `pytest` fonctionne et tous les tests passent
- [ ] Je vois `(.venv)` au début de ma ligne de commande

> ⚠️ **Si un point manque**, retournez au [Guide de démarrage](guides/demarrage.md) et suivez la procédure.

---

## 📖 Contexte : Que va-t-on faire ?

Dans ce TD, vous allez implémenter une **fonction utilitaire** qui servira plus tard dans le projet de gestion de tickets.

**La fonction** : `calculate_duration_hours(start, end)`  
**Son rôle** : Calculer la durée (en heures) entre deux dates

**Pourquoi cette fonction ?**  
Dans le futur système de tickets, on voudra savoir combien de temps un ticket est resté ouvert, combien de temps il a été en cours de traitement, etc.

**Ce que vous allez apprendre** :
- Créer des modules dans la couche `domain/` (logique métier)
- Écrire des tests unitaires avec pytest
- Utiliser le workflow Git/GitHub (commits réguliers → push → tag)

---

## 💻 Partie 1 : Implémentation de la fonction (35 min)

### 2.1 Créer le fichier de la fonction

Créez le fichier `src/domain/utils.py` avec le contenu suivant :

```python
from datetime import datetime


def calculate_duration_hours(start: datetime, end: datetime) -> float:
    """
    Calcule la durée en heures entre deux dates.
    
    Args:
        start: Date de début
        end: Date de fin
        
    Returns:
        Durée en heures (nombre décimal)
        
    Raises:
        ValueError: Si la date de fin est antérieure à la date de début
        
    Examples:
        >>> from datetime import datetime
        >>> start = datetime(2025, 1, 1, 9, 0)
        >>> end = datetime(2025, 1, 1, 17, 0)
        >>> calculate_duration_hours(start, end)
        8.0
    """
    # TODO: À compléter
    #
    # Indications :
    # 1. Vérifier que end >= start, sinon lever ValueError
    # 2. Calculer la différence : delta = end - start
    # 3. Convertir en heures : delta.total_seconds() / 3600
    # 4. Retourner le résultat
    
    pass  # Remplacez cette ligne par votre code
```

### 2.2 Implémenter la fonction

**À vous de jouer !** Complétez la fonction en suivant les indications dans les commentaires.

**Aide** :
```python
# Pour lever une erreur :
raise ValueError("Message d'erreur")

# Pour calculer une différence de dates :
delta = end - start  # Retourne un objet timedelta

# Pour convertir en heures :
heures = delta.total_seconds() / 3600
```

### 2.3 Créer les tests

Créez le fichier `tests/domain/test_utils.py` avec le contenu suivant :

```python
from datetime import datetime, timedelta
import pytest
from src.domain.utils import calculate_duration_hours


def test_calculate_duration_same_day():
    """Test avec deux dates le même jour."""
    start = datetime(2025, 1, 1, 9, 0)   # 1er janvier à 9h
    end = datetime(2025, 1, 1, 17, 0)    # 1er janvier à 17h
    
    result = calculate_duration_hours(start, end)
    
    assert result == 8.0  # 8 heures de différence


def test_calculate_duration_multiple_days():
    """Test avec plusieurs jours de différence."""
    start = datetime(2025, 1, 1, 9, 0)   # 1er janvier à 9h
    end = datetime(2025, 1, 2, 9, 0)     # 2 janvier à 9h
    
    result = calculate_duration_hours(start, end)
    
    assert result == 24.0  # 24 heures = 1 jour


def test_calculate_duration_with_minutes():
    """Test avec des minutes (résultat décimal)."""
    start = datetime(2025, 1, 1, 10, 0)
    end = datetime(2025, 1, 1, 11, 30)
    
    result = calculate_duration_hours(start, end)
    
    assert result == 1.5  # 1h30 = 1.5 heures


def test_calculate_duration_invalid_order():
    """Test que la fonction lève une erreur si end < start."""
    start = datetime(2025, 1, 2, 9, 0)
    end = datetime(2025, 1, 1, 9, 0)  # Date de fin AVANT la date de début
    
    # On vérifie qu'une ValueError est levée
    with pytest.raises(ValueError):
        calculate_duration_hours(start, end)
```

### 2.4 Lancer les tests

```bash
# Lancer uniquement les tests de ce fichier
pytest tests/domain/test_utils.py -v

# -v = verbose (affiche le détail de chaque test)
```

**Résultat attendu** :
```
tests/domain/test_utils.py::test_calculate_duration_same_day PASSED
tests/domain/test_utils.py::test_calculate_duration_multiple_days PASSED
tests/domain/test_utils.py::test_calculate_duration_with_minutes PASSED
tests/domain/test_utils.py::test_calculate_duration_invalid_order PASSED

======================== 4 passed in 0.05s ========================
```

> 💡 **Si des tests échouent**, lisez attentivement le message d'erreur et corrigez votre fonction.

---

## 🔄 Partie 2 : Workflow Git (20 min)

### 3.1 Vérifier les modifications

```bash
# Voir les fichiers modifiés
git status
```

Vous devriez voir :
```
Untracked files:
  src/domain/utils.py
  tests/domain/test_utils.py
```

### 3.2 Ajouter les fichiers au staging

```bash
# Ajouter les deux fichiers créés
git add src/domain/utils.py tests/domain/test_utils.py

# Vérifier qu'ils sont bien "staged" (en vert)
git status
```

### 3.3 Créer un commit

```bash
git commit -m "TD0: Ajout fonction calculate_duration_hours et ses tests"
```

**Anatomie d'un bon message de commit** :
- ✅ Préfixe du TD : `TD0:`
- ✅ Verbe d'action : `Ajout`, `Correction`, `Refactoring`
- ✅ Description claire de ce qui a été fait
- ✅ Court (< 72 caractères si possible)

> 💡 **Bonne pratique** : Faites plusieurs petits commits au fur et à mesure de votre progression, plutôt qu'un seul gros commit à la fin.

### 3.4 Pousser sur GitHub

```bash
# Pousser sur la branche main
git push origin main
```

Vous devriez voir un message de confirmation indiquant que les commits ont été poussés.

---

## 🏷️ Partie 3 : Créer un tag pour soumettre (5 min)

### 4.1 Vérifier que tout est OK

Avant de créer le tag, vérifiez une dernière fois :

```bash
# Tous les tests passent ?
pytest

# Tous les fichiers sont committés ?
git status
# Devrait afficher "nothing to commit, working tree clean"
```

### 4.2 Créer le tag

```bash
# Créer le tag TD0
git tag TD0

# Pousser le tag sur GitHub
git push origin TD0
```

> ⚠️ **Important** : Le nom du tag doit être **exactement** `TD0` (en majuscules). C'est ce nom que le système d'évaluation recherchera pour les TDs suivants (`TD1`, `TD2`, `TD3`, `TD4`).

### 4.3 Vérifier sur GitHub

1. Allez sur votre repository GitHub
2. Cliquez sur le menu déroulant des branches (où il est écrit "main")
3. Cliquez sur l'onglet **Tags**
4. Vous devriez voir `TD0` dans la liste

✅ **Félicitations !** Vous avez soumis votre premier TD !

---

## ⏰ Si vous n'avez pas terminé

Ce TD **n'est pas noté** mais il est **obligatoire**.

Si vous n'avez pas terminé pendant les 2h de TD :
1. ✅ Terminez le travail en autonomie (en dehors des heures de TD)
2. ✅ Créez le tag `TD0` **avant le prochain TD**
3. ⚠️ Au début du TD1, je vérifierai que chacun a bien le tag TD0

**Aide** : Si vous bloquez, consultez :
- Le [Guide de workflow](guides/workflow_de_developpement.md)
- La [documentation pytest](https://docs.pytest.org/)
- Ou envoyez-moi un email avec votre question

---

## 🎯 Récapitulatif du workflow

| Étape | Commande / Action |
|-------|-------------------|
| **1. Coder** | Créer `src/domain/utils.py` et implémenter |
| **2. Tester** | Créer `tests/domain/test_utils.py` et vérifier avec `pytest` |
| **3. Staging** | `git add src/domain/utils.py tests/domain/test_utils.py` |
| **4. Commit** | `git commit -m "TD0: Ajout fonction calculate_duration_hours et ses tests"` |
| **5. Push** | `git push origin main` |
| **6. Vérification** | `pytest` (tous les tests doivent passer) |
| **7. Tag** | `git tag TD0` |
| **8. Push tag** | `git push origin TD0` |

**Ce workflow sera utilisé pour TOUS les TDs du module** (TD1, TD2, TD3, TD4).

---

## 📚 Pour aller plus loin

### Concepts abordés dans ce TD

| Concept | Description |
|---------|-------------|
| **Commits Git** | Sauvegarder progressivement son travail |
| **Tests unitaires** | Valider qu'une fonction fait ce qu'on attend |
| **pytest.raises** | Tester qu'une exception est bien levée |
| **Tags Git** | Marquer une version spécifique pour soumission |
| **Type hints** | Annoter les types en Python (`-> float`) |

### Ressources

- [Documentation datetime](https://docs.python.org/3/library/datetime.html)
- [Documentation pytest](https://docs.pytest.org/)
- [Guide Git](https://git-scm.com/book/fr/v2)

---

## ➡️ Suite du projet

**TD1 : Modélisation du domaine**  

Dans le prochain TD, nous commencerons à construire le **vrai projet** de gestion de tickets en appliquant l'architecture hexagonale.

Vous créerez les entités métier (`Ticket`, `User`, `Status`) avec leurs règles de validation et leurs comportements.

**La fonction `calculate_duration_hours` que vous avez créée aujourd'hui sera utilisée dans le domaine `Ticket` !**

---

## ❓ FAQ

### J'ai oublié de pousser mes commits, comment faire ?

```bash
git push origin main
```

### Je veux corriger quelque chose après avoir créé le tag

```bash
# Supprimer le tag localement et sur GitHub
git tag -d TD0
git push origin :refs/tags/TD0

# Faire vos corrections
git add .
git commit -m "TD0: corrections finales"
git push origin main

# Recréer le tag
git tag TD0
git push origin TD0
```

> ⚠️ Ne faites cela que si le délai n'est pas encore passé !

### J'ai une erreur "fatal: not a git repository"

Vous n'êtes pas dans le bon dossier. Faites :
```bash
cd ~/ticketing  # ou le chemin vers votre projet
```

### Les tests échouent, que faire ?

Lisez attentivement le message d'erreur de pytest. Il indique :
- Quel test échoue
- Quelle assertion n'est pas vérifiée
- La valeur attendue vs la valeur obtenue

Corrigez votre fonction et relancez `pytest`.

### Quel est le mot de passe Git quand je push ?

Ce n'est **pas** votre mot de passe GitHub, c'est votre **Personal Access Token** créé dans le guide de démarrage. Si vous l'avez perdu, recréez-en un : https://github.com/settings/tokens

