# Système d'évaluation par jalons de 2h

## 🎯 Principe général

Chaque séance de TD de 2h constitue un **jalon évaluable indépendant** avec son propre tag Git à pousser.

**Objectif** : Valoriser le travail effectué en présentiel et détecter le travail fait à la maison avec IA.

---

## 📋 Liste des jalons et tags

| Séance | Jalon | Tag Git | Contenu |
|--------|-------|---------|---------|
| 1 | TD0 | `TD0` | Prise en main workflow Git/GitHub |
| 2 | TD1a | `TD1-domain` | Entités domaine (Ticket, User, Status) + règles métier de base |
| 3 | TD1b | `TD1-tests` | Tests unitaires du domaine complets |
| 4 | TD2a | `TD2-ports` | Définition des ports + use case création ticket |
| 5 | TD2b | `TD2-usecases` | Use cases complets (assign, close, list) |
| 6 | TD3a | `TD3-repository` | Repository pattern + implémentation in-memory |
| 7 | TD3b | `TD3-sqlite-1` | SQLite adapter (connexion + création tables) |
| 8 | TD3c | `TD3-sqlite-2` | SQLite CRUD complet + tests d'intégration |
| 9 | TD4a | `TD4-api` | API REST FastAPI (endpoints CRUD de base) |
| 10 | TD4b | `TD4-complete` | Tests E2E + finalisation (après QCM 45mn) |

**Total : 10 jalons évalués**

---

## ✅ Critères de validation d'un jalon

Pour qu'un jalon soit considéré comme **validé en présentiel**, il doit :

1. **Au moins 3 commits** pendant la séance de 2h
2. **Commits répartis** dans le temps (pas tout dans les 10 dernières minutes)
3. **Tag poussé** avant la fin de la séance ou dans les 10 minutes suivantes
4. **Tests passants** sur le tag

---

## 📊 Calcul du bonus présentiel

Chaque jalon reçoit un **coefficient de bonus** selon les commits :

| Critère | Coefficient | Exemple (code noté 16/20) |
|---------|-------------|---------------------------|
| ≥ 3 commits répartis pendant la séance | **1.0** (100%) | 16 × 1.0 = **16/20** |
| Tag poussé dans les 10mn après la fin | **0.9** (90%) | 16 × 0.9 = **14.4/20** |
| Tag poussé < 24h après (ex: le soir) | **0.8** (80%) | 16 × 0.8 = **12.8/20** |
| Tag poussé 1-3 jours après | **0.7** (70%) | 16 × 0.7 = **11.2/20** |
| 1-2 commits ou concentrés en fin | **0.7** (70%) | 16 × 0.7 = **11.2/20** |
| Tag poussé > 3 jours après | **0.6** (60%) | 16 × 0.6 = **9.6/20** |
| Tag absent après relance | **0** (non rendu) | Non évalué |

**Note finale du jalon = Note du code × Coefficient de bonus**

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

2. **N'attendez pas la dernière minute** pour pousser le tag
   ```bash
   git tag TD1-domain
   git push origin TD1-domain
   ```

3. **Travaillez en itérations** :
   - ✅ Implémentation basique → commit
   - ✅ Ajout règles métier → commit
   - ✅ Tests → commit
   - ✅ Refactoring → commit

4. **Testez régulièrement** : `pytest` avant chaque commit

5. **Si vous finissez en avance** : Explorez les **bonus facultatifs** à la fin de chaque TD
   - Ces bonus réalisés **pendant la séance** (avec commits horodatés) peuvent **améliorer votre note**
   - Exemples : tests avancés, validation supplémentaire, documentation enrichie
   - Les bonus comptent comme un critère de qualité dans l'évaluation du jalon

---

## 🎓 Exemple de workflow réussi

**Séance TD1a (2h) : Modélisation du domaine**

```
08:15 - Début de séance
08:45 - Commit 1 : "Add Status enum with 4 values"
09:15 - Commit 2 : "Add User class with basic attributes"
09:45 - Commit 3 : "Add Ticket class with id, title, description"
10:00 - Commit 4 : "Add business rule: title cannot be empty"
10:10 - Tag + push : git tag TD1-domain && git push origin TD1-domain
10:15 - Fin de séance
```

**Résultat** : 4 commits répartis + tag à l'heure → **Coefficient 1.0** ✅

---

