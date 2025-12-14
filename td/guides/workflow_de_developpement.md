# Workflow de développement et rendu

Ce document explique comment organiser votre travail et soumettre vos TDs pour correction.

## Principe : Une branche par TD

Chaque TD doit être développé sur une **branche dédiée**, puis soumis via une **Pull Request** (PR). Ce workflow est utilisé en entreprise pour la revue de code.

```
main (stable)
  │
  ├── td1 → PR → review → merge → tag TD1
  │
  ├── td2 → PR → review → merge → tag TD2
  │
  └── ...
```

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
   - **Questions/remarques** : N'hésitez pas à poser des questions à l'enseignant
5. Cliquez sur **Create pull request**

> 💡 **Conseil** : Prenez le temps de cocher les checklists **avant** de créer la PR. Cela vous permet de vérifier que vous n'avez rien oublié !

> ⚠️ **Important** : Ne mergez PAS la PR vous-même ! Attendez la review.

### 5. Recevoir la review

Votre enseignant va :
- Lire votre code
- Ajouter des **commentaires ligne par ligne** (si nécessaire)
- Demander des modifications si nécessaire
- **Valider la PR** en laissant un commentaire explicite : "✅ Validé, vous pouvez merger"

Vous recevrez une notification GitHub pour chaque commentaire.

### 6. Corriger si demandé

Si des modifications sont demandées :

```bash
# Vous êtes toujours sur la branche td1
git add .
git commit -m "fix: correction suite à la review"
git push origin td1
```

La PR se met à jour automatiquement avec vos nouveaux commits.

### 7. Merger et créer un tag (après validation)

Une fois la PR **validée** par l'enseignant (commentaire "✅ Validé, vous pouvez merger") :

1. **Vous mergez la PR** sur GitHub (bouton "Merge pull request")
2. Confirmez le merge (bouton "Confirm merge")
3. **Vérifiez que le merge a réussi** : vous devez voir un message "Pull request successfully merged and closed" avec une coche violette ✅
4. Seulement après cette confirmation, supprimez la branche distante (bouton "Delete branch")
5. **Créez un tag** pour marquer la version finale :

```bash
git checkout main
git pull origin main
git tag TD1
git push origin TD1
```

> ⚠️ **Important** : Ne mergez pas avant la validation explicite de l'enseignant !

> 💡 **Sécurité** : La suppression de branche sur GitHub ne supprime que la branche **distante**. Votre branche locale reste intacte. Si vous avez un doute, vérifiez d'abord que le merge apparaît bien dans l'historique de `main` avant de supprimer quoi que ce soit.

> 💡 **Bon à savoir** : Tous les commentaires de review restent accessibles après le merge dans l'historique de la PR (onglet "Pull requests" → filtre "Closed").

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

### Puis-je continuer à travailler pendant la review ?

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

### Comment voir les commentaires de review ?

Sur GitHub, dans l'onglet **Pull requests** de votre repo, puis dans la section **Files changed** de votre PR.

---

## Ressources complémentaires

- [Git - Aide-mémoire](git_aide_memoire.md) : Commandes Git essentielles (ligne de commande + VS Code)
