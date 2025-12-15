# Git - Aide-mémoire

> **Référence rapide** des commandes Git essentielles pour le module R4.01.
> 
> Pour chaque opération, vous trouverez :
> - 🖥️ La commande en ligne de commande
> - 🎨 L'équivalent dans VS Code (interface graphique)

---

## 📋 Consulter l'état du projet

### Voir les fichiers modifiés

**🖥️ Ligne de commande**
```bash
git status
```

**🎨 VS Code**
- Cliquez sur l'icône "Source Control" dans la barre latérale (icône de branche)
- Les fichiers modifiés apparaissent dans la section "Changes"

### Voir l'historique des commits

**🖥️ Ligne de commande**
```bash
git log --oneline              # Format compact
git log --oneline -10          # 10 derniers commits
```

**🎨 VS Code**
- Extension **Git Graph** : Cliquez sur l'icône dans la barre latérale
- Pour l'historique d'un fichier : Clic droit sur le fichier → "Git: View File History"

---

## 💾 Workflow quotidien (ce que vous ferez tout le temps)

### 1. Ajouter des fichiers à l'index (staging)

**🖥️ Ligne de commande**
```bash
git add src/domain/ticket.py          # Ajoute un fichier spécifique
git add .                             # Ajoute tous les fichiers modifiés
```

**🎨 VS Code**
- Dans "Source Control", cliquez sur le **+** à côté du fichier
- Ou cliquez sur **+** dans "Changes" pour tout ajouter

### 2. Créer un commit

**🖥️ Ligne de commande**
```bash
git commit -m "TD1: ajout entité Ticket avec validation"
```

**🎨 VS Code**
- Dans "Source Control", écrivez le message dans la zone de texte en haut
- Cliquez sur le bouton **✓ Commit** (ou Ctrl+Enter)

**💡 Bonnes pratiques pour les messages** :
- Commencez par le numéro du TD : `TD1:`, `TD2:`, etc.
- Soyez descriptif : `TD1: ajout méthode assign()` au lieu de `fix`
- Faites des commits réguliers (10-15 par TD)

### 3. Pousser vers GitHub

**🖥️ Ligne de commande**
```bash
git push origin main           # Push vers GitHub
```

**🎨 VS Code**
- Cliquez sur **⋯** (menu) → "Push"
- Ou cliquez sur l'icône **↑** dans la barre d'état (en bas)

### 4. Créer un tag pour soumettre un TD

**🖥️ Ligne de commande**
```bash
git tag TD1                    # Créer le tag
git push origin TD1            # Pousser le tag
```

**🎨 VS Code**
- Palette de commandes (Ctrl+Shift+P) → "Git: Create Tag..."
- Nommez le tag exactement `TD1`, `TD2`, `TD3` ou `TD4`
- Puis : **⋯** → "Push" → Cochez "Include Tags"

**⚠️ Important** : Le nom du tag doit être EXACT (`TD1` en majuscules, pas `td1`)

---

## 🔍 Voir les différences

### Comparer un fichier avec la dernière version

**🖥️ Ligne de commande**
```bash
git diff src/domain/ticket.py          # Différences non commitées
```

**🎨 VS Code**
- Dans "Source Control", cliquez sur le fichier modifié
- Une vue "diff" s'ouvre (rouge = supprimé, vert = ajouté)

---

## 🔧 Corriger des erreurs courantes

### Modifier le dernier commit (avant push)

**🖥️ Ligne de commande**
```bash
# Vous avez oublié un fichier ou fait une faute dans le message
git add fichier_oublie.py
git commit --amend -m "TD1: nouveau message corrigé"
```

**🎨 VS Code**
- Ajoutez les fichiers oubliés au staging (bouton **+**)
- Palette de commandes → "Git: Commit Staged (Amend)"

### Annuler les modifications d'un fichier non commité

**🖥️ Ligne de commande**
```bash
git checkout -- src/domain/ticket.py    # Restaure le fichier
```

**🎨 VS Code**
- Dans "Source Control", clic droit sur le fichier → "Discard Changes"

⚠️ **ATTENTION** : Les modifications sont perdues définitivement !

### Supprimer/recréer un tag

**🖥️ Ligne de commande**
```bash
# Vous avez tagué trop tôt et voulez corriger
git tag -d TD1                          # Supprime localement
git push origin :refs/tags/TD1          # Supprime sur GitHub

# Faites vos corrections...
git add .
git commit -m "TD1: corrections finales"
git push origin main

# Recréez le tag
git tag TD1
git push origin TD1
```

⚠️ **Ne faites cela que si la deadline n'est pas passée !**

---

## 🔄 Mettre à jour depuis GitHub

### Récupérer les dernières modifications

**🖥️ Ligne de commande**
```bash
git pull origin main           # Récupère les changements
```

**🎨 VS Code**
- Cliquez sur **⋯** → "Pull"
- Ou cliquez sur l'icône **↓** dans la barre d'état

**Cas d'usage** : Vous travaillez sur plusieurs machines (IUT + maison)

---

## 🆘 Problèmes fréquents

### "Your branch is behind 'origin/main'"

**Cause** : Vous avez travaillé sur une autre machine et poussé des commits.

**Solution**
```bash
git pull origin main
```

### "fatal: not a git repository"

**Cause** : Vous n'êtes pas dans le bon dossier.

**Solution**
```bash
cd ~/ticketing    # Naviguez vers le dossier du projet
```

### Message d'erreur lors du push (authentication failed)

**Cause** : Votre Personal Access Token est expiré ou incorrect.

**Solution**
- Créez un nouveau token : https://github.com/settings/tokens
- Utilisez ce token comme mot de passe lors du push

---

## 💡 Astuces pour le projet

### Workflow complet pour un TD

```bash
# 1. Coder et tester régulièrement

# 2. Commiter souvent (petits commits)
git add src/domain/ticket.py tests/domain/test_ticket.py
git commit -m "TD1: ajout méthode Ticket.assign()"

# 3. Pousser régulièrement (au moins en fin de séance)
git push origin main

# 4. Quand le TD est terminé, créer le tag
git tag TD1
git push origin TD1
```

### Vérifier l'heure de votre dernier commit

**🖥️ Ligne de commande**
```bash
git log -1 --format="%ai"    # Affiche date/heure du dernier commit
```

**Utile pour** : Vérifier que vous avez bien commité pendant la séance TD (bonus présentiel)

### Lister vos tags existants

**🖥️ Ligne de commande**
```bash
git tag                      # Liste locale
git ls-remote --tags origin  # Liste sur GitHub
```

---

## 📚 Ressources complémentaires

- [Documentation officielle Git (FR)](https://git-scm.com/book/fr/v2)
- [Visualisation interactive Git](https://learngitbranching.js.org/) (pour comprendre les concepts)
- Extension VS Code recommandée : **Git Graph** (visualisation graphique de l'historique)
