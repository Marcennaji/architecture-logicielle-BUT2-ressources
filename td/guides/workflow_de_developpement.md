# Workflow de développement et rendu

Ce document explique comment organiser votre travail et soumettre vos TDs pour évaluation.

## Principe : Commits réguliers sur `main` + tags

Chaque TD est développé directement sur la branche `main` avec des **commits réguliers**, puis marqué avec un **tag standardisé** quand vous êtes prêt à soumettre.

```
main
  │
  ├─ commits TD1 ─→ tag TD1
  │
  ├─ commits TD2 ─→ tag TD2
  │
  ├─ commits TD3 ─→ tag TD3
  │
  └─ commits TD4 ─→ tag TD4
```

**Tags obligatoires** :
- `TD1` (domain modeling)
- `TD2` (use cases + ports)
- `TD3` (repository SQLite)
- `TD4` (API REST)

> 💡 **Pourquoi cette approche ?** Elle simplifie le workflow tout en gardant un historique complet de votre progression via les commits. Les tags permettent à l'enseignant d'évaluer automatiquement votre travail à des étapes précises.

> ⚠️ **Support disponible** : Si vous rencontrez des difficultés sur un TD, **contactez l'enseignant** pendant les séances ou par email. Ne restez pas bloqué !

> ⚠️ **Arborescence obligatoire** : Ne modifiez **JAMAIS** la structure des dossiers principaux (`src/domain/`, `src/application/`, `src/ports/`, `src/adapters/`, `tests/`). Vous pouvez créer des sous-dossiers à l'intérieur, mais l'arborescence de base doit rester identique pour tous.

## Étape par étape

### 1. Développer le TD

Travaillez sur votre code directement sur `main`. Faites des **commits réguliers** :

```bash
git add .
git commit -m "feat: ajout entité Ticket avec validation statut"
```

> 💡 **Important** : Faites **plusieurs petits commits** au fur et à mesure de votre progression (idéalement 10-15 commits par TD). Cela démontre un travail itératif et facilite le debugging.

**Exemples de bonne granularité** :
```bash
git commit -m "feat: création classe Ticket"
git commit -m "feat: ajout validation du titre"
git commit -m "test: ajout tests unitaires Ticket"
git commit -m "feat: ajout méthode assign()"
git commit -m "test: tests pour assign()"
```

### 2. Pousser régulièrement sur GitHub

```bash
git push origin main
```

> 💡 **Conseil** : Poussez vos commits sur GitHub au moins à la fin de chaque séance TD. Cela sauvegarde votre travail et permet à l'enseignant de voir votre progression si vous demandez de l'aide.

### 3. Soumettre le TD avec un tag

Quand vous avez terminé le TD et que tous les tests passent :

```bash
# Vérifier que tous les tests passent
pytest

# Créer le tag (nom EXACT requis)
git tag TD1  # ou TD2, TD3, TD4

# Pousser le tag sur GitHub
git push origin TD1
```

> ⚠️ **Attention** : Le nom du tag doit être **exactement** `TD1`, `TD2`, `TD3` ou `TD4` (en majuscules).

> 📊 **Évaluation** : Votre travail sera évalué à partir du tag. L'historique complet des commits entre les tags sera également pris en compte.

## Résumé des commandes

| Action | Commande |
|--------|----------|
| Ajouter fichiers | `git add .` |
| Commit | `git commit -m "message"` |
| Push vers GitHub | `git push origin main` |
| Vérifier tests | `pytest` |
| Créer un tag | `git tag TD1` (ou TD2, TD3, TD4) |
| Pousser le tag | `git push origin TD1` |

## Bonnes pratiques

### Messages de commit

Utilisez des préfixes pour catégoriser vos commits :

- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `refactor:` refactoring sans changement de comportement
- `test:` ajout ou modification de tests
- `docs:` documentation

**Exemples :**
```
feat: ajout du use case AssignTicket
fix: correction de la validation du statut
test: ajout des tests pour CloseTicket
refactor: extraction de la logique métier dans le domain
```

### Fréquence des commits

- Commitez **souvent** (plusieurs fois par heure de travail)
- Un commit = une unité logique de travail
- Évitez les commits géants avec 10 fichiers modifiés
- **Objectif** : 10-15 commits minimum par TD

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

### J'ai des difficultés sur un TD, que faire ?

**Ne restez pas bloqué !** Contactez l'enseignant :
- Pendant les séances TD (levez la main)
- Par email avec une description claire du problème
- En incluant le lien vers votre repository GitHub

L'enseignant est là pour vous aider à progresser tout au long du module.

---

## Ressources complémentaires

- [Git - Aide-mémoire](git_aide_memoire.md) : Commandes Git essentielles (ligne de commande + VS Code)
