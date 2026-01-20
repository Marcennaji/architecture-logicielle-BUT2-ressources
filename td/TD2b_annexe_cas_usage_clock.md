# Annexe TD2b — Cas d'usage concret : Pourquoi un port Clock ?

**🎯 Objectif** : Comprendre l'intérêt du port Clock à travers un exemple métier réel.

---

## 📋 Cas d'usage : Réouverture limitée à 7 jours

### Règle métier

> **Un ticket fermé peut être réouvert uniquement dans les 7 jours suivant sa fermeture.**

Après 7 jours, le ticket est archivé et ne peut plus être modifié.

---

## 🤔 Question : Pourquoi cette règle justifie-t-elle un port Clock ?

### Analyse

Cette règle n'est **pas** un simple timestamp (`created_at`, `updated_at`).  
C'est une **décision métier** basée sur un **calcul temporel** :

```python
temps_écoulé = maintenant - date_fermeture
peut_rouvrir = temps_écoulé <= 7 jours
```

**Conséquences** :
- Le comportement du système **change selon le temps**
- Il faut tester **plusieurs scénarios temporels** (jour 6, 7, 8...)
- La logique doit être **reproductible** pour les tests

---

## ❌ Solution 1 : Sans port Clock (problématique)

### Implémentation naïve

```python
class Ticket:
    def can_be_reopened(self) -> bool:
        if self.status != Status.CLOSED:
            return False
        
        # ❌ datetime.now() = dépendance cachée au système
        time_since_closure = datetime.now(timezone.utc) - self.closed_at
        return time_since_closure <= timedelta(days=7)
```

### Problèmes

#### 1. Tests non déterministes
```python
def test_cannot_reopen_after_7_days():
    # Comment tester un ticket fermé il y a 8 jours ?
    ticket = Ticket(...)
    ticket.closed_at = datetime.now() - timedelta(days=8)
    
    # ⚠️ Ce test peut échouer selon l'instant exact d'exécution
    # Si datetime.now() dans le test != datetime.now() dans can_be_reopened()
    assert not ticket.can_be_reopened()
```

#### 2. Impossible de tester les cas limites
```python
# Comment tester "exactement 7 jours" ?
# Comment tester "7 jours + 1 seconde" ?
# ➡️ Impossible sans attendre réellement ou sans hacks (mocks globaux)
```

#### 3. Domaine impur (effet de bord)
```python
# La méthode lit l'horloge système = effet de bord
# Résultat différent à chaque appel, même avec le même ticket
ticket.can_be_reopened()  # True (jour 6)
# ... attendre un jour ...
ticket.can_be_reopened()  # False (jour 8)
```

---

## ✅ Solution 2 : Avec port Clock (robuste)

### Implémentation propre

```python
class Ticket:
    REOPEN_DEADLINE_DAYS = 7  # constante de règle métier
    
    def can_be_reopened(self, current_time: datetime) -> bool:
        """
        Vérifie si le ticket peut être réouvert.
        
        Args:
            current_time: L'heure actuelle (injectée)
        """
        if self.status != Status.CLOSED:
            return False
        
        if self.closed_at is None:
            return False
        
        # ✅ Calcul pur : même entrée = même sortie
        time_since_closure = current_time - self.closed_at
        return time_since_closure <= timedelta(days=self.REOPEN_DEADLINE_DAYS)
    
    def reopen(self, current_time: datetime, updated_at: datetime):
        """
        Rouvre un ticket fermé.
        
        Raises:
            InvalidTicketStateError: Si réouverture impossible
        """
        # Valider que le ticket est fermé
        if self._status != Status.CLOSED:
            raise InvalidTicketStateError(
                f"Cannot reopen ticket in {self._status.value} status. "
                "Only CLOSED tickets can be reopened."
            )
        
        # Valider qu'on a un horodatage de fermeture
        if self.closed_at is None:
            raise InvalidTicketStateError(
                "Cannot reopen ticket: Ticket has no closure timestamp"
            )
        
        # Valider le délai de 7 jours
        if not self.can_be_reopened(current_time):
            days_since_closure = (current_time - self.closed_at).days
            raise InvalidTicketStateError(
                f"Cannot reopen ticket: closed {days_since_closure} days ago "
                f"(maximum: {self.REOPEN_DEADLINE_DAYS} days)"
            )
        
        # Appliquer la réouverture
        self._status = Status.IN_PROGRESS
        self.updated_at = updated_at
```

### Use case

Le use case utilise le port Clock pour obtenir le temps actuel, puis le passe au domaine :

```python
class ReopenTicketUseCase:
    def __init__(self, ticket_repo: TicketRepository, clock: Clock):
        self.ticket_repo = ticket_repo
        self.clock = clock  # ✅ Port Clock injecté dans le use case
    
    def execute(self, ticket_id: str) -> Ticket:
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")
        
        # Le use case obtient le temps via Clock
        current_time = self.clock.now()
        
        # Le domaine reçoit datetime en paramètre (pas de dépendance à Clock)
        ticket.reopen(current_time, current_time)
        
        return self.ticket_repo.save(ticket)
```

### Tests déterministes

```python
def test_can_reopen_within_7_days():
    """✅ Test précis : ticket fermé il y a 6 jours."""
    base_time = datetime(2026, 1, 18, 10, 0, 0, tzinfo=timezone.utc)
    closed_time = base_time - timedelta(days=6)
    
    ticket = Ticket(
        id="t-1",
        title="Bug",
        creator_id="user-1",
        created_at=closed_time - timedelta(days=1),
        updated_at=closed_time,
    )
    ticket._status = Status.CLOSED
    ticket.closed_at = closed_time
    
    # Test avec temps contrôlé
    assert ticket.can_be_reopened(base_time) == True


def test_can_reopen_exactly_at_deadline():
    """✅ Test précis : exactement 7 jours."""
    base_time = datetime(2026, 1, 18, 10, 0, 0, tzinfo=timezone.utc)
    closed_time = base_time - timedelta(days=7)
    
    ticket = Ticket(...)
    ticket._status = Status.CLOSED
    ticket.closed_at = closed_time
    
    # Exactement la limite
    assert ticket.can_be_reopened(base_time) == True


def test_cannot_reopen_after_deadline():
    """✅ Test précis : 7 jours + 1 seconde."""
    base_time = datetime(2026, 1, 18, 10, 0, 0, tzinfo=timezone.utc)
    closed_time = base_time - timedelta(days=7, seconds=1)
    
    ticket = Ticket(...)
    ticket._status = Status.CLOSED
    ticket.closed_at = closed_time
    
    # Dépassement de 1 seconde
    assert ticket.can_be_reopened(base_time) == False


def test_reopen_use_case_after_deadline_raises_error():
    """✅ Test du use case avec message d'erreur clair."""
    repo = InMemoryTicketRepository()
    base_time = datetime(2026, 1, 18, 10, 0, 0, tzinfo=timezone.utc)
    clock = FixedClock(base_time)
    
    # Ticket fermé il y a 8 jours
    ticket = Ticket(...)
    ticket._status = Status.CLOSED
    ticket.closed_at = base_time - timedelta(days=8)
    repo.save(ticket)
    
    use_case = ReopenTicketUseCase(repo, clock)
    
    # Vérifier que l'erreur contient le bon message
    with pytest.raises(InvalidTicketStateError) as exc:
        use_case.execute("t-1")
    
    assert "closed 8 days ago" in str(exc.value)
    assert "maximum: 7 days" in str(exc.value)
```

---

## 📊 Comparaison

| Aspect | Sans Clock | Avec Clock |
|--------|-----------|-----------|
| **Test jour 6** | ⚠️ Approximatif | ✅ Précis |
| **Test jour 7 exact** | ❌ Impossible | ✅ Facile |
| **Test jour 7 + 1s** | ❌ Impossible | ✅ Facile |
| **Reproductibilité** | ❌ Varie | ✅ Toujours identique |
| **Domaine pur** | ❌ Effet de bord | ✅ Fonction pure |
| **Parallélisation tests** | ⚠️ Fragile | ✅ Isolation parfaite |

---

## 🎯 Leçons clés

### 1. Le temps comme paramètre métier

Quand le temps intervient dans une **décision métier** (pas juste un timestamp), il devient un **paramètre** qu'il faut pouvoir contrôler.

**Dans le domaine** : le temps est reçu en paramètre (pas de dépendance externe) :

```python
# ✅ Bon : temps = paramètre du domaine
def can_be_reopened(self, current_time: datetime) -> bool:
    return current_time - self.closed_at <= timedelta(days=7)

# ❌ Mauvais : temps = dépendance cachée dans le domaine
def can_be_reopened(self) -> bool:
    return datetime.now() - self.closed_at <= timedelta(days=7)
```

**Dans le use case** : Clock est un port sortant injecté pour obtenir le temps actuel, qui est ensuite passé au domaine.

### 2. Tests précis sur les limites

Les **cas limites** sont critiques :
- Que se passe-t-il exactement à J+7 ?
- Et à J+7 + 1 seconde ?

Le port Clock permet de tester ces cas **à la seconde près**.

### 3. Fonction pure = testable

```python
# Fonction pure : même entrée → même sortie
can_reopen = ticket.can_be_reopened(datetime(2026, 1, 18, 10, 0, 0))
# ✅ Toujours le même résultat, peu importe quand on exécute

# Fonction impure : résultat variable
can_reopen = ticket.can_be_reopened()  # Lit datetime.now()
# ❌ Résultat change selon le moment d'exécution
```

---

## ⚖️ Quand utiliser un port Clock ?

### ✅ Port Clock justifié

- Règles métier avec **comparaisons temporelles** (SLA, deadline, âge)
- Calculs de **durées** ou **métriques temporelles**
- Décisions basées sur **l'écoulement du temps**
- Besoin de **tests précis** sur les cas limites

**Exemples** :
- "Ticket escaladé si non traité en 2h"
- "Réouverture limitée à 7 jours"
- "Promotion expirée après 30 jours"

### ❌ Port Clock non nécessaire

- Simple **enregistrement** de timestamps (`created_at`, `updated_at`)
- Pas de **logique métier** dépendant du temps
- Juste pour l'**audit** ou l'**affichage**

**Exemples** :
- Afficher "Créé le 18/01/2026"
- Logger "Modifié à 14h30"

---

## 💡 Conclusion

Le port Clock n'est **pas** de l'over-engineering quand :
1. Le temps fait partie de la **logique métier**
2. Vous avez besoin de **tests reproductibles**
3. Vous devez tester des **cas limites précis**

Dans le cas de la "réouverture sous 7 jours", le port Clock permet de :
- ✅ Tester **tous** les scénarios (J-1, J, J+1s...)
- ✅ Avoir un **domaine pur** (sans effets de bord)
- ✅ Écrire des tests **déterministes**
- ✅ Isoler complètement les tests

**Règle simple** : Si vous écrivez `if current_time > deadline` dans votre domaine, vous avez besoin du port Clock !

---

**➡️ Retour : [TD2b](TD2b_adding_horodating.md)**
