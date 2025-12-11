# Critères d'évaluation - R4.01 Architecture Logicielle

> 💡 Cette grille détaille les **modalités d'évaluation** du module. La note finale combine projet, travail en TD, et examen.

## 📊 Répartition de la note finale (sur 20)

| Composant | Poids | Description |
|-----------|-------|-------------|
| **Projet** | 8/20 (40%) | Code du ticketing system (travail à la maison) |
| **Travail en TD** | 8/20 (40%) | Exercices pratiques chronométrés (présentiel) |
| **Participation** | 2/20 (10%) | Présence active et engagement en TD |
| **Examen final** | 2/20 (10%) | QCM/questions sur les concepts |

---

## 🤖 Utilisation des assistants IA

### ✅ Autorisée pour le projet (à la maison)

Vous **pouvez** utiliser des assistants IA (ChatGPT, Claude, GitHub Copilot, etc.) pour :
- Générer du code
- Comprendre des concepts
- Débugger des erreurs
- Améliorer votre code

**Pourquoi ?** Parce qu'en 2025, savoir **utiliser efficacement** les IA fait partie des compétences attendues d'un développeur.

**⚠️ Attention** : L'IA ne vous garantit PAS une bonne note si vous ne comprenez pas ce qu'elle génère. Les exercices en TD (40% de la note) se font **sans IA** et révèlent votre vraie compréhension.

### 🚫 Bloquée pendant les TD (présentiel)

En salle de TD, l'accès aux assistants IA est **bloqué par le proxy réseau**. Vous devrez :
- Écrire le code vous-même
- Résoudre les problèmes en autonomie
- Mobiliser vos connaissances du cours

**C'est là qu'on évalue votre compréhension réelle.**

---

## 📦 Évaluation du projet (8/20)

### Architecture & découpage (3 pts)
- Respect de l'architecture hexagonale (Ports & Adapters)
- Séparation claire entre Domain / Application / Ports / Adapters
- Respect de la règle de dépendance (flux entrant uniquement)
- Clarté du code et lisibilité

### Fonctionnalités (2.5 pts)
- CRUD tickets (création, lecture, mise à jour, suppression)
- Assignation de tickets
- Transitions de statut (ouverture, résolution, clôture)
- Validation des règles métier

### Tests (2 pts)
- Tests unitaires du domaine (entités, règles métier)
- Tests unitaires des use cases (orchestration)
- Tests d'intégration API (end-to-end)

### Bonnes pratiques (0.5 pt)
- Messages de commits clairs et cohérents
- README complet et à jour
- Code formaté (pre-commit hooks)

### Bonus (0-1 pt)
- Authentification JWT, notifications, audit logs
- Adapters supplémentaires (Redis, monitoring)
- Qualité exceptionnelle du code

---

## 🎯 Évaluation des TD (8/20)

**6 exercices pratiques** réalisés en présentiel (TD1 à TD6) :
- Durée : 30 min à 1h30 selon la complexité
- Notation : ~1-1.5 pts par exercice
- Format : code à écrire sur votre machine, commit à la fin
- **Sans accès IA**

**Exemples d'exercices** :
- TD1 : Ajouter une méthode `Ticket.reopen()` avec tests
- TD2 : Implémenter le use case `AssignTicket`
- TD3 : Créer l'adapter SQLite pour `UserRepository`
- TD4 : Ajouter l'endpoint API `/tickets/{id}/comments`

**L'enseignant passe dans les rangs, vérifie votre code, et note en direct.**

---

## 🎯 Simulation de notes

### Étudiant "IA only" (vient peu en TD)
- Projet : 6-7/8 (IA génère du bon code)
- TD : 2-3/8 (absent ou en difficulté sans IA)
- Participation : 0.5/2
- Examen : 0.5/2
- **Total : 9-11/20** ❌ Module non validé

### Étudiant assidu (comprend les concepts)
- Projet : 5-6/8 (code correct, même avec aide IA)
- TD : 6-7/8 (réussit les exercices en autonomie)
- Participation : 1.5-2/2
- Examen : 1.5-2/2
- **Total : 14-17/20** ✅ Module validé

**Moralité** : L'IA peut aider pour le projet, mais ne remplace pas la compréhension pour les TD et l'examen.

---

## 🎯 Attentes par niveau (projet seul)

### Socle minimal (> 4/8)
- Architecture hexagonale respectée (Domain pur, Ports, Adapters)
- CRUD tickets fonctionnel via API
- Repository SQLite opérationnel
- Tests de base présents (au moins domain + 1 test e2e)

### Bon niveau (5-6/8)
## ❓ Questions fréquentes

### Puis-je utiliser ChatGPT/Claude pour le projet ?
**Oui, totalement.** Les IA font partie des outils modernes de développement. Mais attention : si vous ne comprenez pas le code généré, vous serez en difficulté en TD.

### Comment réussir les TD sans IA ?
En **pratiquant** régulièrement et en **comprenant** ce que vous faites. L'IA peut écrire du code, mais ne peut pas apprendre à votre place.

### Si j'utilise l'IA, aurai-je 20/20 ?
**Non.** Un étudiant qui utilise l'IA sans comprendre :
- Projet : ~6-7/8 (code fonctionnel mais générique)
- TD : ~2-3/8 (bloqué sans IA en présentiel)
- **Total : ~9-11/20** → Module non validé

### Dois-je tout implémenter dans le projet ?
Non. Le **socle minimal** (CRUD + tests) suffit. Les bonus sont optionnels.

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

### L'examen final est-il difficile ?
Non. Ce sont des **questions de compréhension** (pas de code à écrire) :
- "Pourquoi séparer domain et adapters ?"
- "Qu'est-ce qu'un port ? Donnez un exemple"
- "Quel est le rôle de l'application layer ?"

Si vous avez suivi les TD, c'est facile.

### TD
- **Format** : Exercices chronométrés en présentiel
- **Durée** : 30 min à 1h30 selon complexité
- **Notation** : En direct par l'enseignant
- **IA bloquée** : Oui, par le proxy réseau

### Examen final
- **Format** : QCM + questions courtes
- **Durée** : 1h
- **Contenu** : Concepts d'architecture, principes hexagonaux, choix de design

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
