# Critères d'évaluation - R4.01 Architecture Logicielle

## 📊 Composantes de l'évaluation

1. **Projet ticketing** - Résultat final en fin de module
2. **Contrôle en présentiel** - 2h sans IA sur machine IUT  
3. **Travail en TD** - (NB. les TD ne sont pas corrigés individuellement)

**Barèmes détaillés communiqués en début de module.**

---

## 🤖 Utilisation des assistants IA

### ✅ Autorisée pour le projet
- Générer du code, comprendre des concepts, débugger
- **Mais** : vous devez comprendre ce que l'IA génère

### 🚫 Bloquée pendant le contrôle
- Proxy réseau IUT bloque l'accès IA
- Vous codez en autonomie → évalue votre vraie compréhension

---

## 📦 Projet final : Critères d'évaluation

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

**20h présentiel** : TD0 (2h) + TD1 (4h) + TD2 (4h) + TD3 (4h) + TD4 (4h)

**Workflow** : Branche → PR → Auto-validation via checklists → Merge

**Pas de correction individuelle** : Utilisez les checklists pour vous auto-évaluer.

---

## 📝 Contrôle final

**Durée** : 2h | **Support** : Machine IUT sans IA | **Rendu** : Push GitHub

**Format** :
- Analyse de code (identifier violations architecturales)
- Refactoring (restructurer selon principes hexagonaux)
- Questions de compréhension

---

## ✅ Conseils

**TDs** : Comprenez les concepts, testez, posez des questions  
**Projet** : Itérez, refactorez, utilisez l'IA pour apprendre (pas copier)  
**Contrôle** : Révisez concepts, refaites TDs sans IA, analysez du code

---

## ❓ FAQ

**IA autorisée pour le projet ?** Oui, mais vous devez comprendre le code généré.

**Réussir sans IA ?** Pratiquez et comprenez. L'IA ne remplace pas l'apprentissage.

**IA intensive sans maîtrise ?** Projet OK mais échec au contrôle → module non validé.

**Socle minimal ?** CRUD + tests + architecture hexagonale.

**TDs corrigés ?** Non. Auto-évaluation via checklists PR.

**Contrôle difficile ?** Non si vous avez compris l'architecture.
