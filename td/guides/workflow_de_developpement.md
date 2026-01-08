# Workflow de développement et rendu

Ce document explique comment organiser votre travail et soumettre vos jalons pour évaluation.

## Principe : Commits réguliers + tags par jalon de 2h

Chaque **séance de 2h** constitue un **jalon évalué indépendamment** avec son propre tag Git. Vous travaillez sur la branche `main` avec des **commits réguliers**, puis vous créez un tag spécifique à la fin de la séance.

```
main
  │
  ├─ commits séance 1 ─→ tag TD0
  │
  ├─ commits séance 2 ─→ tag TD1a
  │
  ├─ commits séance 3 ─→ tag TD1b
  │
  │
  └─ ... (10 jalons au total)
```

> 💡 **Pourquoi cette approche ?** Chaque séance de 2h (i.e, "jalon") est évaluable immédiatement. Cela valorise le travail en présentiel et évite l'accumulation de retard.

> ⚠️ **Support disponible** : Si vous rencontrez des difficultés, **contactez l'enseignant** pendant les séances ou par email. Ne restez pas bloqué !

> ⚠️ **Arborescence obligatoire** : Ne modifiez **JAMAIS** la structure des dossiers principaux (`src/domain/`, `src/application/`, `src/ports/`, `src/adapters/`, `tests/`). Vous pouvez créer des sous-dossiers à l'intérieur, mais l'arborescence de base doit rester identique pour tous.

## Étape par étape

### 1. Développer pendant la séance de 2h

Travaillez sur votre code directement sur `main`. Faites des **commits réguliers** pendant la séance :

```bash
git add .
git commit -m "Add Status enum with lifecycle values"
git push
```

> 💡 **Important** : Faites des commits réguliers pendant la séance de 2h. Cela témoigne de votre engagement et de votre progression pendant les séances de TD.

**Exemples de bonne granularité pour un jalon** :
```bash
# Séance TD1a (2h)
git commit -m "Add Status enum with 4 values"
git commit -m "Add User class with attributes"
git commit -m "Add Ticket class with assign method"
git commit -m "Add business rules validation"
```

### 2. Pousser régulièrement sur GitHub

```bash
git push origin main
```

> 💡 **Conseil** : Poussez vos commits plusieurs fois pendant la séance. Cela sauvegarde votre travail et permet à l'enseignant de suivre votre progression.

### 3. Soumettre le jalon avec un tag

**Avant la fin de la séance de 2h** (ou dans les 10 minutes suivantes), créez et poussez le tag :

```bash
# Vérifier que les tests passent
pytest

# Créer le tag du jalon (nom EXACT requis)
git tag TD1a  # Exemple pour le jalon TD1a

# Pousser le tag sur GitHub
git push origin TD1a
```

> ⚠️ **Attention** : Le nom du tag doit être **exactement** celui indiqué dans le TD (`TD0`, `TD1a`, `TD1b`, etc.).

> 📊 **Évaluation** : Votre engagement pendant les séances de TD est pris en compte dans l'évaluation. Voir [evaluation.md](../evaluation.md) pour les détails.

## Résumé des commandes

| Action | Commande |
|--------|----------|
| Ajouter fichiers | `git add .` |
| Commit | `git commit -m "message"` |
| Push vers GitHub | `git push origin main` |
| Vérifier tests | `pytest` |
| Créer un tag | `git tag TD1a` (voir nom exact dans le TD) |
| Pousser le tag | `git push origin TD1a` |

## Bonnes pratiques

### Messages de commit

Soyez clairs et concis dans vos messages :

**Exemples :**
```
Add Status enum with lifecycle values
Add User class with attributes
Add ticket title validation in __post_init__
Add tests for business rules
Fix assign method to check closed status
```

### Fréquence des commits

- **Minimum : 3 commits** par séance de 2h
- **Idéal : 4-5 commits** répartis régulièrement
- Un commit toutes les 20-30 minutes de travail
- Évitez les commits géants en fin de séance
- **Important** : La répartition temporelle compte pour votre évaluation !

### Structure des dossiers

⚠️ **IMPORTANT** : L'arborescence de base du projet est **obligatoire et identique pour tous** :

```
src/
├── domain/          # ✅ Ne pas renommer/supprimer
├── application/     # ✅ Ne pas renommer/supprimer
├── ports/           # ✅ Ne pas renommer/supprimer
├── adapters/        # ✅ Ne pas renommer/supprimer
│   ├── api/         # ✅ Ne pas renommer/supprimer
│   └── db/          # ✅ Ne pas renommer/supprimer
└── config/          # ✅ Ne pas renommer/supprimer

tests/
├── domain/          # ✅ Ne pas renommer/supprimer
├── application/     # ✅ Ne pas renommer/supprimer
└── e2e/             # ✅ Ne pas renommer/supprimer
```

✅ **Autorisé** : Créer des sous-dossiers à l'intérieur (ex: `src/domain/entities/`, `src/domain/value_objects/`)

❌ **Interdit** : Renommer, déplacer ou supprimer ces dossiers principaux

## FAQ

### Combien de commits minimum par jalon ?

**Minimum : 3 commits** répartis dans le temps pendant la séance de 2h. Idéalement 4-5 commits.

### Quand dois-je pousser le tag ?

**Idéalement pendant ou juste après la séance** pour montrer votre avancement. Vous pouvez aussi le pousser plus tard si vous continuez à travailler chez vous. Voir [evaluation.md](../evaluation.md) pour plus de détails.

### J'ai oublié de pousser le tag pendant la séance, que faire ?

Vous pouvez le pousser plus tard. Le travail régulier en séance est valorisé, mais mieux vaut un tag tardif que pas de tag du tout. Voir [evaluation.md](../evaluation.md).

### Puis-je terminer le jalon chez moi ?

Oui, mais cela n'aura pas le même impact sur votre évaluation. L'objectif est de valoriser le travail en présentiel et la progression pendant les séances.

### J'ai des difficultés sur un jalon, que faire ?

**Ne restez pas bloqué !** Contactez l'enseignant :
- Pendant les séances TD (levez la main)
- Par email avec une description claire du problème
- En incluant le lien vers votre repository GitHub

L'enseignant est là pour vous aider à progresser tout au long du module.

---

## 🎨 Vérifier la qualité du code (optionnel)

Pour détecter automatiquement les violations de conventions Python (PEP 8) avant de committer :

```bash
# Installation (une seule fois)
pip install ruff

# Vérifier le code
ruff check src/domain/

# Corriger automatiquement ce qui peut l'être
ruff check --fix src/
```

**Pourquoi ?** Les conventions Python (noms de classes, variables, etc.) sont signalées dans le rapport d'évaluation mais ne pénalisent pas la note. Néanmoins, respecter ces conventions rend le code plus lisible et professionnel.

💡 **Note** : Si vous avez cloné le template récemment, la vérification automatique est déjà configurée dans les pre-commit hooks.

---

## Ressources complémentaires

- [Git - Aide-mémoire](git_aide_memoire.md) : Commandes Git essentielles (ligne de commande + VS Code)
