# TD2b — Ports sortants & horodatage

**⏰ Durée : 2h** | **🏷️ Tag (pour feedback) : `TD2b`** | **📋 Prérequis : TD2a fait et compris**

---

## 🎯 Objectifs

1. Implémenter l'horodatage des actions métier
2. Créer le use case `StartTicket`
3. Découvrir comment gérer les dépendances temporelles

> 💡 **Approche** : Réfléchir avant de coder. Appliquer les principes du TD2a.

---

## 📋 Partie 1 : Horodatage (AUTONOMIE)

### 🎯 Besoin

Enregistrer la date/heure quand un ticket est démarré (`started_at`).

**Cas d'usage** : statistiques, audit, métriques de performance.

### 🤔 Questions

**Q1.** Comment obtenir la date/heure actuelle en Python ?

**Q2.** Si on met `datetime.now()` dans le use case, pourquoi c'est problématique pour les tests ?

**Q3.** Au TD2a, comment avez-vous géré la base de données pour que les tests soient indépendants ?

**Q4.** Quelle architecture du TD2a pourrait s'appliquer ici ?

### 🎯 Livrable

Créez une solution permettant :

```python
# Production : heure système réelle
>>> horloge.now()
datetime(2026, 1, 16, 14, 32, 18)
>>> horloge.now()
datetime(2026, 1, 16, 14, 35, 22)

# Tests : heure fixe (déterministe)
>>> horloge_test.now()
datetime(2026, 1, 16, 14, 30, 0)
>>> horloge_test.now()
datetime(2026, 1, 16, 14, 30, 0)  # Toujours pareil !
```

**Contraintes** :
- ✅ Architecture hexagonale respectée
- ✅ Tests déterministes (même résultat à chaque exécution)

<details>
<summary>💡 Indices</summary>

- Le temps = dépendance externe (comme la DB)
- Même solution qu'au TD2a : interface + adapteurs
- Nommage (classique) proposé:
  - Port : `Clock`
  - Adaptateur production : `SystemClock`
  - Adaptateur test : `FixedClock`

</details>

---

## 📋 Partie 2 : Domaine

### 🎯 Spécifications

**Action** : Un agent démarre le traitement d'un ticket.

**Effets** :
- Enregistre `started_at`
- Transition : `OPEN` → `IN_PROGRESS`

**Validations métier** (à implémenter dans `ticket.start()`) :
1. Le ticket est assigné
2. L'agent qui démarre = agent assigné
3. Le ticket est `OPEN`

**À faire** :
1. Ajoutez le champ `started_at: Optional[datetime]` dans `Ticket`
2. Créez la méthode `start(agent_id, started_at)` avec les 3 validations métier
3. Créez les exceptions nécessaires (`TicketNotAssignedError`, `WrongAgentError`, `InvalidTicketStateError`)

---

## 📋 Partie 3 : Use Case (AUTONOMIE)

**Spécifications `StartTicketUseCase`** :

- **Entrées** : `ticket_id: str`, `agent_id: str`
- **Sortie** : Le ticket modifié
- **Dépendances** : Repository + Horloge (créée en Partie 1)

**Comportement** :
1. Récupérer le ticket depuis le repository
2. Vérifier existence (lever `TicketNotFoundError` si None)
3. Obtenir le timestamp depuis l'horloge
4. Appeler `ticket.start(agent_id, timestamp)` (qui fait les validations métier)
5. Sauvegarder le ticket
6. Retourner le ticket modifié

**À faire** : Créez `src/application/usecases/start_ticket.py`

---

## 📋 Partie 4 : Tests

Créez `tests/application/test_start_ticket.py` avec :

1. `test_start_ticket_success` → Succès nominal
2. `test_start_ticket_not_found` → TicketNotFoundError (validation use case)
3. `test_start_ticket_invalid_status` → InvalidTicketStateError (validation domaine)

**Clé** : Vérifier `ticket.started_at == temps_fixe` (déterminisme)

**Optionnel** : `test_start_ticket_not_assigned`, `test_start_ticket_wrong_agent`

---

## ✅ Critères de validation

**Architecture**
- [ ] Interface abstraite pour le temps (port Clock dans `src/ports/`)
- [ ] Adaptateur production (`SystemClock` utilisant `datetime.now()`)
- [ ] Adaptateur test (`FixedClock` avec temps fixe)
- [ ] Injection de Clock dans StartTicketUseCase
- [ ] Le domaine reçoit datetime en paramètre (pas de dépendance à Clock)

**Domaine**
- [ ] Champ `started_at`
- [ ] Méthode `start()` + 3 validations métier (assigné, bon agent, statut OPEN)
- [ ] Transition d'état correcte (OPEN → IN_PROGRESS)
- [ ] 3 exceptions créées pour le domaine (`TicketNotAssignedError`, `WrongAgentError`, `InvalidTicketStateError`)

**Use Case & Tests**
- [ ] StartTicketUseCase fonctionnel
- [ ] 3 tests minimum (success, not_found, invalid_status)
- [ ] Tests déterministes
- [ ] `pytest tests/` → 100% ✅

**Git**
- [ ] Commits réguliers en séance

---

## 🎓 Bonus (si temps)

**Nettoyer complètement le domaine**

Si vous aviez déjà une fonction `_now_utc()` ou des appels à `datetime.now()` dans votre domaine `Ticket` (pour `created_at`, `updated_at`, etc.), il faut également les supprimer pour être cohérent avec les principes du TD2b.

**Objectif** : Le domaine doit être **complètement pur**, sans aucune référence au temps système.

**À faire** :
1. Supprimer la fonction `_now_utc()` du domaine
2. Modifier les méthodes du domaine (`assign`, `transition_to`, `set_priority`) pour accepter un paramètre `updated_at: datetime`
3. Rendre `created_at` et `updated_at` obligatoires dans le constructeur de `Ticket`
4. Adapter tous les use cases (`CreateTicket`, `AssignTicket`) pour injecter le port `Clock` et passer les timestamps au domaine
5. Mettre à jour tous les tests pour passer explicitement les timestamps

**Avantage** : Architecture hexagonale strictement respectée, domaine testable sans effets de bord.

---

## 📚 Pour aller plus loin

**[Annexe : Cas d'usage concret du port Clock](TD2b_annexe_cas_usage_clock.md)**

Un exemple métier réel qui illustre pourquoi le port Clock est indispensable : la réouverture de ticket limitée à 7 jours.

Cette lecture approfondit votre compréhension du TD2b à travers un cas concret avec tests détaillés. À lire chez vous ou en fin de séance si vous avez terminé.

---

