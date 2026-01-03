# Guide de démarrage

**Temps estimé** : 20-30 minutes

---

## 🚀 Etapes à suivre (à faire chez vous, avant le tout premier TD)

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

### 5. Cloner le repository sur votre machine

Ouvrez un terminal et allez dans le répertoire où vous voulez cloner votre projet :

```bash
git clone https://github.com/VOTRE-USERNAME/ticketing.git
```

Git vous demandera vos identifiants :
- **Username** : votre nom d'utilisateur GitHub
- **Password** : **collez votre token** (pas votre mot de passe !)

> 💡 Le token ne s'affiche pas quand vous le collez, c'est normal. Faites Ctrl+Shift+V puis Entrée.

### 6. Identifier votre repository

**⚠️ Si votre nom d'utilisateur GitHub ne correspond pas à votre nom réel** (ex: `dark_coder_666`), l'enseignant ne pourra pas savoir à qui appartient le repository.

**Solution** : Ajoutez vos nom et prénom en haut du fichier `README.md` :

```bash
cd ticketing
# Éditez README.md avec VS Code, nano, ou votre éditeur préféré
```

Ajoutez en haut du fichier :
```markdown
# Projet Ticketing - Architecture Logicielle

**Étudiant** : Prénom NOM

---

[reste du README...]
```

Puis commitez et poussez :
```bash
git add README.md
git commit -m "Ajout identification étudiant"
git push origin main
```

### 7. Initialiser l'environnement

> 💡 **Environnement de travail** : Ces TDs sont conçus pour Linux (machines de l'IUT). 

**Sur les machines IUT (Ubuntu)**, installez d'abord le package python3-venv :

```bash
sudo apt update
sudo apt install -y python3-venv
```

> 💡 Cette installation est nécessaire une seule fois par machine. Si la commande échoue (ex: pas de droits sudo), demandez de l'aide.

**⚠️ Si l'installation échoue (erreur de droits d'écriture)** :

1. **Option 1** : Demandez à l'enseignant ou au responsable de salle d'installer le package
2. **Option 2** : Changez de machine (le package est peut-être déjà installé sur d'autres postes)
3. **Option 3** : Vérifiez d'abord si c'est nécessaire en testant directement :
   ```bash
   cd ticketing
   python3 -m venv .venv
   ls .venv/bin/activate   # Si ce fichier existe, python3-venv est déjà installé
   ```

Puis initialisez l'environnement du projet :

```bash
cd ticketing  # si pas déjà dans le dossier
source scripts/init.sh
```

Le script configure automatiquement l'environnement Python et installe les dépendances.

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
