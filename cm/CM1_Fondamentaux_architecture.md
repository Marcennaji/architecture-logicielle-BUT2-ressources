---
marp: true
theme: default
paginate: true
title: CM1 — Fondamentaux de l'architecture logicielle
style: |
  section {
    font-family: "Liberation Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #1f1f1f;
  }
  h1, h2, h3 {
    color: #004f9f;
  }
  h1 {
    border-bottom: 2px solid #d0d7de;
    padding-bottom: 0.3em;
  }
  code {
    background: #f6f8fa;
    padding: 0.1em 0.3em;
    border-radius: 3px;
  }
  pre code {
    font-size: 0.75em;
  }
  table {
    font-size: 0.9em;
  }
---

# 🧱 CM1 : Fondamentaux de l'architecture logicielle

BUT Informatique — Ressource R4.01 « Architecture logicielle »  
Enseignant : Marc Ennaji  

🛠 Objectif du cours :  
Comprendre **pourquoi** l'architecture logicielle est essentielle et maîtriser les **principes fondamentaux** qui guident toute bonne conception.

---

## 🧩 Plan du cours

1. Pourquoi une architecture logicielle ?
2. L'architecture à l'ère des assistants de codage IA
3. **Principes fondamentaux** :
   - Cohésion
   - Couplage
   - Gestion des dépendances
   - Séparation des responsabilités
   - Inversion de dépendances
4. **Architecture hexagonale** (Ports & Adapters)
5. Présentation du projet ticketing

---

## 🚀 1. Pourquoi parler d'architecture ?

Sans vraie architecture, on obtient vite :

- Du **code spaghetti** 🍝 *(attention aux indigestions)*
- Une application **difficile à comprendre**
- Des bugs qui reviennent en boucle
- Une application **impossible à tester**
- Une appli qui ne supporte pas bien les évolutions

👉 L'architecture sert à organiser le logiciel pour qu'il soit **vivable** sur le long terme.

---

## 🎯 Objectifs d'une bonne architecture

Une bonne architecture doit aider à :

- 🔧 **Maintenir** : corriger, faire évoluer
- 📦 **Modulariser** : pouvoir changer une partie sans tout casser
- 🧪 **Tester** : isoler le métier pour le tester sans tout l'environnement
- 🌱 **Faire évoluer** : ajouter des fonctionnalités sans tout réécrire
- 🙋‍♀️ **Comprendre** : nouveaux développeurs qui arrivent sur le projet

> *Plus l'architecture est pensée, moins on "jette et réécrit" les applis.*

---

## 🤖 2. L'ère du "vibe coding" et des assistants IA

**« Avec GitHub Copilot, ChatGPT, Cursor... je code par "intuition" et ça marche.  
Du coup l'architecture, c'est moins important ? »**

❌ **FAUX.** C'est même l'inverse.

💬 *Le "vibe coding" (coder à l'instinct avec l'IA) a sa place pour prototyper ou explorer.  
Mais en production sans maîtrise des fondamentaux → dette technique garantie.*

---

## 🤖 Pourquoi l'architecture devient PLUS importante (1/3)

1. **"Vibe coding" = productivité à court terme, chaos à moyen terme**
   - L'IA + votre intuition → Code qui marche *maintenant*
   - Mais sans vision architecturale → Dette technique exponentielle
   - *Dans 6 mois : "Qui a écrit ce code ?" — Spoiler : c'était vous + l'IA*

2. **L'IA suit des instructions, elle ne conçoit pas de systèmes**
   - Elle peut respecter une architecture… *si vous lui expliquez laquelle*
   - Elle ne sait pas si votre "vibe" justifie une exception aux règles
   - Elle amplifie vos décisions (bonnes **ou** mauvaises)

---

## 🤖 Pourquoi l'architecture devient PLUS importante (2/3)

3. **Le "vibe" ne scale pas (sauf si c'est le vibe d'un expert)**
   - 100 lignes de code → Intuition suffit (même pour un junior)
   - 10 000 lignes → Il faut une structure claire
   - 100 000 lignes → Seule l'intuition **fondée sur des principes** fonctionne
   - *Le "vibe" d'un senior avec 10 ans d'expérience ≠ le "vibe" d'un junior qui découvre*

---

## 🤖 Pourquoi l'architecture devient PLUS importante (3/3)

4. **Votre valeur = comprendre le système, pas juste taper du code**
   - IA + "vibe" → N'importe qui peut générer du code fonctionnel
   - Ingénieur → Seuls ceux qui maîtrisent les concepts peuvent concevoir un système cohérent
   - Questions que l'IA ne peut pas trancher :
     * Où placer la frontière domaine/infrastructure ?
     * Ce couplage est-il acceptable *dans ce contexte* ?
     * Faut-il sacrifier la pureté pour la simplicité ici ?

---

## 🎯 À retenir ! (1/2)

> **IA + "vibe coding + maîtrise insuffisante de l'archi" = conduire une Ferrari sans permis.**  
> Vous allez vite… droit dans le mur.

**Usages légitimes du "vibe coding" :**
- ✅ Prototypage rapide / POC
- ✅ Scripts one-shot
- ✅ Exploration d'une nouvelle techno

**Mais en production, le "vibe" sans fondamentaux = illusion de compétence :**
- ✅ Ça marche maintenant (court terme)
- ❌ Ça ne scale pas (moyen terme)
- ❌ Personne ne comprend le code dans 3 mois (long terme)

---

## 🎯 À retenir ! (2/2)

💡 **L'IA code très bien. Aucune IA n'est ingénieure logicielle.**

Un **"vibe coder"** génère du code qui fonctionne *maintenant*.  
Un **ingénieur logiciel** conçoit des systèmes cohérents, maintenables, évolutifs.

**L'intuition a de la valeur... quand elle est fondée sur l'expérience :**
- Senior qui "vibe" = 10 ans de patterns intégrés → souvent juste ✅
- Junior qui "vibe" = copier-coller sans comprendre → dette technique ❌

**Ce cours vous apprend les fondamentaux** pour que, dans 5 ou 10 ans :
- Votre intuition soit fiable
- Vous ne soyez pas remplacés par GPT-12 + un stagiaire qui "vibe" 💸 

---

## 🧠 3. Principes fondamentaux

Ces principes sont **universels** — ils s'appliquent quelle que soit l'architecture choisie.

Les maîtriser, c'est pouvoir :
- Évaluer la qualité d'un code existant
- Guider une IA efficacement
- Faire les bons choix de conception

---

## 3.1 La cohésion

> **Ce qui va ensemble doit rester ensemble.**

Une classe, un module, un service doit avoir une **responsabilité claire et focalisée**.

✅ **Forte cohésion** (bien) :
```python
class ShoppingCart:
    def add_item(self, item): ...
    def remove_item(self, item): ...
    def calculate_total(self): ...
    def apply_discount(self, code): ...
```

---
## 3.1 La cohésion

❌ **Faible cohésion** (problème) :
```python
class ShoppingCart:
    def add_item(self, item): ...
    def send_email(self, to, subject): ...  # ❌ Rien à voir !
    def generate_pdf_report(self): ...      # ❌ Pas sa responsabilité
```

---

## 3.1 La cohésion — pourquoi c'est important ?

**Faible cohésion = problèmes garantis :**

- 🐛 Modifications à un endroit cassent des choses sans rapport
- 🧪 Tests difficiles : il faut mocker des choses non liées
- 🤯 Code difficile à comprendre : "cette classe fait quoi exactement ?"
- 🔄 Réutilisation impossible : tout est mélangé

**Forte cohésion = bénéfices :**

- ✅ Code auto-documenté par sa structure
- ✅ Tests ciblés et simples
- ✅ Évolutions localisées

---

## 3.2 Le couplage

> **Moins les modules dépendent les uns des autres, mieux c'est.**

Le couplage mesure à quel point un module est **lié** à d'autres.

```text
Fort couplage                      Faible couplage
      A ←──────→ B                      A ──→ Interface ←── B
      │          │                           (contrat)
      ↓          ↓
      C ←──────→ D                 Les modules ne se connaissent 
                                   que via des abstractions
Tout est connecté à tout
→ Modifier A impacte B, C, D
```

---

## 3.2 Le couplage — comparaison

| ❌ **Fort couplage** | ✅ **Faible couplage** |
|---------------------|------------------------|
| **Code :** | **Code :** |
| `class OrderService:` | `class OrderService:` |
| `  self.db = MySQLDatabase()` | `  def __init__(self, repo: OrderRepository,` |
| `  self.mailer = SmtpMailer()` | `                notifier: Notifier):` |
|  | `    self.repo = repo  # Interface` |
| **Problèmes :** | **Bénéfices :** |
| • Impossible de tester sans MySQL/SMTP | • Testable avec fakes |
| • Changer de DB = réécrire le service | • Changer MySQL → PostgreSQL = 0 impact |
| • Changer d'email = réécrire | • Changer SMTP → SMS = 0 impact |

---

## 3.3 Les dépendances

Une **dépendance** = quelque chose dont votre code a besoin pour fonctionner.

| Type | Exemples | Risque |
|------|----------|--------|
| **Infrastructure** | Base de données, système de fichiers | Changement coûteux |
| **Framework** | Spring, Django, Symfony | Couplage au cycle de vie du framework |
| **Services externes** | API paiement, météo, IA | Indisponibilité, changements d'API |
| **Bibliothèques** | PDF, logging, validation | Obsolescence, failles |

👉 **Plus votre code dépend directement de ces éléments, plus il est fragile.**

---

## 3.4 Séparation des responsabilités

> **Chaque composant doit avoir UNE raison de changer.**

C'est le principe **SRP** (Single Responsibility Principle).

❌ **Classe "God Object"** qui fait tout :

```python
class OrderManager:
    def create_order(self): ...
    def validate_payment(self): ...
    def send_confirmation_email(self): ...
    def generate_invoice_pdf(self): ...
    def update_stock(self): ...
    def calculate_shipping(self): ...
    def apply_loyalty_points(self): ...
```

→ 7 raisons de changer cette classe = 7 sources de bugs potentiels à chaque modif.

---

## 3.4 Séparation — la bonne approche

✅ **Chaque responsabilité isolée** :

```python
class OrderService:           # Création de commande
class PaymentService:         # Validation paiement  
class NotificationService:    # Envoi emails/SMS
class InvoiceGenerator:       # Génération PDF
class StockService:           # Gestion stock
class ShippingCalculator:     # Calcul livraison
class LoyaltyService:         # Points fidélité
```

**Avantages :**
- Chaque classe est simple et focalisée
- On peut modifier le calcul de livraison sans risquer de casser les emails
- On peut tester chaque responsabilité indépendamment

---

## 3.5 Inversion de dépendances

> **Les modules de haut niveau ne doivent pas dépendre des modules de bas niveau.  
> Les deux doivent dépendre d'abstractions.**

C'est le **D** de SOLID — et c'est **fondamental** pour l'architecture hexagonale.

---

## 3.5 Inversion — avant/après

```text
❌ Classique (problème) :              ✅ Inversé (solution) :

+--------------+                      +---------------------------+
|    Métier    |                      | +---------------------+   |
+------+-------+                      | | Métier              |   |
       |                              | +---------------------+   |
       | dépend de                    | | <<interface>>       |   | DOMAINE
       v                              | | Repository          |   |
+--------------+                      | +-----------^---------+   |
|   Database   |                      +-------------|-------------+
+--------------+                                    |
                                                    | implémente
Le métier connaît MySQL                             |
                                            +-----------------+
                                            | Database (MySQL)|
                                            +-----------------+
```

**Avant :** Métier dépend de la DB → Tester = installer MySQL → Changer de DB = réécrire métier  
**Après :** Métier définit l'interface → Tester = injecter un fake → Changer de DB = nouvel adapter

👉 **C'est le cœur de l'architecture hexagonale** (voir partie 4).

---

## 3.6 Le rôle des tests dans l'architecture

> **Les tests ne servent pas qu'à détecter les bugs.  
> Ils révèlent (et forcent) la qualité de votre architecture.**

**Code difficile à tester = Code mal architecturé**

Si vous devez :
- Instancier 15 dépendances pour tester une fonction → ❌ Trop couplé
- Lancer une DB pour tester une règle métier → ❌ Pas d'inversion de dépendances
- Mocker la moitié de l'application → ❌ Faible cohésion

👉 **Les tests sont un détecteur de problèmes architecturaux.**

---

## 3.6 TDD : piloter l'architecture par les tests

**TDD (Test-Driven Development)** : Écrire le test **AVANT** le code.

```text
1. ✍️  Écrire un test qui échoue (Red)
2. ✅  Écrire le code minimal pour passer (Green)
3. ♻️  Refactorer pour améliorer (Refactor)
```

**Bénéfices architecturaux :**
- Force la testabilité et réduit le couplage
- Impose la cohésion (test complexe = trop de responsabilités)
- Garantit l'inversion (le test définit l'interface)

💡 *TDD ne garantit pas une bonne architecture, mais une mauvaise architecture ne survit pas au TDD.*

---

## 🎯 Récapitulatif des principes

| Principe | Question à se poser |
|----------|---------------------|
| **Cohésion** | Cette classe/module a-t-elle une responsabilité claire et unique ? |
| **Couplage** | Si je modifie ce module, combien d'autres sont impactés ? |
| **Dépendances** | Mon code métier dépend-il directement de la technique ? |
| **Responsabilités** | Combien de raisons cette classe a-t-elle de changer ? |
| **Inversion** | Qui définit les interfaces : le métier ou la technique ? |

💡 **Ces principes guident TOUTES les décisions architecturales.**

---

## 🛡️ 4. Architecture hexagonale (Ports & Adapters)

### 4.1 Le problème à résoudre

❌ **Code "framework-first" typique** :

```python
@app.post("/tickets")
def create_ticket(request: Request, db: Session = Depends(get_db)):
    data = request.json()
    
    # Validation métier dans le controller 😬
    if len(data["title"]) < 3:
        raise HTTPException(400, "Titre trop court")
    
    # Accès direct à la DB 😬
    ticket = TicketModel(title=data["title"], status="open")
    db.add(ticket)
    db.commit()
    
    return {"id": ticket.id}
```

**Problèmes :**
- 🧪 Impossible de tester la règle métier sans lancer FastAPI + DB  
  *"Pour tester 3 lignes, tu installes MySQL, tu lances un serveur web, tu fais un café..."* ☕
- 🔄 Changer de framework = tout réécrire
- 🐛 Logique métier éparpillée partout

---

### 4.2 La solution : séparer le métier de la technique

**Principe central de l'hexagonale :**

> **Le domaine métier au centre, indépendant de toute technique.**  
> La technique s'adapte au métier, pas l'inverse.

```text
+----------------------------------------------------------+
|                      ADAPTERS                            |
|  (FastAPI, SQLAlchemy, SMTP, APIs externes...)           |
|                                                          |
|  +----------------------------------------------------+  |
|  |              APPLICATION LAYER                     |  |
|  |   (Use Cases : orchestration métier + ports)       |  |
|  |                                                    |  |
|  |  +-------------------------------------------+     |  |
|  |  |          DOMAIN LAYER                     |     |  |
|  |  |  (Entités, Règles métier, Value Objects)  |     |  |
|  |  |  ZÉRO import technique                    |     |  |
|  |  +-------------------------------------------+     |  |
|  +----------------------------------------------------+  |
+----------------------------------------------------------+

        Dependencies flow INWARD ->
```

---

### 4.3 Les 3 couches (1/3)

#### 🟢 DOMAIN (le cœur)

**Contenu :**
- Entités (`Ticket`, `User`)
- Règles métier (`ticket.assign_to()`, `ticket.close()`)
- Value Objects (`TicketStatus`, `Email`)

**Règle d'or :**
> Aucun import de framework ou lib technique (FastAPI, SQLAlchemy, etc.)

---

### 4.3 Les 3 couches — exemple DOMAIN (2/3)

```python
# domain/ticket.py
from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

@dataclass
class Ticket:
    id: int
    title: str
    status: Status
    assignee_id: int | None = None
    
    def assign(self, user_id: int) -> None:
        """Règle métier : on ne peut assigner qu'un ticket ouvert."""
        if self.status != Status.OPEN:
            raise ValueError("Impossible d'assigner un ticket non ouvert")
        self.assignee_id = user_id
        self.status = Status.IN_PROGRESS
```

---

### 4.3 Les 3 couches — PORTS (3/4)

#### 🔵 PORTS (interfaces)

Des **contrats** (interfaces) définis par le métier :

```python
# ports/ticket_repository.py
from abc import ABC, abstractmethod

class TicketRepository(ABC):
    @abstractmethod
    def save(self, ticket: Ticket) -> None: pass
    
    @abstractmethod
    def get(self, ticket_id: int) -> Ticket | None: pass
    
    @abstractmethod
    def list_all(self) -> list[Ticket]: pass
```

👉 Le métier **définit** ce dont il a besoin, sans savoir **comment** c'est implémenté.

---

### 4.3 Les 3 couches — APPLICATION (4/5)

#### 🟡 APPLICATION (orchestration)

**Use cases** qui coordonnent le métier et les ports :

```python
# application/usecases/create_ticket.py
class CreateTicket:
    def __init__(self, ticket_repository: TicketRepository):
        self.repository = ticket_repository
    
    def execute(self, title: str) -> Ticket:
        ticket = Ticket(id=None, title=title, status=Status.OPEN)
        self.repository.save(ticket)
        return ticket
```

---

### 4.3 Les 3 couches — ADAPTERS (5/5)

**Implémentations concrètes** des ports :

```python
# adapters/db/ticket_repository_inmemory.py
class InMemoryTicketRepository(TicketRepository):
    def __init__(self):
        self.tickets: dict[int, Ticket] = {}
        self.next_id = 1
    
    def save(self, ticket: Ticket) -> None:
        if ticket.id is None:
            ticket.id = self.next_id
            self.next_id += 1
        self.tickets[ticket.id] = ticket
```

---

### 4.4 Pourquoi c'est puissant ?

✅ **Testabilité** :
```python
# Test du domaine (ZÉRO dépendance)
def test_cannot_assign_closed_ticket():
    ticket = Ticket(id=1, title="Bug", status=Status.CLOSED)
    with pytest.raises(ValueError):
        ticket.assign(user_id=42)

# Test du use case (InMemory fake)
def test_create_ticket():
    repo = InMemoryTicketRepository()
    use_case = CreateTicket(repo)
    ticket = use_case.execute("Bug critique")
    assert ticket.status == Status.OPEN
```

✅ **Évolutivité** : Passer de InMemory → SQLite → PostgreSQL sans toucher au métier

✅ **Clarté** : Chaque couche a un rôle précis

---

### 4.6 Justification pédagogique (1/2)

**Question légitime :** *Pourquoi l'hexagonale et pas une autre architecture ?*

**Réponses :**

1. 📚 **Impose structurellement les bons principes**
   - Séparation domaine/infrastructure visible immédiatement
   - Impossible de contourner l'inversion de dépendances

2. ⏱️ **Adaptée au format 20h TD**
   - Ni trop simple (layered classique), ni trop complexe (microservices)
   - Juste assez de contraintes pour apprendre les fondamentaux

---

### 4.6 Justification pédagogique (2/2)

3. 🧪 **Naturellement testable** : Tests par couche sans dépendances
   - Domain : pur (0 mock)
   - Use cases : fake repository (pas de vraie DB)
   - E2E : API complète

4. 🌍 **Transférable** : Fondation pour comprendre toutes les archi modernes
   - Clean Architecture, Onion, DDD → mêmes concepts
   - Compatible TDD, microservices, event-driven

> **💡 Pour aller plus loin :** Voir les annexes pour comparaisons détaillées des architectures et discussion monolithe vs microservices

---

## 🎯 5. Le projet : Ticketing System

### 5.1 Vue d'ensemble (1/2)

Vous allez implémenter un **système de tickets** (simplifié) en architecture hexagonale.

**Domaine métier :**
- `Ticket` : id, titre, statut, assigné à
- `User` : id, username
- `Status` : OPEN, IN_PROGRESS, RESOLVED, CLOSED

---
### 5.1 Vue d'ensemble (2/2)

**Use cases :**
- Créer un ticket
- Assigner un ticket à un utilisateur
- Changer le statut d'un ticket
- Récupérer un ticket / liste de tickets

**Adapters :**
- Persistance : InMemory → SQLite
- API : FastAPI (REST)

---

### 5.2 Progression des TDs

| TD | Objectif | Couche |
|----|----------|--------|
| **TD0** | Setup environnement, workflow Git | - |
| **TD1** | Modéliser le domaine (`Ticket`, `User`, `Status`) | Domain |
| **TD2** | Créer les use cases et ports | Application + Ports |
| **TD3** | Implémenter le repository SQLite | Adapters (DB) |
| **TD4** | Exposer l'API REST | Adapters (API) |

---

### 5.3 Évaluation

📊 **Répartition** :
- 30% : Projet final (GitHub, code fonctionnel)
- 40% : Exercices de TD (livrables intermédiaires)
- 30% : Contrôle final (analyse de code architectural)

⚠️ **Important** :
- 70% de la note **sans IA** (TD présentiel + Contrôle)
- L'IA est **autorisée** pour le projet à la maison
- Mais **comprendre** l'architecture reste indispensable

📖 Grille détaillée : `td/evaluation.md`

---

### 5.4 Ressources

📦 **Template de code** :  
https://github.com/Marcennaji/ticketing_starter

📚 **Documentation TDs** :  
https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources

🔧 **Technologies** :
- Python 3.11+
- FastAPI (web framework)
- SQLite (base de données, module `sqlite3` intégré)
- pytest (tests)

🚀 **Prérequis** : Guide de démarrage à suivre **AVANT le TD0**

---

## 🎯 Récapitulatif (1/2)

Vous avez maintenant :

✅ Compris **pourquoi** l'architecture est essentielle (encore plus avec l'IA)

✅ Découvert les **principes fondamentaux** :
- Cohésion, couplage, dépendances
- Séparation des responsabilités
- Inversion de dépendances

---

## 🎯 Récapitulatif (2/2)

✅ Découvert l'**architecture hexagonale** :
- Domain (métier pur)
- Ports (interfaces)
- Application (use cases)
- Adapters (implémentations)

✅ Une vision du **projet ticketing**

➡ **Prochaine étape** : TD0 (prise en main environnement + workflow)

---

## 📚 Pour aller plus loin

**Annexes du cours (PDF) :**
- [Comparaison des architectures](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/export/CM1_annexe_comparaison_architectures.pdf) — Layered, MVC, MVVM, Microservices, Hexagonale
- [Architecture vs Design](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/export/CM1_annexe_architecture_vs_design.pdf) — Clarification conceptuelle
- [TDD et architecture](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/export/CM1_annexe_TDD.pdf) — Les tests comme détecteur de qualité
- [Monolithe vs Microservices](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/export/CM1_annexe_monolithe_microservices.pdf) — Démystifier le monolithe

**Articles de référence (français) :**
- [Architecture Hexagonale : trois principes et un exemple](https://blog.octo.com/architecture-hexagonale-trois-principes-et-un-exemple-dimplementation) (OCTO Technology)
- [Hexagonal Architecture expliquée simplement](https://lesdieuxducode.com/blog/2020/11/architecture-hexagonale--la-structure-ideale-pour-vos-applications-metier) (Les Dieux du Code)

---

# 🏁 Fin du cours

📂 **Toutes les ressources sont sur GitHub :**  
https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources

❓ **Questions ?**
