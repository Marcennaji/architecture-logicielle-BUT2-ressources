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
- Réalisé au fil des TD (TD0-TD4, 20h présentiel + travail maison).
- Dépôt propre à chaque étudiant, créé à partir d'un **bootstrap** commun.
- Les TD servent de **guides de progression**.

## 📚 Ressources du cours

### Cours magistraux (CM)

| Document | Description |
|----------|-------------|
| [CM : Fondamentaux et architecture hexagonale](export/CM1_Fondamentaux_architecture.pdf) | Pourquoi l'architecture ? Principes fondamentaux • Architecture hexagonale |

### Travaux dirigés

**Guides généraux** :
- [📖 Guide de démarrage](td/guides/demarrage.md) ⚠️ **À suivre AVANT le TD0**
- [🔄 Workflow de développement](td/guides/workflow_de_developpement.md)
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

### Travaux dirigés (TD0-TD4)

| TD | Titre | Contenu |
|----|-------|---------|
| **TD0** | Prise en main | Environnement Python, FastAPI, pytest |
| **TD1** | Modélisation du domaine | Entités (Ticket, User), Value Objects, règles métier |
| **TD2** | Use cases et ports | Cas d'usage, ports entrants et sortants |
| **TD3** | Adapters persistance | Repository abstrait + implémentation SQLite |
| **TD4** | API REST | Adapter FastAPI, tests d'intégration |

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
