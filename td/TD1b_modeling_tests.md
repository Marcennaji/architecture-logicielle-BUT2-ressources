# TD1b — Tests unitaires du domaine

## 📦 Jalon TD1b (2h) → Tag `TD1b`

**Durée : 1 séance de 2h** (séance suivant TD1a)

### Objectif

Écrire des tests unitaires qui couvrent **toutes les règles métier** du domaine, y compris les cas d'erreur. L'objectif est de garantir qu'on ne peut pas contourner les règles métier.

### Ce qui est attendu

- ✅ Chaque règle métier a un test qui vérifie le cas nominal
- ✅ Chaque règle métier a un test qui vérifie le cas d'erreur
- ✅ Tous les tests passent : `pytest tests/domain/` vert
- ✅ On ne peut pas contourner les règles métier

Voir [evaluation.md](evaluation.md) pour le système de notation.

> ⚠️ **Important** : Les exemples de règles métier donnés dans ce TD sont indicatifs. Vous devez les adapter en fonction des entités et des règles métier que **vous** avez réellement implémentées dans TD1a. Chaque étudiant peut avoir des règles légèrement différentes.

---

## Étape 1 : Lister les règles métier

Avant de tester, listez, si vous ne l'avez pas déjà fait dans le fichier domain-notes.md, **toutes les règles métier** de votre domaine :

**Exemples de règles métier** :
- Un ticket doit avoir un titre non vide
- Un utilisateur doit avoir un username non vide
- Un ticket fermé ne peut plus être assigné
- Un ticket déjà fermé ne peut pas être re-fermé


---

## Étape 2 : Tester les cas nominaux

Pour chaque règle métier, écrivez un test unitaire qui vérifie le **comportement normal**.

**Exemples de cas nominaux à tester** :
- Un ticket peut être créé avec des valeurs valides
- Un ticket ouvert peut être assigné à un agent
- Un ticket assigné peut être fermé
- Un utilisateur peut être créé avec un username valide
- Un ticket a le statut OPEN à sa création
- L'assignation d'un ticket change son statut à IN_PROGRESS

---

## Étape 3 : Tester les cas d'erreur

Pour chaque règle métier, écrivez un test unitaire qui vérifie qu'on **ne peut pas violer la règle**.

**Exemples de règles à tester (cas d'erreur)** :
- Un ticket ne peut pas avoir un titre vide
- Un ticket ne peut pas avoir un titre contenant uniquement des espaces
- Un utilisateur ne peut pas avoir un username vide
- Un ticket fermé ne peut plus être assigné
- Un ticket fermé ne peut pas être re-fermé
- Un ticket ne peut pas être assigné sans ID d'agent
- Les valeurs du Status sont bien limitées aux 4 valeurs attendues (OPEN, IN_PROGRESS, CLOSED, RESOLVED)

---

## Étape 4 : Vérifier qu'on ne peut pas contourner

Testez les tentatives de contournement des règles métier.

**Exemples de tests de non-contournement** :
- On ne peut pas modifier le statut d'un ticket fermé en le réassignant
- Les transitions de statut respectent un ordre logique (OPEN → IN_PROGRESS → CLOSED)
- On ne peut pas passer directement de OPEN à CLOSED sans assignation (si c'est une règle métier)
- On ne peut pas créer un ticket sans créateur
- On ne peut pas modifier les attributs immuables après création (si applicable)

---

## Étape 5 : Valider

Vérifiez que tous vos tests passent :

```bash
pytest tests/domain/
```

Si vous voulez vérifier la couverture (optionnel) :

```bash
pytest tests/domain/ --cov=src/domain
```

---

## ✅ Checklist avant de soumettre

**Tests** :
- [ ] Chaque règle métier a un test pour le cas nominal
- [ ] Chaque règle métier a un test pour les cas d'erreurs (au moins les plus courants)
- [ ] Tests de non-contournement écrits
- [ ] `pytest tests/domain/` vert (tous les tests passent)

**Git** :
- [ ] Commits réguliers pendant la séance
- [ ] Tag `TD1b` poussé :
  ```bash
  git tag TD1b
  git push origin TD1b
  ```

---

💡 **Rappel** : L'objectif n'est pas la quantité de tests, mais la **qualité** : couvrir toutes les règles métier et s'assurer qu'on ne peut pas les contourner.
