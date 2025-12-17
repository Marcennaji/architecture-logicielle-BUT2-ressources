# Module R4.01 Architecture logicielle (BUT2)

Année 2025/2026 - Enseignant : Marc Ennaji (marc.ennaji@univ-rennes.fr)

## 🎯 Objectifs du module

- Comprendre **pourquoi** l'architecture logicielle est essentielle
- Maîtriser les **principes fondamentaux** d'une bonne architecture : cohésion, couplage, dépendances, inversion de dépendances.
- Savoir **structurer une application** selon l'architecture hexagonale (Ports & Adapters).
- Mettre en œuvre une architecture hexagonale sur un **projet fil rouge**.
- Travailler avec des **briques logicielles existantes** (framework web, ORM, services web, etc.).

## 📌 Projet fil rouge

- Sujet : **Gestionnaire de tickets / workflow** (type Trello / Jira minimal).
- Réalisé au fil des TD : **10 jalons de 2h** évalués indépendamment.
- Dépôt propre à chaque étudiant, créé à partir d'un **bootstrap** commun.
- Chaque jalon = 1 tag Git à pousser pendant la séance.
- **Bonus présentiel** : Commits réguliers pendant les séances valorisés.

## 📚 Ressources du cours

### Cours magistraux (CM)

| Document | Description |
|----------|-------------|
| [CM : Fondamentaux et architecture hexagonale](export/CM1_Fondamentaux_architecture.pdf) | Pourquoi l'architecture ? Principes fondamentaux • Architecture hexagonale |

### Travaux dirigés

**Guides généraux** :
- [📖 Guide de démarrage](td/guides/demarrage.md) ⚠️ **À suivre AVANT le TD0**
- [🔄 Workflow de développement](td/guides/workflow_de_developpement.md)
- [📊 Système d'évaluation par jalons](td/evaluation_jalons.md) 🎯 **Important !**
- [🧪 Guide des tests](td/guides/comment_tester.md)

**TDs** (publiés progressivement) :
- [TD0 : Prise en main](td/TD0_prise_en_main.md) ✅ Disponible
- [TD1 : Modélisation du domaine](td/TD01_domain_modeling.md) ✅ Disponible
- TD2 : Use cases et ports 🔒 *Bientôt*
- TD3 : Repository SQLite 🔒 *Bientôt*
- TD4 : API REST 🔒 *Bientôt*

👉 [Accéder à tous les TDs](td/README.md)

### Template de code

Le template de démarrage (code à compléter) est dans un repository séparé :

👉 https://github.com/Marcennaji/ticketing_starter

## 🗓 Planning indicatif

### Cours magistral (1 × 2h)

| CM | Titre | Contenu |
|----|-------|---------|
| **CM** | Fondamentaux et architecture hexagonale | Pourquoi l'architecture ? • Architecture à l'ère de l'IA • Principes (cohésion, couplage, dépendances) • Architecture hexagonale (Ports & Adapters) • Présentation du projet |

**Volume total du module** : 2h CM + 20h TD = **22h** (sur calendrier)
10 jalons de 2h)

| Jalon | Titre | Tag | Contenu |
|-------|-------|-----|---------|
| **TD0** | Prise en main | `TD0` | Workflow Git/GitHub, pytest |
| **TD1a** | Modélisation domaine | `TD1-domain` | Entités (Ticket, User, Status), règles métier |
| **TD1b** | Tests domaine | `TD1-tests` | Tests unitaires du domaine |
| **TD2a** | Ports & use case | `TD2-ports` | Ports + use case création ticket |
| **TD2b** | Use cases complets | `TD2-usecases` | Assign, close, list tickets |
| **TD3a** | Repository pattern | `TD3-repository` | Repository abstrait + in-memory |
| **TD3b** | SQLite adapter | `TD3-sqlite-1` | Connexion SQLite + tables |
| **TD3c** | SQLite CRUD | `TD3-sqlite-2` | CRUD complet + tests intégration |
| **TD4a** | API REST | `TD4-api` | Endpoints FastAPI CRUD |
| **TD4b** | Tests E2E | `TD4-complete` | Tests E2E + finalisation (après QCM) |

**Système d'évaluation** : Chaque jalon = 1 livrable évalué avec bonus présentiel (commits réguliers pendant la séance). Voir [evaluation_jalons.md](td/evaluation_jalons.md)
Ce planning couvre le socle minimal de l'architecture hexagonale. Les fonctionnalités avancées (authentification, notifications, etc.) peuvent être ajoutées en bonus.

## 📖 Références

### Architecture hexagonale
- [Architecture hexagonale : 3 principes et un exemple — OCTO](https://blog.octo.com/architecture-hexagonale-trois-principes-et-un-exemple-dimplementation/) *(FR)*

### Principes fondamentaux
- [Principes SOLID — Grafikart](https://grafikart.fr/tutoriels/solid-principles-2153) *(vidéo FR)*
- [Écrivez du code Python maintenable — OpenClassrooms](https://openclassrooms.com/fr/courses/7415611-ecrivez-du-code-python-maintenable) *(cours gratuit FR)*

### Outils utilisés
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation pytest](https://docs.pytest.org/)

### Pour aller plus loin
- 📘 **Modern Software Engineering** — David Farley *(EN)* : vision pragmatique de l'ingénierie logicielle moderne
