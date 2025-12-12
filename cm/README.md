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
| [architectures_reference.md](architectures_reference.md) | Panorama détaillé des architectures (lecture autonome) |
| [CM1_architectures_modernes.md](CM1_architectures_modernes.md) | Version alternative du CM1 (focus architectures modernes) |

**Fichiers archivés** :
- `CM2_architecture_hexagonale.md.archived` : Ancien CM2 fusionné dans CM1

---

## 🎯 Rationale : Pourquoi 1 seul CM ?

**Avant** : 2 CM × 2h (CM1 fondamentaux + CM2 hexagonale)
- Total : 4h de cours + 16h de TD
- Problème : Peu de temps pour la pratique

**Maintenant** : 1 CM × 2h (fondamentaux + hexagonale condensée)
- Total : 2h de cours + 20h de TD
- Avantages :
  - ✅ +2h de pratique en TD
  - ✅ Cohérence : tout le contexte théorique en une fois
  - ✅ Les étudiants voient l'hexagonal AVANT de coder (TD1-TD4)
  - ✅ Moins de redondance (l'hexagonal sera vu en pratique dans les TDs)

**Compromis** :
- Le panorama des architectures (monolithe, microservices, MVC...) est renvoyé au document de référence
- L'essentiel est concentré sur ce qui sera pratiqué : l'architecture hexagonale

---

## 🔄 Export des slides

Les slides Marp sont exportés en HTML et PDF via :

```bash
cd /chemin/vers/architecture-logicielle-BUT2-ressources
./scripts/export_slides.sh
```

Les fichiers exportés sont disponibles dans `export/`.
