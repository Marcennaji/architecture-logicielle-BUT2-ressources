# TD1b — Tests unitaires du domaine

## 📦 Séance TD1b (2h) → Tag `TD1b` (optionnel)

**Durée : 1 séance de 2h** (séance suivant TD1a)

> 📋 **Contexte du TD1** :
> - **TD1a + TD1b** constituent ensemble le **TD1 complet** sur la modélisation du domaine métier
> - Le tag `TD1b` est **optionnel** et permet d'obtenir un **feedback intermédiaire** si vous le souhaitez
> - Le tag **`TD1` (obligatoire)** doit être créé quand vous avez terminé l'ensemble du domaine (TD1a + TD1b)
> - **Deadline pour `TD1`** : avant la séance **TD2b** (vous avez donc encore ~1 semaine après TD1b pour finaliser)
> - La **correction du TD1 sera déclenchée** uniquement lorsque vous pousserez le tag `TD1`
> 
> 💡 Il n'est pas obligatoire de pousser les tags en séance ! Prenez le temps nécessaire pour avoir un domaine métier solide.

### Objectif

Écrire des tests unitaires qui couvrent **toutes les règles métier** du domaine, y compris les cas d'erreur. L'objectif est de garantir que les règles métier sont implémentées, et qu'on ne peut pas les contourner.

### Ce qui est attendu

- ✅ Chaque règle métier a un test qui vérifie le cas nominal
- ✅ Chaque règle métier a un test qui vérifie les cas d'erreurs (au moins les plus courants)
- ✅ Tous les tests passent : `pytest tests/domain/` vert
- ✅ Un code applicatif ne peut pas contourner par inadvertance les règles métier

Voir [evaluation.md](evaluation.md) pour le système de notation.

> ⚠️ **Important** : Les exemples de règles métier donnés dans ce TD sont indicatifs. Vous devez les adapter en fonction des entités et des règles métier que **vous** avez réellement implémentées dans TD1a. Chaque étudiant peut avoir des règles légèrement différentes.

---

## Étape 1 : Lister les règles métier

Avant de tester, listez (si vous ne l'avez pas déjà fait) dans le fichier docs/domain-notes.md, **toutes les règles métier** de votre domaine :

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

## Étape 3 : Tester les cas d'erreur et le non-contournement

Pour chaque règle métier, écrivez un test unitaire qui vérifie qu'on **ne peut pas violer la règle**, directement ou indirectement.

**Exemples de tests à écrire (dépendent de vos règles métier)** :
- Un ticket ne peut pas avoir un titre vide
- Un ticket ne peut pas avoir un titre contenant uniquement des espaces
- Un utilisateur ne peut pas avoir un username vide
- Un ticket fermé ne peut plus être assigné
- Un ticket fermé ne peut pas être re-fermé
- On ne peut pas modifier le statut d'un ticket fermé en le réassignant (contournement)
- Les transitions de statut respectent un ordre logique (OPEN → IN_PROGRESS → CLOSED)
- On ne peut pas passer directement de OPEN à CLOSED sans assignation (si c'est une règle métier)
- Un ticket ne peut pas être assigné sans ID d'agent
- On ne peut pas créer un ticket sans créateur
- On ne peut pas modifier les attributs immuables après création (si applicable)
- Les valeurs du Status sont bien limitées aux 4 valeurs attendues (OPEN, IN_PROGRESS, CLOSED, RESOLVED)

---

## Étape 4 : Valider

Vérifiez que tous vos tests passent :

```bash
pytest tests/domain/
```
---

## ✅ Checklist avant de soumettre

**Tests** :
- [ ] Chaque règle métier a des test pour les cas d'utilisation normale
- [ ] Chaque règle métier a des tests qui vérifient qu'une exception est lancée, si cette règle n'est pas respectée
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
