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

| Critère | Coefficient |
|---------|-------------|
| ≥ 3 commits répartis pendant la séance | **1.0** (100%) |
| Tag poussé dans les 10mn après la fin | **0.9** (90%) |
| Tag poussé > 10mn après la séance | **0.7** (70%) |
| 1-2 commits seulement ou concentrés en fin | **0.7** (70%) |
| Tag absent ou très tardif | **0.5** (50%) |

**Note finale du jalon = Note du code × Coefficient de bonus**

---

## 🔍 Détection automatique

Un script analysera pour chaque tag :

```python
# Analyse du dépôt Git pour chaque jalon
- Nombre de commits entre début et fin de séance
- Timestamps des commits (répartition temporelle)
- Heure de push du tag
- Taille des diff (détection de gros commits suspects)
```

**Indicateurs suspects** :
- ❌ 1 seul gros commit juste avant la fin
- ❌ Tag poussé 1-2 jours après la séance
- ❌ Changements massifs incompatibles avec 2h de travail
- ❌ Code trop "parfait" sans itérations visibles

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

### ⚠️ À éviter :

- ❌ Tout faire chez soi puis copier en fin de séance
- ❌ Attendre 1h45 pour faire le premier commit
- ❌ Générer tout le code avec IA puis le copier d'un coup
- ❌ Pousser le tag plusieurs jours après la séance

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

## ❓ FAQ

**Q : Je n'ai pas fini le jalon pendant la séance, puis-je le terminer chez moi ?**
R : Oui, mais vous aurez un coefficient réduit (0.7-0.5). Mieux vaut avoir un code simple mais poussé pendant la séance.

**Q : Exception pour le groupe qui a TD0+TD1a le même jour ?**
R : Oui. Si vous n'aviez pas fait le guide de démarrage avant d'arriver et que vous manquez de temps, vous pourrez **exceptionnellement** terminer TD1a à la maison **sans pénalité de coefficient**. Prévenez l'enseignant en début de séance si c'est votre cas.

**Q : Combien de commits minimum ?**
R : 3 commits répartis dans le temps. Idéalement 4-5.

**Q : Puis-je utiliser l'IA chez moi pour terminer ?**
R : Techniquement oui, mais vous serez pénalisé par le coefficient. L'objectif est de travailler en présentiel.

**Q : Comment savoir si mon coefficient sera bon ?**
R : Si vous commitez régulièrement et poussez votre tag avant la fin, vous aurez 1.0.

**Q : Les commits doivent être parfaits ?**
R : Non ! Des commits de travail en cours sont normaux et valorisés. Ça montre une vraie progression.

---

## 🔐 Intégrité académique

Ce système permet de :
- ✅ **Valoriser** le travail en présentiel sans IA
- ✅ **Détecter** facilement le code généré par IA et copié
- ✅ **Encourager** une pratique professionnelle (commits réguliers)
- ✅ **Évaluer** votre compréhension réelle (QCM sans IA)

**Rappel** : L'IA est un outil d'apprentissage, pas de contournement. Le QCM final (sans IA) compte significativement dans la note.
