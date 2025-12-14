# Guide de démarrage

## ⚠️ PRÉREQUIS OBLIGATOIRE AVANT LE TD0

**Cette procédure DOIT être suivie AVANT d'arriver au TD0.**

En suivant cette procédure maintenant, vous gagnerez du temps lors du TD0 et pourrez vous concentrer directement sur le code et le workflow Git/GitHub.

**Temps estimé** : 15-20 minutes

**Vérification de réussite** : Au début du TD0, vous devez être capable de :
- ✅ Lancer la commande `pytest` dans votre projet et voir tous les tests passer
- ✅ Voir votre repository `ticketing` sur votre compte GitHub
- ✅ Voir "Marcennaji" dans la liste de vos collaborateurs GitHub (avec le rôle **Triage**)

---

## 🚀 Premier TD

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
   - **Visibilité** : **Private** ⚠️ (obligatoire)
4. Cliquez sur **"Create repository"**

### 4. Ajouter l'enseignant comme collaborateur

1. Dans votre repository `ticketing` → **Settings** (en haut)
2. Dans le menu de gauche → **Collaborators and teams**
3. Cliquez sur **Add people**
4. Recherchez `Marcennaji`
5. Sélectionnez le rôle **Triage** (permet la review de code et les commentaires de validation)
6. Cliquez sur **Add Marcennaji to this repository**

> ⚠️ **Obligatoire** : Sans cela, je ne pourrai pas reviewer votre code ni valider vos Pull Requests !

### 5. Cloner et initialiser

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

Le dossier persiste entre les séances. A chaque début de TD, faire :

```bash
cd ticketing
source scripts/init.sh
```

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
cd ~
rm -rf ticketing
```

> ⚠️ Le compte est partagé entre tous les étudiants. Ne laissez pas vos credentials ni votre code sur la machine !

---

## 📖 Documentation

- [Workflow de développement](workflow_de_developpement.md) - Comment soumettre votre travail
- [Stratégie de tests](comment_tester.md) - Guide des tests par couche

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
