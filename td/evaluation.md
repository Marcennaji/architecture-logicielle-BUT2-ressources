# Critères d'évaluation - R4.01 Architecture Logicielle

## 📊 Composantes de l'évaluation

1. **Travail en TD** (TD1-TD4) - Soumission via tags Git sur GitHub
2. **QCM final** - 30-45 mn en dernière séance (correction automatique)
3. **Bonus présentiel** - Travail soumis pendant séances TD valorisé

**Barèmes détaillés communiqués en début de module.**

---

## 🤖 Utilisation des assistants IA

### ✅ Autorisée pour le projet
- Générer du code, comprendre des concepts, débugger
- **Mais** : vous devez comprendre ce que l'IA génère

### 🚫 Bloquée pendant le QCM
- Proxy réseau IUT bloque l'accès IA
- Vous répondez en autonomie → évalue votre vraie compréhension

---

## 📦 Projet ticketing : Critères d'évaluation

**Architecture**
- Séparation Domain / Application / Ports / Adapters
- Règle de dépendance respectée
- Inversion de dépendances

**Fonctionnalités**
- CRUD tickets + gestion statuts
- Persistence SQLite + API REST

**Tests**
- Unitaires (domain, use cases)
- Intégration (API)

**Qualité**
- Code lisible, bien structuré
- Commits clairs, README complet

---

## 🎯 Travail en TD

**18h TD** : 10 séances de 2h, chacune constituant un jalon évaluable indépendant

**Système de jalons** : Chaque séance de 2h = 1 livrable avec son propre tag Git
- TD0 → Tag `TD0`
- TD1a → Tag `TD1-domain` (entités domaine)
- TD1b → Tag `TD1-tests` (tests unitaires)
- TD2a → Tag `TD2-ports` (ports + 1er use case)
- TD2b → Tag `TD2-usecases` (use cases complets)
- TD3a → Tag `TD3-repository` (repository in-memory)
- TD3b → Tag `TD3-sqlite-1` (SQLite connexion/tables)
- TD3c → Tag `TD3-sqlite-2` (SQLite CRUD complet)
- TD4a → Tag `TD4-api` (API REST endpoints)
- TD4b → Tag `TD4-complete` (tests E2E + finalisation)

**📋 Détails complets** : Voir [evaluation_jalons.md](evaluation_jalons.md)

**Workflow** : 
1. Commitez régulièrement pendant la séance (≥ 3 commits répartis)
2. Poussez le tag avant la fin de la séance
3. Tests passants obligatoires

**Bonus présentiel** : Coefficient de 0.6 à 1.0 selon les commits et le délai de push

Voir le tableau complet des coefficients dans [evaluation_jalons.md](evaluation_jalons.md).

---

## 📝 QCM final

**Durée** : 30-45 mn | **Support** : Machine IUT sans IA | **Correction** : Automatique

**Format** :
- Questions de compréhension sur l'architecture hexagonale
- Analyse de code (identifier violations architecturales)
- Concepts de ports & adapters, inversion de dépendances
- Bonnes pratiques de test

---

## ✅ Conseils

**TDs** : Comprenez les concepts, testez, posez des questions  
**Projet** : Itérez, refactorez, utilisez l'IA pour apprendre (pas copier)  
**QCM** : Révisez concepts, refaites TDs, analysez du code

---

## ❓ FAQ

**IA autorisée pour le projet ?** Oui, mais vous devez comprendre le code généré.

**Réussir sans IA ?** Pratiquez et comprenez. L'IA ne remplace pas l'apprentissage.

**IA intensive sans maîtrise ?** Projet peut-être OK, mais échec au QCM → module non validé.

**Comment sont évalués les TDs ?** Chaque jalon de 2h est évalué avec un coefficient de bonus selon les commits pendant la séance. Voir [evaluation_jalons.md](evaluation_jalons.md) pour les détails.

**QCM difficile ?** Non si vous avez compris l'architecture et suivi les TD.

**Bonus présentiel ?** Oui, chaque jalon reçoit un coefficient de 0.6 à 1.0 selon le nombre et la répartition des commits pendant la séance, ainsi que le délai de push du tag. Les étudiants qui travaillent régulièrement sur site et poussent leur tag à temps obtiennent coefficient 1.0. Voir [evaluation_jalons.md](evaluation_jalons.md) pour le barème complet.
