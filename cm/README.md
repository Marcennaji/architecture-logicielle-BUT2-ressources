# Cours magistraux (CM)

## 📚 Structure du module

Le module R4.01 Architecture logicielle comporte **1 cours magistral de 2h** suivi de **10 séances de TD** (20h).

### CM unique : Fondamentaux et architecture hexagonale

**Durée** : 2 heures

**Contenu** :
1. Pourquoi l'architecture logicielle ?
2. Architecture à l'ère de l'IA (message clé 🤖)
3. Principes fondamentaux :
   - Cohésion
   - Couplage
   - Gestion des dépendances
   - Séparation des responsabilités
   - Inversion de dépendances
4. Architecture hexagonale (Ports & Adapters)
5. Présentation du projet ticketing

**Fichier** : [CM1_Fondamentaux_architecture.md](CM1_Fondamentaux_architecture.md)

---

## 📖 Documents de référence

| Document | Description |
|----------|-------------|
| [CM1_Fondamentaux_architecture.md](CM1_Fondamentaux_architecture.md) | Cours principal (slides Marp) |
| [architectures_reference.md](architectures_reference.md) | Panorama des principales architectures (lecture autonome) |

---

## 🔄 Export des slides

Les slides Marp sont exportés en HTML et PDF via :

```bash
cd /chemin/vers/architecture-logicielle-BUT2-ressources
./scripts/export_slides.sh
```

Les fichiers exportés sont disponibles dans `export/`.
