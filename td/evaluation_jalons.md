# Système d'évaluation par jalons de 2h

## 🎯 Principe général

Chaque séance de TD de 2h constitue un **jalon évaluable indépendant** avec son propre tag Git à pousser.

**Objectif** : Valoriser le travail effectué en présentiel.

---

## 📋 Liste des jalons et tags

| Séance | Jalon | Tag Git | Contenu |
|--------|-------|---------|---------|
| 1 | TD0 | `TD0` | Prise en main workflow Git/GitHub |
| 2 | TD1a | `TD1a` | Entités domaine (Ticket, User, Status) + règles métier de base |
| 3 | TD1b | `TD1b` | Tests unitaires du domaine complets |
| 4 | TD2a | `TD2a` | Définition des ports + use case création ticket |
| 5 | TD2b | `TD2b` | Use cases complets (assign, close, list) |
| 6 | TD3a | `TD3a` | Repository pattern + implémentation in-memory |
| 7 | TD3b | `TD3b` | SQLite adapter (connexion + création tables) |
| 8 | TD3c | `TD3c` | SQLite CRUD complet + tests d'intégration |
| 9 | TD4a | `TD4a` | API REST FastAPI (endpoints CRUD de base) |
| 10 | TD4b | `TD4b` | Tests E2E + finalisation (après QCM 45mn) |

**Total : 10 jalons évalués**

---

## ✅ Critères de validation d'un jalon

Pour qu'un jalon soit considéré comme **validé en présentiel avec coefficient maximum (1.0)**, il doit remplir toutes ces conditions:

1. **Au moins 3 commits** pendant la séance de 2h
2. **Tag poussé** avant la fin de la séance
3. **Tests passants avec succès** sur le tag

---

## 📊 Calcul de la note

### 1. Coefficient présentiel

| Critère | Coefficient |
|---------|-------------|
| Tag poussé pendant la séance + ≥ 3 commits en séance | **1.0** |
| Tag poussé dans les 7 jours après la séance | **0.7** |
| Tag poussé après relance (> 7 jours) | **0.5** |
| Pas de tag 3 jours après relance | **0** |

> 💡 **Relance automatique** : Un rappel est envoyé 7 jours après chaque séance pour les jalons non rendus. Délai supplémentaire : 3 jours (coefficient 0.5).

### 2. Bonus

**⚠️ Les bonus ne sont comptabilisés QUE si le tag est poussé pendant la séance** (avec un coefficient 1.0).

Chaque bonus réalisé ajoute **+0.5 point** à la note de base (max +5 points).

#### Calcul des bonus - Classes Exception du domaine

Une classe Exception donne droit à un bonus de **+0.5 point** uniquement si :

1. ✅ Elle hérite (directement ou indirectement) de `Exception`
2. ✅ Elle est **effectivement levée** (`raise` en Python) dans le code métier du domaine

**⚠️ Pénalité** : Une exception définie mais **jamais levée** = **-0.5 point**

**Exemples :**

❌ **Exception fantôme (pénalité -0.5 pt)** :
```python
# exceptions.py - Exception définie
class TicketNotFoundError(DomainError):
    pass

# Aucun fichier ne fait: raise TicketNotFoundError(...)
```
→ Exception créée "au cas où" = **-0.5 point**

✅ **Exception utilisée (bonus +0.5 pt)** :
```python
# exceptions.py
class InvalidStatusTransitionError(DomainError):
    pass

# ticket.py - Exception levée dans une règle métier
def close(self):
    if self.status == Status.CLOSED:
        raise InvalidStatusTransitionError("Already closed")
    self.status = Status.CLOSED
```
→ Exception utilisée dans le domaine = **+0.5 point**

**Principe** : Une exception existe parce qu'elle est levée dans une règle métier, pas "au cas où un futur Use Case en aurait besoin". En architecture hexagonale, les Use Cases *consomment* les exceptions, ils ne les anticipent pas.

#### Autres bonus

- Entités métier supplémentaires : **+1.0 pt/classe** (Comment, Priority, Project, etc.)
- Tests avancés (parametrize, fixtures) : **+0.5 pt**
- Configuration externe (YAML, ENV) : **+0.5 pt**

### 3. Calcul final

**Note finale = (Note de base + Points bonus) × Coefficient**

**Exemples** : 

*Cas 1 - Tag pendant séance avec bonus :*
- Note de base : 15/20
- 2 bonus réalisés : +1 point
- Tag pendant la séance : coefficient 1.0
- **Note finale** : (15 + 1) × 1.0 = **16/20** ✅

*Cas 2 - Tag le lendemain (bonus ignorés) :*
- Note de base : 15/20
- 2 bonus réalisés mais tag le lendemain : +0 point (bonus non comptés)
- Tag dans les 7 jours : coefficient 0.7
- **Note finale** : 15 × 0.7 = **10.5/20** ⚠️

*Cas 3 - Tag après relance (9 jours après la séance) :*
- Note de base : 15/20
- Tag après relance : coefficient 0.5
- **Note finale** : 15 × 0.5 = **7.5/20** ❌

> 💡 **Philosophie** : L'IA est un outil d'apprentissage légitime. Ce système valorise le travail en présentiel sans pénaliser excessivement ceux qui terminent chez eux. Même avec un coefficient réduit, un excellent travail reste reconnu.

---

## 💡 Conseils aux étudiants

### Pour maximiser votre note :

1. **Commitez régulièrement** (toutes les 20-30 minutes)
   ```bash
   git add .
   git commit -m "Implémentation classe Ticket"
   git push
   ```

2. **Poussez le tag avant la fin de la séance**
   ```bash
   git tag TD1a
   git push origin TD1a
   ```

3. **Travaillez en itérations** :
   - ✅ Implémentation basique → commit
   - ✅ Ajout règles métier → commit
   - ✅ Tests → commit
   - ✅ Refactoring → commit

4. **Testez régulièrement** : `pytest` avant chaque commit

5. **Si vous finissez en avance** : Réalisez les **bonus facultatifs** à la fin de chaque TD
   - Chaque bonus = **+0.5 point** sur la note finale (max +1 point)
   - ⚠️ **Bonus comptés uniquement si tag poussé pendant la séance**
   - Exemples : tests avancés (parametrize, fixtures), attributs supplémentaires, fichiers de configuration

---

## 🎓 Exemple de workflow réussi

**Séance TD1a (2h) : Modélisation du domaine**

```
08:15 - Début de séance
08:45 - Commit 1 : "Add Status enum with 4 values"
09:15 - Commit 2 : "Add User class with basic attributes"
09:45 - Commit 3 : "Add Ticket class with id, title, description"
10:00 - Commit 4 : "Add business rule: title cannot be empty"
10:10 - Tag + push : git tag TD1a && git push origin TD1a
10:15 - Fin de séance
```

**Résultat** : 4 commits + tag poussé pendant la séance → **Coefficient 1.0** ✅

---

