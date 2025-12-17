# Guide de démarrage

## ⚠️ PRÉREQUIS CRITIQUE AVANT LE TD0

**Cette procédure DOIT être suivie AVANT d'arriver au TD0.**

**📅 Groupes 2A, 2B, 2C (TD le 6 janvier)** :  
Setup **OBLIGATOIRE** avant la première séance. Sans cela, vous ne pourrez pas suivre le TD efficacement.

**📅 Groupe 2D (TD le 19 décembre)** :  
Le setup sera fait ensemble pendant la première séance. Mais si vous avez le temps de le faire avant, c'est **fortement recommandé** pour gagner du temps et pouvoir terminer TD0 + TD1a dans les 4h.

**Temps estimé** : 20-30 minutes

---

## 🚀 Etapes à suivre

### 1. Créer votre compte GitHub

Si ce n'est pas déjà fait, créez un compte sur [github.com](https://github.com/)

### 2. Créer un Personal Access Token (PAT)

GitHub n'accepte plus les mots de passe pour Git. Vous devez créer un **token** :

1. Connectez-vous à GitHub
2. Allez dans **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
   
   Ou directement : https://github.com/settings/tokens

3. Cliquez sur **Generate new token (classic)**
4. Configurez :
   - **Note** : `IUT R4.01` (ou ce que vous voulez)
   - **Expiration** : `90 days` (ou plus)
   - **Scopes** : cochez **`repo`** (accès complet aux repositories)
5. Cliquez sur **Generate token**
6. **⚠️ IMPORTANT : Copiez le token immédiatement !** Il ne sera plus visible après.

> 💡 **Conservez ce token** : envoyez-le vous par email pour pouvoir le copier-coller facilement en TD.

### 3. Créer votre repository

1. Rendez-vous sur **https://github.com/Marcennaji/ticketing_starter**
2. Cliquez sur **"Use this template"** → **"Create a new repository"**
3. Configurez :
   - **Owner** : votre compte GitHub personnel
   - **Repository name** : `ticketing`
   - **Visibility** : **Private** ⚠️ (obligatoire)
4. Cliquez sur **"Create repository"**

### 4. Ajouter l'enseignant comme collaborateur

1. Dans votre repository `ticketing` → **Settings** (en haut)
2. Dans le menu de gauche → **Collaborators and teams**
3. Cliquez sur **Add people**
4. Recherchez `Marcennaji`
5. Sélectionnez le rôle **Read** (accès en lecture)
6. Cliquez sur **Add Marcennaji to this repository**

> ⚠️ **Obligatoire** : Sans cela, votre travail ne pourra pas être évalué !

### 5. Cloner et initialiser sur votre machine de travail
Allez dans le répertoire où vous voulez cloner votre projet, puis:

```bash
git clone https://github.com/VOTRE-USERNAME/ticketing.git
```

Git vous demandera vos identifiants :
- **Username** : votre nom d'utilisateur GitHub
- **Password** : **collez votre token** (pas votre mot de passe !)

> 💡 Le token ne s'affiche pas quand vous le collez, c'est normal. Faites Ctrl+Shift+V puis Entrée.

Puis initialisez :
```bash
cd ticketing
source scripts/init.sh
```

Le script configure tout automatiquement.

**Vérification finale** : Si vous voyez ce message à la fin, c'est bon ✅ :
```
🎉 Environnement prêt !
✅ Tous les tests passent !
```

Si vous avez des erreurs, consultez la section "Problèmes fréquents" ci-dessous.

---

## 🔄 TD suivants

### PC fixes, ou PC portables attribués personnellement (compte personnel)

Le dossier persiste entre les séances. A chaque début de TD :

```bash
cd ticketing
git pull origin main          # ⚠️ IMPORTANT : récupérer vos dernières modifications
source scripts/init.sh
```

> ⚠️ **CRITIQUE si vous travaillez sur plusieurs machines** : Si vous alternez entre votre PC personnel et un PC de l'IUT (ou entre deux machines différentes), vous DEVEZ faire `git pull` avant de travailler, sinon vous risquez des conflits de code source et la perte de travail.

**Workflow multi-machines** :
1. **Début de séance** : `git pull origin main` (récupérer le travail fait ailleurs)
2. **Travail** : coder, tester, committer régulièrement
3. **Fin de séance** : `git push origin main` (sauvegarder sur GitHub)

### PC portables qui restent à l'IUT (compte partagé avec d'autres étudiants)

Rien ne persiste, il faut tout recloner à chaque début de TD:

```bash
git clone https://github.com/VOTRE-USERNAME/ticketing.git
cd ticketing
source scripts/init.sh
```

> 💡 Gardez votre token à portée de main, il sera demandé à chaque clone.

### Fin de séance sur portables restant à l'IUT (⚠️ OBLIGATOIRE)

Sur les **PC portables restant à l'IUT**, supprimez votre dossier en fin de séance :

```bash
# 1. Vérifier que tout est bien sauvegardé sur GitHub
git push origin main

# 2. Si vous avez terminé un TD, créer et pousser le tag
git tag TD1              # ou TD2, TD3, TD4 selon le TD
git push origin TD1

# 3. Supprimer le dossier local
cd ~
rm -rf ticketing
```

> 💡 Pour le tagging et la soumission des TDs, consultez le [Workflow de développement](workflow_de_developpement.md).

> ⚠️ Le compte de ces PC portables est partagé entre tous les étudiants. Ne laissez pas vos credentials ni votre code sur la machine !

---

## 🛠️ Commandes utiles

```bash
pytest                          # Lancer les tests
uvicorn src.main:app --reload   # Démarrer le serveur (http://localhost:8000)
```

---

## ❓ Problèmes fréquents

| Problème | Solution |
|----------|----------|
| `remote: Invalid username or token` | Vérifiez votre token (régénérez-le si besoin) |
| `uvicorn: command not found` | Relancez `source scripts/init.sh` |
| Tests échouent (erreurs d'import) | Vérifiez que vous êtes à la racine du projet |
| Port 8000 occupé | `uvicorn src.main:app --reload --port 8001` |

### Token perdu ou expiré ?

1. Allez sur https://github.com/settings/tokens
2. Supprimez l'ancien token (si visible)
3. Créez-en un nouveau (voir étape 2)
