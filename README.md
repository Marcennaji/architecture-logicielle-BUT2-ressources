# Syllabus — R4.01 Architecture logicielle (BUT2)

## 🎯 Objectifs du module

- Comprendre **pourquoi** l'architecture logicielle est essentielle
- Maîtriser les **principes fondamentaux** d'une bonne architecture : cohésion, couplage, dépendances, inversion de dépendances.
- Connaître les principales **familles d'architectures** (monolithe, N-tiers, MVC, microservices, event-driven, hexagonale…).
- Savoir **structurer une application** selon l'architecture hexagonale (Ports & Adapters).
- Mettre en œuvre une architecture hexagonale sur un **projet fil rouge**.
- Travailler avec des **briques logicielles existantes** (framework web, ORM, services web, etc.).

## 📌 Projet fil rouge

- Sujet : **Gestionnaire de tickets / workflow** (type Trello / Jira minimal).
- Réalisé au fil des TD/TP (~70h).
- Dépôt propre à chaque étudiant, créé à partir d'un **bootstrap** commun.
- Les TD servent de **guides de progression**.

## 📚 Ressources du cours

| Document | Description |
|----------|-------------|
| `cm/CM1_Fondamentaux_architecture.md` | Fondamentaux de l'architecture logicielle |
| `cm/CM2_architecture_hexagonale.md` | Architecture hexagonale (Ports & Adapters) |
| `cm/architectures_reference.md` | Fiches de référence sur les architectures (à consulter) |

> 📁 Les **guides des TD** (TD0 à TD7) se trouvent dans le **repo bootstrap du projet** (ticketing).

## 🗓 Planning indicatif

### Cours magistraux (2 × 2h)

| CM | Titre | Contenu |
|----|-------|---------|
| **CM1** | Fondamentaux de l'architecture | Pourquoi l'architecture ? • Architecture à l'ère de l'IA • Principes (cohésion, couplage, dépendances) • Panorama des architectures |
| **CM2** | Architecture hexagonale | Ports & Adapters • Domain / Application / Adapters • Exemples de code • Tests • Comparaison avec Clean/MVC |

### Travaux dirigés

| TD | Titre | Contenu |
|----|-------|---------|
| **TD0** | Prise en main | Environnement Python, FastAPI, pytest |
| **TD1** | Modélisation du domaine | Entités (Ticket, User), Value Objects, règles métier |
| **TD2** | Use cases et ports | Cas d'usage, ports entrants et sortants |
| **TD3** | Adapters persistance | Repository abstrait + implémentation SQLite |
| **TD4** | API REST | Adapter FastAPI, tests d'intégration |
| **TD5** | Authentification | JWT, rôles, sécurité |
| **TD6** | Tests et CI | Couverture, refactoring, intégration continue |
| **TD7** | Extensions | Notifications, métriques, événements (bonus) |

Ce planning est volontairement souple : chaque TD indique ce qui est **prioritaire** et ce qui relève du **bonus**.

## 💡 Message clé du module

> **L'IA est une excellente codeuse, pas (encore) une ingénieure logicielle.**
>
> Un *codeur* maîtrise un langage et produit du code qui fonctionne.  
> Un *ingénieur logiciel* conçoit des systèmes cohérents, maintenables, évolutifs.
>
> **Ce cours vise à faire de vous des ingénieurs, pas juste des codeurs assistés par IA.**

## 📖 Références

- **Clean Architecture** — Robert C. Martin
- **Domain-Driven Design** — Eric Evans
- **Building Microservices** — Sam Newman
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation pytest](https://docs.pytest.org/)
