# Critères d'évaluation - R4.01 Architecture Logicielle

> 💡 Cette grille détaille les **modalités d'évaluation** du module. La note finale combine projet, travail en TD, et examen.

## 📊 Répartition de la note finale (sur 20)

| Composant | Poids | Description |
|-----------|-------|-------------|
| **Projet final** | 6/20 (30%) | Code du ticketing system complet (livraison fin de module) |
| **Travaux en TD** | 8/20 (40%) | Exercices pratiques chronométrés (présentiel, sans IA) |
| **Contrôle final** | 6/20 (30%) | Analyse de code - Diagnostic architectural (fin de module, après TD4) |

---

## 🤖 Utilisation des assistants IA

### ✅ Autorisée pour le projet (à la maison)

Vous **pouvez** utiliser des assistants IA (ChatGPT, Claude, GitHub Copilot, etc.) pour :
- Générer du code
- Comprendre des concepts
- Débugger des erreurs
- Améliorer votre code

**Pourquoi ?** Parce qu'en 2025, savoir **utiliser efficacement** les IA fait partie des compétences attendues d'un développeur.

**⚠️ Attention** : L'IA ne vous garantit PAS une bonne note si vous ne comprenez pas ce qu'elle génère. Les travaux en TD (40%) et le contrôle final (30%) se font **sans IA** et révèlent votre vraie compréhension.

### 🚫 Bloquée pendant les TD (présentiel)

En salle de TD, l'accès aux assistants IA est **bloqué par le proxy réseau**. Vous devrez :
- Écrire le code vous-même
- Résoudre les problèmes en autonomie
- Mobiliser vos connaissances du cours

**C'est là qu'on évalue votre compréhension réelle.**

---

## 📦 Évaluation du projet final (6/20)

### Architecture & découpage (2.5 pts)
- Respect de l'architecture hexagonale (Ports & Adapters)
- Séparation claire entre Domain / Application / Ports / Adapters
- Respect de la règle de dépendance (flux entrant uniquement)
- Clarté du code et lisibilité

### Fonctionnalités (2 pts)
- CRUD tickets (création, lecture, mise à jour, suppression)
- Assignation de tickets
- Transitions de statut (ouverture, résolution, clôture)
- Validation des règles métier

### Tests (1.5 pt)
- Tests unitaires du domaine (entités, règles métier)
- Tests unitaires des use cases (orchestration)
- Tests d'intégration API (end-to-end)

### Bonus (0-1 pt)
- Extensions architecturales pertinentes
- Qualité exceptionnelle du code
- Messages de commits clairs, README complet, code formaté
- Tests particulièrement exhaustifs

---

## 🎯 Évaluation des TD (8/20)

### Format des TDs

**Module complet** : TD0 à TD4 sur 20h de présentiel (10 séances × 2h)

Répartition :
- **TD0** (2h) : Prise en main - Workflow Git/GitHub
- **TD1** (4h) : Domain - Entités et règles métier
- **TD2** (4h) : Use cases et ports - Architecture hexagonale
- **TD3** (4h) : Repository SQLite - Persistence
- **TD4** (6h) : API REST - Endpoints FastAPI

À la **fin de chaque TD** (sauf TD0), un **exercice noté** valide vos acquis :
- Durée : 30 min à 1h30
- Contexte : En présentiel, **sans accès IA**
- Notation : ~2 pts par exercice (4 exercices = 8 pts total)

### 📋 Modalités de rendu

**Pendant la séance d'évaluation** :

1. L'enseignant annonce l'exercice et la **deadline** (ex: 16h30)
2. Vous créez une branche dédiée (ex: `td3-exercice`)
3. Vous codez, testez, commitez
4. Vous pushez **avant la deadline**

**⚠️ IMPORTANT** : Seuls les commits **dans la fenêtre horaire** sont évalués.

```bash
# Exemple : exercice du TD3 le 15/01/2025 de 15h30 à 16h30
git checkout -b td3-exercice
# ... vous codez ...
git add .
git commit -m "feat(td3): ajout CommentRepository SQLite"
git push origin td3-exercice
# ⏰ Commit AVANT 16h30 impératif !
```

**Notation** : L'enseignant récupère vos commits via leur **timestamp** et évalue le code en différé.

### Exemples d'exercices notés

- **Fin TD1** (Domain) : "Ajoutez la méthode `Ticket.reopen()` avec tests" (30 min)
- **Fin TD2** (Use cases) : "Implémentez le use case `GetTicketById`" (45 min)
- **Fin TD3** (SQLite) : "Ajoutez la persistance pour `User`" (1h)
- **Fin TD4** (API REST) : "Créez l'endpoint `PATCH /tickets/{id}/status`" (1h)

### ⚖️ Règles

- ✅ Commit dans les temps → Évalué normalement
- ⏰ Commit hors délai (> 5 min) → Pénalité -50%
- ❌ Commit hors délai (> 30 min) → 0/2
- 🚫 Absence non justifiée → Exercice de rattrapage à faire

---

## 📝 Contrôle final - Analyse de code (6/20)

### Format

**Quand** : Fin de module (après TD4)

**Durée** : 45 minutes

**Support** : Moodle (questions à réponse courte/texte libre)

**Contexte** : Sans IA, sans documentation (seules vos connaissances)

### Structure de l'épreuve

Vous analysez **3 extraits de code Python** présentant des problèmes architecturaux.

Pour chaque extrait (2 points) :
1. **Diagnostic** (0.75 pt) : Identifier le(s) problème(s) architectural/architecturaux
2. **Correction** (1.25 pt) : Proposer une solution respectant l'architecture hexagonale

**Barème détaillé :**

#### Exercice 1 : Violation de la règle de dépendance (2 pts)
- **Contexte** : Code du domain important directement SQLAlchemy ou FastAPI
- **Diagnostic** (0.75 pt) :
  - 0.75 pt : Identifie clairement la violation ("le domain dépend de l'infrastructure")
  - 0.5 pt : Identifie partiellement ("problème d'import")
  - 0 pt : N'identifie pas le problème
- **Correction** (1.25 pt) :
  - 1.25 pt : Propose une solution complète (port + adapter, inversion de dépendance)
  - 0.75 pt : Solution partielle (retire l'import mais ne propose pas d'alternative)
  - 0.25 pt : Vague ("il faut séparer les couches")
  - 0 pt : Pas de solution ou solution incorrecte

#### Exercice 2 : Logique métier dans l'adapter (2 pts)
- **Contexte** : Repository ou API router contenant de la logique métier
- **Diagnostic** (0.75 pt) :
  - 0.75 pt : "La logique métier doit être dans le domain, pas dans l'adapter"
  - 0.5 pt : "Ce code n'est pas au bon endroit"
  - 0 pt : Ne voit pas le problème
- **Correction** (1.25 pt) :
  - 1.25 pt : Déplace la logique dans le domain (méthode d'entité ou use case)
  - 0.75 pt : Identifie où déplacer mais sans préciser comment
  - 0.25 pt : Solution floue
  - 0 pt : Pas de solution

#### Exercice 3 : Use case couplé à l'infrastructure (2 pts)
- **Contexte** : Use case qui instancie directement un repository SQLite ou appelle des détails SQL
- **Diagnostic** (0.75 pt) :
  - 0.75 pt : "Le use case ne doit pas connaître les détails d'implémentation du repository"
  - 0.5 pt : "Trop de couplage"
  - 0 pt : Ne détecte pas le problème
- **Correction** (1.25 pt) :
  - 1.25 pt : Injection de dépendance via port (interface abstraite)
  - 0.75 pt : Mentionne l'injection de dépendance sans détailler
  - 0.25 pt : "Utiliser une interface"
  - 0 pt : Pas de solution

**Total : 6 points**

### Exemples de problèmes à identifier

- ❌ Domain qui importe `sqlalchemy`, `fastapi`, `requests`
- ❌ Entité avec méthodes `.save()` ou `.delete()` (responsabilité du repository)
- ❌ Use case qui construit des requêtes SQL directement
- ❌ API router avec validation métier (devrait être dans le domain)
- ❌ Repository avec logique de calcul métier
- ❌ Dépendances circulaires entre couches
- ❌ Adapter qui connaît les détails du domain au lieu de passer par un port

### Critères de réussite

- **Excellent (5-6/6)** : Diagnostique précis + solutions complètes et justifiées
- **Bon (3.5-4.5/6)** : Identifie les problèmes + solutions partielles ou imprécises
- **Passable (2-3/6)** : Détecte certains problèmes mais solutions vagues
- **Insuffisant (< 2/6)** : Ne détecte pas les violations ou solutions incorrectes

### Conseils de préparation

1. **Relisez votre code de projet** : Où avez-vous mis chaque responsabilité ?
2. **Révisez les principes** : Règle de dépendance, séparation des couches
3. **Pratiquez l'analyse** : Prenez des exemples de code et demandez-vous "Qu'est-ce qui cloche ?"
4. **Connaissez les patterns** : Repository, Use Case, Dependency Injection

---

## ⏱️ Charge de travail et utilisation de l'IA

### Temps de travail attendu

**En présentiel (obligatoire)** : 20h de TD réparties sur 10 séances

**À la maison** :
- Avec IA (utilisation intelligente) : **8-10h**
- Sans IA ou IA mal utilisée : **15-20h**

**Total réaliste** : ~30h de travail étudiant (présentiel + maison)

### Comment utiliser l'IA efficacement

✅ **Bon usage de l'IA** :
- Générer du code boilerplate (dataclasses, schémas Pydantic)
- Comprendre des erreurs ou des concepts
- Accélérer l'écriture de tests simples
- **Puis** : Lire, comprendre, adapter, tester le code généré

❌ **Mauvais usage de l'IA** :
- Copier-coller sans comprendre
- Ne pas tester le code généré
- Ignorer les erreurs et redemander du code
- Croire que l'IA connaît l'architecture de VOTRE projet

### Pourquoi l'IA ne suffit pas

**L'IA accélère le coding (~50%)** mais ne remplace PAS :
- ❌ La compréhension architecturale (où mettre ce code ?)
- ❌ Le debugging (pourquoi ce test échoue ?)
- ❌ L'adaptation au contexte du projet

**70% de votre note** (TD + Contrôle) se passe **sans IA** → Impossible de valider le module en trichant.

### Conseils pratiques

1. **En TD** : Codez vous-même, posez des questions, comprenez
2. **À la maison** : Utilisez l'IA pour accélérer, mais relisez tout
3. **Avant le contrôle** : Révisez les principes architecturaux, pratiquez l'analyse de code
4. **Projet final** : Code fonctionnel > Code parfait

---

## 🎯 Simulation de notes

### Étudiant "IA only" (vient peu en TD)
- Projet final : 5/6 (IA génère du bon code)
- TD : 2-3/8 (absent ou en difficulté sans IA)
- Contrôle final : 0.5-1/6 (ne comprend pas l'architecture)
- **Total : 7.5-10/20** ❌ Module non validé

### Étudiant assidu (comprend les concepts)
- Projet final : 4-5/6 (code correct, même avec aide IA)
- TD : 6-7/8 (réussit les exercices en autonomie)
- Contrôle final : 4-5/6 (diagnostique bien, propose des solutions)
- **Total : 14-17/20** ✅ Module validé

**Moralité** : L'IA peut aider pour le projet (30%), mais ne remplace pas la compréhension pour les TD (40%) et le contrôle (30%).

---

## 🎯 Attentes par niveau (projet seul)

### Socle minimal (> 3/6)
- Architecture hexagonale respectée (Domain pur, Ports, Adapters)
- CRUD tickets fonctionnel via API
- Repository SQLite opérationnel
- Tests de base présents (au moins domain + 1 test e2e)

### Bon niveau (4-5/6)
- Socle + transitions de statut correctes
- Couverture de tests satisfaisante (domain + application + e2e)
- Code propre et lisible
- Commits réguliers et messages clairs

### Excellent niveau (6/6 + bonus)
- Tout le socle impeccable
- Tests exhaustifs avec bonne couverture
- Code exemplaire (nommage, découpage, documentation)
- Extensions architecturales pertinentes (si implémentées)

## ❓ Questions fréquentes

### Puis-je utiliser ChatGPT/Claude pour le projet ?
**Oui, totalement.** Les IA font partie des outils modernes de développement. Mais attention : si vous ne comprenez pas le code généré, vous serez en difficulté en TD.

### Comment réussir les TD sans IA ?
En **pratiquant** régulièrement et en **comprenant** ce que vous faites. L'IA peut écrire du code, mais ne peut pas apprendre à votre place.

### Si j'utilise intensivement l'IA sans vraiment maitriser les concepts, puis-je valider le module ?
**Non.** Un étudiant qui utilise l'IA sans comprendre :
- Projet : ~5/6 (code fonctionnel mais générique)
- TD : ~2-3/8 (bloqué sans IA en présentiel)
- Contrôle : ~0.5-1/6 (ne sait pas analyser le code)
- **Total : ~7.5-10/20** → Module non validé

### Dois-je tout implémenter dans le projet ?
Non. Le **socle minimal** (CRUD + tests + architecture hexagonale) suffit pour valider le module. Les extensions sont optionnelles et valorisées dans la note bonus.

### Comment sont notés les tests ?
- Présence de tests : ✅
- Tests pertinents (testent réellement le comportement) : ✅✅
- Bonne couverture (domain + application + e2e) : ✅✅✅

### Puis-je modifier l'architecture proposée ?
Oui, tant que vous respectez les **principes** de l'architecture hexagonale (séparation des couches, inversion de dépendances).

### Que se passe-t-il si je rate un TD ?
- 1 absence : Rattrapable (exercice équivalent à faire)
- 2+ absences : Impact significatif sur la note (TD = 40%)
- **Conseil** : Venez en TD, c'est là que vous apprenez vraiment.

### Le contrôle final est-il difficile ?
Non, si vous avez **compris** l'architecture. Ce n'est pas un piège :
- Vous analysez du code Python simple
- Les problèmes sont des violations classiques (domain qui importe SQLAlchemy, etc.)
- Vous devez juste **expliquer** ce qui cloche et **comment** le corriger

Si vous avez suivi les TD et compris pourquoi on structure le code ainsi, c'est accessible.

## ❓ Questions fréquentes

### Dois-je tout implémenter ?
Non. Le **socle minimal** suffit pour valider le module. Les modules additionnels sont pour aller plus loin.

### Comment sont notés les tests ?
- Présence de tests : ✅
- Tests pertinents (testent réellement le comportement) : ✅✅
- Bonne couverture (domain + application + e2e) : ✅✅✅

### Puis-je modifier l'architecture proposée ?
Oui, tant que vous respectez les **principes** de l'architecture hexagonale (séparation des couches, inversion de dépendances).

### Le code doit-il être parfait ?
Non. On évalue :
- Votre **compréhension** de l'architecture
- Votre capacité à **structurer** le code
- La **cohérence** de votre implémentation

Pas la perfection absolue. C'est un projet pédagogique, pas un produit en production.
