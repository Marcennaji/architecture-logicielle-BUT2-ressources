# Critères d'évaluation - R4.01 Architecture Logicielle

## 📊 Composantes de l'évaluation

**Note finale du module = (Note TDs × 0.8) + (Note QCM × 0.2)**

1. **Travail en TD (80%)** - 10 jalons de 2h évalués via tags Git sur GitHub
2. **QCM final (20%)** - 30-45 mn en dernière séance (correction automatique)

**Bonus présentiel** : Coefficient de 0.7 à 1.0 appliqué sur chaque jalon selon le travail en présentiel

---

## 🤖 Utilisation des assistants IA

### ✅ Autorisée pour le projet (hors présentiel)
- Générer du code, comprendre des concepts, débugger
- **Mais** : vous devez comprendre ce que l'IA génère

### 🚫 Interdite pendant les séances de TD
- L'IA n'est **pas autorisée en présentiel** (salles de TD)
- Le travail avec IA se fait donc **en dehors des séances**
- ⚠️ **Conséquence** : coefficient réduit (0.7 vs 1.0 en présentiel)
- 📊 Voir le [tableau des coefficients](evaluation_jalons.md#1-coefficient-présentiel)

### 🚫 Bloquée pendant le QCM
- Proxy réseau IUT bloque l'accès IA
- Vous répondez en autonomie → évalue votre vraie compréhension

---

## 📦 Projet ticketing : Critères d'évaluation

Chaque jalon est évalué selon des critères objectifs répartis en 4 catégories :

### Tronc commun (tous les jalons)

**1. Architecture hexagonale**
- ✅ Le domaine ne dépend d'aucune librairie technique (FastAPI, SQLite, etc.)
- ✅ Les dépendances pointent vers l'intérieur (adapters → application → domain)
- ✅ Les responsabilités sont clairement séparées (domain / application / adapters)
- ✅ Les ports (interfaces) sont définis dans le domaine, implémentés dans les adapters

**2. Tests**
- ✅ Tous les tests passent (`pytest` en vert)
- ✅ Les règles métier sont testées sans infrastructure (tests unitaires du domain)
- ✅ Les tests ne dépendent pas d'un serveur web ou d'une vraie base de données
- ✅ Les tests sont lisibles et vérifient un comportement précis

**3. Qualité du code**
- ✅ Code formaté (pre-commit hook passé sans erreur)
- ✅ Noms de variables/fonctions explicites
- ✅ Pas de code commenté inutile
- ✅ Messages de commits clairs et descriptifs

**4. Fonctionnalités spécifiques au TD**
Les fonctionnalités à implémenter obligatoirement sont variables, selon le jalon (entités, use cases, adapters, API, etc.)
Elles seront détaillées dans chaque énoncé de TD

> 💡 Chaque critère non respecté entraîne une réduction de points selon un barème établi.

---

## 🎯 Travail en TD

**20h TD** : 10 séances de 2h, chacune constituant un jalon évaluable indépendant

**Système de jalons** : Chaque séance de 2h = 1 livrable avec son propre tag Git

> 📋 **Liste des jalons** : Voir [README.md](README.md#-liste-des-tds)  
> **Système d'évaluation** : Voir [evaluation_jalons.md](evaluation_jalons.md)

**Workflow** : 
1. Commitez régulièrement pendant la séance (≥ 3 commits répartis)
2. Poussez le tag avant la fin de la séance
3. Tests passants obligatoires

**Bonus présentiel** : le coefficient maximum ne peut s'obtenir que via un travail effectué en présentiel.

Voir le tableau complet des coefficients dans [evaluation_jalons.md](evaluation_jalons.md).

---

## 📝 QCM final

**Durée** : 30-45 mn | **Support** : Machine IUT sans IA | **Correction** : Automatique

**Format** :
- Questions de compréhension sur les principes fondamentaux d'une bonne architecture, valables quelle que soit l'architecture
- Questions de compréhension sur les principes spécifiques à l'architecture hexagonale
- Analyse de code (identifier des violations architecturales)

---

## ✅ Conseils

**TDs** : Comprenez les concepts, testez, posez des questions  
**Projet** : Itérez, refactorez, utilisez l'IA pour apprendre (pas copier)  
**QCM** : Révisez concepts, refaites TDs, analysez du code

---

## ❓ FAQ

**IA autorisée pour le projet ?** Oui, mais vous devez comprendre le code généré.

**Réussir sans IA ?** Pratiquez et comprenez. L'IA ne remplace pas l'apprentissage.

**IA intensive sans maîtrise ?** Projet peut-être OK (avec une note minorée), mais échec au QCM → module non validé.

**Comment sont évalués les TDs ?** Chaque jalon de 2h est évalué avec un coefficient de bonus selon les commits pendant la séance. Voir [evaluation_jalons.md](evaluation_jalons.md) pour les détails.

**QCM difficile ?** Non si vous avez compris l'architecture et suivi les TD.

**Bonus présentiel ?** Oui, chaque jalon reçoit un coefficient de 0.7 ou 1.0. Le coefficient 1.0 est obtenu en travaillant en présentiel avec au moins 3 commits et le tag poussé pendant la séance. Voir [evaluation_jalons.md](evaluation_jalons.md) pour le barème complet.
