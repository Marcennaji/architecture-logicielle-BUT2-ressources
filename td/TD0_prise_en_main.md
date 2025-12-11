# TD0 — Prise en main du workflow Git/GitHub

> **Durée estimée** : 2h (extensible en autonomie)  
> **Prérequis** : [Guide de démarrage](guides/demarrage.md) suivi (repository cloné, `scripts/init.sh` exécuté)  
> **Objectif** : Maîtriser le workflow de développement Git/GitHub utilisé pour tous les TDs  
> **⚠️ Non noté** : Ce TD sert à valider le workflow, mais il est **obligatoire**

---

## 🎯 Objectifs de ce TD

À la fin de ce TD, vous saurez :

1. ✅ Créer une branche dédiée pour un TD
2. ✅ Implémenter une fonction utilitaire simple avec ses tests
3. ✅ Utiliser pytest pour valider votre code
4. ✅ Commiter et pousser votre travail sur GitHub
5. ✅ Créer une Pull Request pour soumission et review
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
- [ ] J'ai ajouté `Marcennaji` comme collaborateur (rôle Read)
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
- Utiliser le workflow Git/GitHub (branche → commit → push → PR)

---

## 📁 Partie 1 : Création de la branche de travail (5 min)

### Pourquoi une branche par TD ?

En entreprise comme dans ce module, on ne travaille **jamais directement sur `main`**. On crée une branche pour chaque fonctionnalité ou TD, puis on soumet notre travail via une **Pull Request**.

**Avantages** :
- 🔒 La branche `main` reste stable
- 👀 Le code peut être reviewé avant d'être intégré
- 🔄 On peut travailler sur plusieurs TDs en parallèle

### Créer votre branche

```bash
# Vérifier qu'on est sur main
git branch
# L'étoile * devrait être sur main

# Créer et basculer sur la nouvelle branche
git checkout -b td0-utils-duration

# Vérifier qu'on est bien sur la nouvelle branche
git branch
# L'étoile * devrait maintenant être sur td0-utils-duration
```

> 💡 **Convention de nommage** : `td0-utils-duration` = TD0 + description courte de ce qu'on fait

---

## 💻 Partie 2 : Implémentation de la fonction (35 min)

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

## 🔄 Partie 3 : Workflow Git (20 min)

### 3.1 Vérifier les modifications

```bash
# Voir les fichiers modifiés
git status
```

Vous devriez voir :
```
On branch td0-utils-duration
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

### 3.4 Pousser la branche sur GitHub

```bash
# Pousser la branche sur votre repository GitHub
git push origin td0-utils-duration
```

Vous devriez voir un message de confirmation indiquant que la branche a été poussée.

---

## 📬 Partie 4 : Création de la Pull Request (20 min)

### 4.1 Qu'est-ce qu'une Pull Request ?

Une **Pull Request** (PR) est une demande pour intégrer votre code dans la branche `main`. Elle permet :
- 👀 La **revue de code** par l'enseignant
- 💬 Des **commentaires** ligne par ligne
- ✅ La **validation** avant l'intégration

### 4.2 Créer la PR sur GitHub

1. Allez sur votre repository GitHub : `https://github.com/VOTRE-USERNAME/ticketing`

2. Vous devriez voir un bandeau jaune proposant de créer une PR pour votre branche :
   ```
   td0-utils-duration had recent pushes
   [Compare & pull request]
   ```
   Cliquez sur **Compare & pull request**

3. **Si le bandeau n'apparaît pas** :
   - Cliquez sur l'onglet **Pull requests**
   - Cliquez sur **New pull request**
   - Sélectionnez votre branche `td0-utils-duration` dans le menu déroulant

4. Remplissez le formulaire de la PR :
   - **Titre** : `TD0 - Fonction calculate_duration_hours`
   - **Description** : 
     ```markdown
     ## Résumé
     Implémentation de la fonction `calculate_duration_hours` qui calcule 
     la durée en heures entre deux dates.
     
     ## Fichiers ajoutés
     - `src/domain/utils.py` : fonction utilitaire
     - `tests/domain/test_utils.py` : 4 tests (cas nominaux + erreur)
     
     ## Tests
     - ✅ Tous les tests passent (4/4)
     ```

5. **⚠️ NE MERGEZ PAS** la PR vous-même ! Cliquez sur **Create pull request**

### 4.3 Attendre la review et merger

Votre enseignant va :
- 📖 Lire votre code
- 💬 Ajouter des commentaires ligne par ligne si nécessaire
- ✅ Approuver la PR quand tout est bon (bouton "Approve")

Vous recevrez une **notification GitHub** pour chaque action.

**Quand vous recevez des commentaires** :
1. Lisez attentivement chaque commentaire
2. Apportez les corrections demandées dans votre code local
3. Commitez et poussez les modifications sur la même branche :
   ```bash
   git add .
   git commit -m "TD0: Corrections suite à review"
   git push origin td0-utils-duration
   ```
4. La PR se mettra à jour automatiquement avec vos nouveaux commits

**Quand la PR est approuvée** (✅ "Approved") :
1. Vérifiez que tous les commentaires sont résolus
2. **Vous mergez la PR vous-même** (bouton "Merge pull request")
3. Confirmez le merge (bouton "Confirm merge")
4. Vous pouvez ensuite supprimer la branche (bouton "Delete branch")

> ⚠️ **Important** : Ne mergez PAS avant l'approbation de l'enseignant !

> 💡 **Bon à savoir** : Même après le merge, tous les commentaires de la PR restent accessibles dans l'historique GitHub.

---

## ⏰ Si vous n'avez pas terminé

Ce TD **n'est pas noté** mais il est **obligatoire**.

Si vous n'avez pas terminé pendant les 2h de TD :
1. ✅ Terminez le travail en autonomie (en dehors des heures de TD)
2. ✅ Soumettez votre Pull Request **avant le prochain TD**
3. ⚠️ Au début du TD1, je vérifierai que chacun a soumis sa PR

**Aide** : Si vous bloquez, consultez :
- Le [Guide de workflow](guides/workflow_de_developpement.md)
- La [documentation pytest](https://docs.pytest.org/)
- Ou envoyez-moi un email avec votre question

---

## 🎯 Récapitulatif du workflow

| Étape | Commande / Action |
|-------|-------------------|
| **1. Créer branche** | `git checkout -b td0-utils-duration` |
| **2. Coder** | Créer `src/domain/utils.py` et implémenter |
| **3. Tester** | Créer `tests/domain/test_utils.py` et vérifier avec `pytest` |
| **4. Staging** | `git add src/domain/utils.py tests/domain/test_utils.py` |
| **5. Commit** | `git commit -m "TD0: Ajout fonction calculate_duration_hours et ses tests"` |
| **6. Push** | `git push origin td0-utils-duration` |
| **7. Pull Request** | Sur GitHub : Create pull request |
| **8. Review** | Attendre la review et l'approbation de l'enseignant |
| **9. Corrections** | Si demandées : corriger, commiter, pusher |
| **10. Merge** | **Après approbation** : vous mergez vous-même la PR |

**Ce workflow sera utilisé pour TOUS les TDs du module.**

---

## 📚 Pour aller plus loin

### Concepts abordés dans ce TD

| Concept | Description |
|---------|-------------|
| **Branching Git** | Isoler son travail sur une branche dédiée |
| **Tests unitaires** | Valider qu'une fonction fait ce qu'on attend |
| **pytest.raises** | Tester qu'une exception est bien levée |
| **Pull Request** | Soumettre du code pour review |
| **Type hints** | Annoter les types en Python (`-> float`) |

### Ressources

- [Documentation datetime](https://docs.python.org/3/library/datetime.html)
- [Documentation pytest](https://docs.pytest.org/)
- [Guide Git](https://git-scm.com/book/fr/v2)
- [Guide Pull Request](https://docs.github.com/en/pull-requests)

---

## ➡️ Suite du projet

**TD1 : Modélisation du domaine**  

Dans le prochain TD, nous commencerons à construire le **vrai projet** de gestion de tickets en appliquant l'architecture hexagonale.

Vous créerez les entités métier (`Ticket`, `User`, `Status`) avec leurs règles de validation et leurs comportements.

**La fonction `calculate_duration_hours` que vous avez créée aujourd'hui sera utilisée dans le domaine `Ticket` !**

---

## ❓ FAQ

### Puis-je modifier ma PR après l'avoir créée ?

Oui ! Faites simplement de nouveaux commits sur la même branche et poussez-les :
```bash
git add .
git commit -m "TD0: Correction suite à remarque"
git push origin td0-utils-duration
```
La PR se mettra à jour automatiquement.

### Qui merge la Pull Request ?

**Vous** ! Après que l'enseignant ait approuvé votre PR, c'est à vous de cliquer sur le bouton "Merge pull request" sur GitHub. Ne mergez pas avant l'approbation.

### Les commentaires de la PR disparaissent après le merge ?

Non ! Tous les commentaires restent accessibles dans l'historique de la PR même après le merge. Vous pouvez les consulter à tout moment dans l'onglet "Pull requests" (filtre "Closed").

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
