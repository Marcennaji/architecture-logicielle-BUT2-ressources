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

**18h TD** : TD0 (2h) + TD1 (4h) + TD2 (4h) + TD3 (4h) + TD4 (4h)

**Workflow** : Commits réguliers sur `main` → Tag standardisé pour soumettre (TD1, TD2, TD3, TD4)

**Soumission** : Quand vous avez terminé un TD, créez un tag Git avec le nom exact (`TD1`, `TD2`, etc.) et poussez-le sur GitHub.

**Évaluation** : Chaque TD est évalué. L'enseignant reste disponible si vous rencontrez des difficultés pendant les séances.

**Bonus présentiel** : Le travail effectué et soumis pendant les séances TD est valorisé.

**Commits réguliers encouragés** : Faites plusieurs petits commits pour chaque TD, au fur et à mesure de votre progression. Assurez vous que vos tests passent en local, avant de committer.

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

**Comment sont évalués les TDs ?** Chaque TD est noté. Les modalités précises sont communiquées en début de module.

**QCM difficile ?** Non si vous avez compris l'architecture et suivi les TD.

**Bonus présentiel ?** Oui, le travail effectué pendant les séances TD est valorisé dans la note finale.
