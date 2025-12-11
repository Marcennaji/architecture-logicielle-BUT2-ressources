# Git - Aide-mémoire

> **Référence rapide** des commandes Git essentielles pour le projet R4.01.
> 
> Pour chaque opération, vous trouverez :
> - 🖥️ La commande en ligne de commande
> - 🎨 L'équivalent dans VS Code (interface graphique)

---

## 📋 Consulter l'état du dépôt

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
git log --oneline --graph      # Avec visualisation des branches
git log -n 5                   # 5 derniers commits
```

**🎨 VS Code**
- Extension **Git Graph** (installée par défaut) : Cliquez sur l'icône "Git Graph" dans la barre latérale
- Ou palette de commandes (Ctrl+Shift+P) → "Git Graph: View Git Graph"
- Pour l'historique d'un fichier : Clic droit sur le fichier → "Git: View File History"

---

## 🌿 Gérer les branches

### Créer une nouvelle branche

**🖥️ Ligne de commande**
```bash
git checkout -b td1-domain     # Crée et bascule sur la nouvelle branche
```

**🎨 VS Code**
- Cliquez sur le nom de la branche actuelle (en bas à gauche)
- Sélectionnez "+ Create new branch..."
- Donnez un nom (ex: `td1-domain`)

### Changer de branche

**🖥️ Ligne de commande**
```bash
git checkout main              # Bascule sur main
git checkout td1-domain        # Bascule sur td1-domain
```

**🎨 VS Code**
- Cliquez sur le nom de la branche actuelle (en bas à gauche)
- Sélectionnez la branche cible dans la liste

### Lister les branches

**🖥️ Ligne de commande**
```bash
git branch                     # Branches locales
git branch -a                  # Toutes les branches (locales + distantes)
```

**🎨 VS Code**
- Cliquez sur le nom de la branche actuelle (en bas à gauche)
- La liste complète s'affiche

### Supprimer une branche

**🖥️ Ligne de commande**
```bash
git branch -d td1-domain       # Supprime localement (seulement si mergée)
git branch -D td1-domain       # Force la suppression
```

**🎨 VS Code**
- Palette de commandes (Ctrl+Shift+P) → "Git: Delete Branch..."
- Sélectionnez la branche à supprimer

---

## 💾 Sauvegarder ses modifications

### Ajouter des fichiers à l'index (staging)

**🖥️ Ligne de commande**
```bash
git add src/domain/ticket.py          # Ajoute un fichier spécifique
git add src/domain/                   # Ajoute tout un dossier
git add .                             # Ajoute tous les fichiers modifiés
```

**🎨 VS Code**
- Dans "Source Control", cliquez sur le **+** à côté du fichier
- Ou cliquez sur **+** dans "Changes" pour tout ajouter

### Valider les modifications (commit)

**🖥️ Ligne de commande**
```bash
git commit -m "feat(domain): ajout de la méthode reopen()"
```

**🎨 VS Code**
- Dans "Source Control", écrivez le message dans la zone de texte en haut
- Cliquez sur le bouton **✓ Commit** (ou Ctrl+Enter)

### Envoyer les commits sur GitHub (push)

**🖥️ Ligne de commande**
```bash
git push origin td1-domain     # Push de la branche td1-domain
git push                       # Push de la branche actuelle
```

**🎨 VS Code**
- Dans "Source Control", cliquez sur **⋯** (menu) → "Push"
- Ou cliquez sur l'icône **↑** dans la barre d'état (en bas)

### Récupérer les dernières modifications (pull)

**🖥️ Ligne de commande**
```bash
git pull origin main           # Récupère les changements de main
git pull                       # Pull de la branche actuelle
```

**🎨 VS Code**
- Dans "Source Control", cliquez sur **⋯** (menu) → "Pull"
- Ou cliquez sur l'icône **↓** dans la barre d'état (en bas)

---

## 🔧 Dépannage courant

### Annuler le dernier commit (garder les modifications)

**🖥️ Ligne de commande**
```bash
git reset --soft HEAD~1        # Le commit est annulé, les fichiers restent "staged"
```

**🎨 VS Code**
- Palette de commandes → "Git: Undo Last Commit"
- Les modifications restent dans "Staged Changes"

### Annuler les modifications d'un fichier non commité

**🖥️ Ligne de commande**
```bash
git checkout -- src/domain/ticket.py    # Restaure le fichier à l'état du dernier commit
```

**🎨 VS Code**
- Dans "Source Control", clic droit sur le fichier → "Discard Changes"

⚠️ **ATTENTION** : Les modifications sont perdues définitivement !

### Mettre de côté des modifications temporairement (stash)

**🖥️ Ligne de commande**
```bash
git stash                      # Sauvegarde les modifications
git stash pop                  # Restaure les modifications sauvegardées
git stash list                 # Liste les stashes
```

**🎨 VS Code**
- Dans "Source Control", cliquez sur **⋯** (menu) → "Stash" → "Stash"
- Pour restaurer : **⋯** → "Stash" → "Pop Latest Stash"

**Cas d'usage** : Vous êtes sur la mauvaise branche, vous avez déjà codé → stash, checkout branche correcte, stash pop.

### Voir les différences d'un fichier

**🖥️ Ligne de commande**
```bash
git diff src/domain/ticket.py          # Différences non stagées
git diff --staged src/domain/ticket.py # Différences stagées
```

**🎨 VS Code**
- Dans "Source Control", cliquez sur le fichier modifié
- Une vue "diff" s'ouvre automatiquement (rouge = supprimé, vert = ajouté)

---

## 🚨 Commandes dangereuses (à utiliser avec précaution)

### Écraser l'historique distant (force push)

**🖥️ Ligne de commande**
```bash
git push --force origin td1-domain
```

**🎨 VS Code**
- Palette de commandes → "Git: Push (Force)"

⚠️ **NE JAMAIS FAIRE** sur `main` ou une branche partagée !  
✅ OK sur votre branche personnelle si vous avez fait un `git commit --amend` ou un `git rebase`.

### Réinitialiser complètement une branche

**🖥️ Ligne de commande**
```bash
git reset --hard origin/main   # Remet la branche exactement comme origin/main
```

**🎨 VS Code**
- Palette de commandes → "Git: Reset" → Sélectionnez "Hard"

⚠️ **TOUTES les modifications locales non commitées sont PERDUES** !

### Modifier le dernier commit

**🖥️ Ligne de commande**
```bash
# Vous avez oublié un fichier ou fait une faute de frappe dans le message
git add fichier_oublie.py
git commit --amend              # Ouvre l'éditeur pour modifier le message
git commit --amend --no-edit    # Garde le même message
```

**🎨 VS Code**
- Ajoutez les fichiers oubliés au staging (bouton **+**)
- Palette de commandes → "Git: Commit Staged (Amend)"

⚠️ Si vous avez déjà pushé le commit, vous devrez faire un `git push --force` (évitez sur des branches partagées).

---

## 💡 Astuces pour le projet

### Workflow complet pour un exercice de TD

```bash
# 1. Créer la branche d'exercice
git checkout -b td3-exercice

# 2. Coder, tester...

# 3. Vérifier ce qui a changé
git status
git diff

# 4. Ajouter et commiter
git add .
git commit -m "feat(td3): ajout CommentRepository SQLite"

# 5. Pousser AVANT la deadline
git push origin td3-exercice

# ⏰ Vérifier l'heure du commit
git log -1 --format="%ai"    # Affiche la date/heure du dernier commit
```

### Éviter les commits "tout vrac"

❌ **Mauvais**
```bash
git add .
git commit -m "changements"
```

✅ **Bon**
```bash
# Commiter par unité logique
git add src/domain/ticket.py tests/domain/test_ticket.py
git commit -m "feat(domain): ajout méthode Ticket.reopen()"

git add src/application/usecases/reopen_ticket.py
git commit -m "feat(application): use case ReopenTicket"
```

**🎨 Dans VS Code** : Utilisez le staging sélectif (cliquez **+** fichier par fichier).

### Rattraper une branche en retard sur main

```bash
# Vous êtes sur td2-usecases, mais main a avancé
git checkout main
git pull origin main

git checkout td2-usecases
git merge main               # Intègre les nouveautés de main dans td2-usecases
# Ou: git rebase main        # Alternative plus "propre" mais plus complexe
```

**🎨 VS Code**
- Basculez sur `main`, faites un pull
- Revenez sur `td2-usecases`
- Palette de commandes → "Git: Merge Branch..." → Sélectionnez `main`

---

## 🆘 Problèmes fréquents

### "Your branch is behind 'origin/main'"

**Cause** : Quelqu'un (ou vous depuis une autre machine) a pushé sur `main`.

**Solution**
```bash
git pull origin main
```

**🎨 VS Code** : Cliquez sur **↓** dans la barre d'état.

### "Merge conflict"

**Cause** : Git ne peut pas fusionner automatiquement car vous et quelqu'un d'autre avez modifié les mêmes lignes.

**Solution**
1. **🖥️ Ligne de commande**
   ```bash
   # Ouvrez le fichier en conflit (marqueurs <<<<<<, ======, >>>>>>)
   # Éditez manuellement pour garder la bonne version
   git add fichier_resolu.py
   git commit -m "fix: résolution conflit merge"
   ```

2. **🎨 VS Code**
   - Les conflits sont marqués visuellement dans l'éditeur
   - Cliquez sur "Accept Current Change", "Accept Incoming Change", ou "Accept Both"
   - Une fois résolu, cliquez sur **+** pour stager le fichier
   - Commitez

### "fatal: not a git repository"

**Cause** : Vous n'êtes pas dans le bon dossier.

**Solution**
```bash
cd ~/mon-projet-ticketing    # Naviguez vers le dossier du projet
```

**🎨 VS Code** : Ouvrez le bon dossier (Fichier → Ouvrir le dossier...).

### Commit poussé par erreur sur la mauvaise branche

**Exemple** : Vous avez commité sur `main` au lieu de `td1-domain`.

**Solution**
```bash
# Sur main (où est le commit à déplacer)
git log --oneline -3         # Notez l'ID du commit (ex: a1b2c3d)

# Créez la bonne branche depuis ce commit
git checkout -b td1-domain

# Revenez sur main et annulez le commit
git checkout main
git reset --hard HEAD~1      # Supprime le dernier commit de main

# Pushez la correction
git push origin td1-domain
git push --force origin main # ⚠️ Seulement si vous êtes seul sur main
```

---

## 📚 Ressources complémentaires

- [Documentation officielle Git](https://git-scm.com/doc)
- [Visualisation interactive Git](https://learngitbranching.js.org/) (excellent pour comprendre les branches)
- [Git Cheat Sheet (PDF)](https://education.github.com/git-cheat-sheet-education.pdf)
- Extension VS Code installée : **Git Graph** (`mhutchie.git-graph`) pour visualiser l'historique graphique
