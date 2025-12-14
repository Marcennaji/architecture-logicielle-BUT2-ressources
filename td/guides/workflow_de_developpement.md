# Workflow de développement et rendu

Ce document explique comment organiser votre travail et soumettre vos TDs pour correction.

## Principe : Une branche par TD

Chaque TD doit être développé sur une **branche dédiée**, puis soumis via une **Pull Request** (PR). Ce workflow est utilisé en entreprise pour la revue de code.

```
main (stable)
  │
  ├── td1 → PR → auto-validation → merge → tag TD1
  │
  ├── td2 → PR → auto-validation → merge → tag TD2
  │
  ├── td3 → PR → auto-validation → merge → tag TD3
  │
  └── td4 → PR → auto-validation → merge → tag TD4
```

> 💡 **Note** : Les TD ne sont pas corrigés individuellement. Vous vous auto-validez via les checklists des PR. L'enseignant évaluera le **projet final complet** (tag TD4) pour l'appréciation globale.

> ⚠️ **Support disponible** : Si vous rencontrez des difficultés sur un TD, **contactez l'enseignant** pendant les séances ou par email. Ne restez pas bloqué !

## Étape par étape

### 1. Créer une branche pour le TD

```bash
# S'assurer d'être sur main à jour
git checkout main
git pull origin main

# Créer et basculer sur la branche du TD (ici, cette branche s'appelle 'td1')
git checkout -b td1
```

### 2. Développer le TD

Travaillez normalement sur votre code. Faites des commits réguliers :

```bash
git add .
git commit -m "feat: implémentation du use case CreateTicket"
```

> 💡 **Conseil** : Faites plusieurs petits commits plutôt qu'un seul gros commit. Cela montre votre progression et facilite la revue.

### 3. Pousser la branche nommée 'td1'

```bash
git push origin td1
```

### 4. Créer une Pull Request

1. Allez sur votre repo GitHub
2. Vous verrez un bandeau proposant de créer une PR pour `td1`
3. Cliquez sur **Compare & pull request**
4. Remplissez le template de PR qui s'affiche automatiquement :
   - **Titre** : `TD1 - [Votre description]`
   - **Description** : Le template contient des checklists à cocher (architecture, tests, qualité)
   - **Checklist spécifique au TD** : Ajoutez les points demandés dans l'énoncé du TD
   - **Questions/remarques** : Notez vos difficultés ou interrogations (optionnel)
5. Cliquez sur **Create pull request**

> 💡 **Conseil** : Prenez le temps de cocher les checklists **avant** de créer la PR. Cela vous permet de vérifier que vous n'avez rien oublié !

> ℹ️ **Tous les TD** : Vous pouvez merger vous-même après auto-validation via les checklists.

### 5. Auto-validation

1. Relisez votre code et vérifiez les checklists de la PR
2. Assurez-vous que tous les tests passent (`pytest`)
3. Si tout est OK, passez à l'étape 7 (merger)

> 💡 Les checklists du template de PR sont votre guide d'auto-évaluation.

> 📊 **Évaluation finale** : L'enseignant évaluera votre **projet complet** (tag TD4) en fin de module pour donner une appréciation globale sur l'architecture, les fonctionnalités, les tests et la qualité du code.

### 6. Corriger si nécessaire

Si vous détectez des problèmes lors de l'auto-validation, corrigez-les avant de merger :

```bash
# Vous êtes toujours sur la branche (td1, td2, td3 ou td4)
git add .
git commit -m "fix: correction après relecture"
git push origin td1  # ou td2, td3, td4
```

La PR se met à jour automatiquement avec vos nouveaux commits.

### 7. Merger et créer un tag

Une fois les checklists vérifiées et les tests OK :

1. **Vous mergez la PR** sur GitHub (bouton "Merge pull request")
2. Confirmez le merge (bouton "Confirm merge")
3. **Vérifiez que le merge a réussi** : message "Pull request successfully merged and closed" ✅
4. Supprimez la branche distante (bouton "Delete branch")
5. **Créez un tag** pour marquer la version finale :

```bash
git checkout main
git pull origin main
git tag TD1  # ou TD2, TD3, TD4
git push origin TD1
```

> 💡 **Sécurité** : La suppression de branche sur GitHub ne supprime que la branche **distante**. Votre branche locale reste intacte. Si vous avez un doute, vérifiez d'abord que le merge apparaît bien dans l'historique de `main` avant de supprimer quoi que ce soit.

## Résumé des commandes

| Action | Commande |
|--------|----------|
| Nouvelle branche | `git checkout -b td2` |
| Commit | `git commit -m "message"` |
| Push branche | `git push origin td2` |
| Retour sur main | `git checkout main` |
| Mise à jour main | `git pull origin main` |
| Créer un tag | `git tag TD2 && git push origin TD2` |

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

### Description de PR

Une bonne description de PR contient :
- Ce que vous avez implémenté
- Les choix techniques que vous avez faits
- Les difficultés rencontrées (optionnel)
- Les questions que vous avez (optionnel)

## FAQ

### Puis-je continuer à travailler sur le TD suivant avant de merger le TD actuel ?

Oui ! Créez une nouvelle branche pour le TD suivant :

```bash
git checkout main
git checkout -b td2
```

### J'ai fait une erreur sur ma branche, comment corriger ?

```bash
# Modifier le dernier commit
git add .
git commit --amend -m "nouveau message"
git push origin td1 --force
```

### J'ai supprimé ma branche par erreur avant de merger !

**Pas de panique** : votre branche locale existe toujours sur votre machine.

```bash
# Vérifier que la branche existe localement
git branch

# Si elle existe, la repousser sur GitHub
git push origin td1
```

Si vous avez supprimé aussi la branche locale, vous pouvez la recréer depuis votre dernier commit (tant que vous n'avez pas fait `git gc`) :

```bash
# Voir l'historique de vos actions Git
git reflog

# Recréer la branche depuis un commit spécifique
git checkout -b td1 <hash-du-commit>
```

**En cas de doute**, contactez l'enseignant AVANT de faire des manipulations hasardeuses.

### J'ai des difficultés sur un TD, que faire ?

**Ne restez pas bloqué !** Contactez l'enseignant :
- Pendant les séances TD (levez la main)
- Par email avec une description claire du problème
- En incluant le lien vers votre PR si pertinent

L'enseignant est là pour vous aider à progresser tout au long du module.

---

## Ressources complémentaires

- [Git - Aide-mémoire](git_aide_memoire.md) : Commandes Git essentielles (ligne de commande + VS Code)
