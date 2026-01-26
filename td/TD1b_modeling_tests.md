# TD1b — Tests unitaires du domaine

## 📦 Séance TD1b (2h) → Tag `TD1b` (optionnel)

**Durée : 1 séance de 2h** (séance suivant TD1a)

> 📋 **Contexte du TD1** :
> - **TD1a + TD1b** constituent ensemble le **TD1 complet** sur la modélisation du domaine métier
> - Le tag `TD1b` est **optionnel** et permet d'obtenir un **feedback intermédiaire** si vous le souhaitez
> - **Correction finale de TD1** : déclenchée automatiquement **1 semaine après la séance TD1b**
> - La correction évalue l'**état le plus récent du code sur la branche `main`** (pas de tag obligatoire)
> 
> 💡 Prenez le temps nécessaire pour avoir un domaine métier solide avant la deadline de correction !

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

## Étape 0 : Vérifier la protection des transitions de statut (5-10 min)

**Objectif** : S'assurer que les règles de transition de statut ne peuvent pas être contournées.

### ✅ Checklist de vérification

Vérifiez dans votre `src/domain/status.py` et `src/domain/ticket.py` :

- [ ] **Status est un Enum** Python :
  ```python
  from enum import Enum
  
  class Status(Enum):
      OPEN = "open"
      IN_PROGRESS = "in_progress"
      RESOLVED = "resolved"
      CLOSED = "closed"
  ```
  💡 Si ce n'est pas le cas, corrigez maintenant avant de continuer.

- [ ] Le statut du ticket est **privé** : `_status` (avec underscore) au lieu de `status`
- [ ] Une **propriété lecture seule** permet d'accéder au statut :
  ```python
  @property
  def status(self) -> Status:
      return self._status
  ```
- [ ] Vos méthodes métier (`close()`, `resolve()`, `reopen()`, etc.) **valident les transitions** avant de modifier `_status`

💡 **Si tout est bon** : Passez directement à l'Étape 1.

### 📝 Alternative : méthode `transition_to()` centralisée (optionnel)

Si vous préférez centraliser la logique de transition dans une seule méthode :

**Fichier** : `src/domain/ticket.py`

```python
class Ticket:
    # Transitions autorisées
    ALLOWED_TRANSITIONS = {
        Status.OPEN: [Status.IN_PROGRESS],
        Status.IN_PROGRESS: [Status.RESOLVED],
        Status.RESOLVED: [Status.CLOSED, Status.IN_PROGRESS],
        Status.CLOSED: [Status.IN_PROGRESS],
    }
    
    def transition_to(self, new_status: Status, updated_at: datetime) -> None:
        """Fait transiter le ticket vers un nouveau statut."""
        if new_status not in self.ALLOWED_TRANSITIONS.get(self._status, []):
            raise InvalidStatusTransitionError(
                f"Cannot transition from {self._status.value} to {new_status.value}"
            )
        self._status = new_status
        self.updated_at = updated_at
```

Vos méthodes métier deviennent alors :
```python
def close(self, closed_at: datetime):
    self.transition_to(Status.CLOSED, closed_at)  # Valide automatiquement la transition
    self.closed_at = closed_at
```

💡 **Les deux approches sont valables** :
- **Méthodes autonomes** : chaque méthode (`close()`, `resolve()`) fait sa propre validation
- **Avec `transition_to()`** : délègue toute la validation des transitions à `transition_to()`

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
- Un ticket assigné peut être démarré (transition vers IN_PROGRESS)
- Un utilisateur peut être créé avec un username valide
- Un ticket a le statut OPEN à sa création

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
- Les transitions de statut respectent l'ordre logique que vos règles métier ont définies
- On ne peut pas passer directement de OPEN à RESOLVED (il faut passer par IN_PROGRESS)
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

- [ ] Chaque règle métier a des test pour les cas d'utilisation normale
- [ ] Chaque règle métier a des tests qui vérifient qu'une exception est lancée, si cette règle n'est pas respectée
- [ ] `pytest tests/domain/` vert (tous les tests passent)


---

💡 **Rappel** : L'objectif n'est pas la quantité de tests, mais la **qualité** : couvrir toutes les règles métier et s'assurer qu'on ne peut pas les contourner.

## Si vous avez fini avant la fin de séance
Enrichissez encore votre domaine métier (entités et/ou règles métier) et créez les tests unitaires associés.
