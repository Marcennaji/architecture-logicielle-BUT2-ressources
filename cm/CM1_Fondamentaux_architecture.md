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
  table {
    font-size: 0.9em;
  }
---

# 🧱 CM1 : Fondamentaux de l'architecture logicielle

🎓 BUT Informatique — Ressource R4.01 « Architecture logicielle »  
👨‍🏫 Enseignant·e : _à compléter_  

🛠 Objectif du cours :  
Comprendre **pourquoi** l'architecture logicielle est essentielle et maîtriser les **principes fondamentaux** qui guident toute bonne conception.

---

## 🧩 Plan du cours

1. Pourquoi une architecture logicielle ?
2. L'architecture à l'ère de l'IA — **message clé** 🤖
3. **Principes fondamentaux** :
   - Cohésion
   - Couplage
   - Gestion des dépendances
   - Séparation des responsabilités
   - Inversion de dépendances
4. Panorama des architectures (survol)
5. Mini-exercice de synthèse

---

## 🚀 1. Pourquoi parler d'architecture ?

Sans vraie architecture, on obtient vite :

- Du **code spaghetti** 🍝
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

## 🤖 2. Et avec GitHub Copilot, ChatGPT & co ?

**« L'IA code à ma place, donc l'architecture, ouf, plus besoin… »**

❌ **FAUX.** C'est même l'inverse.

---

## 🤖 Pourquoi l'architecture devient PLUS importante

1. **L'IA suit des instructions, elle ne prend pas de décisions stratégiques**
   - Elle peut respecter une architecture… *si vous lui expliquez laquelle*
   - Elle ne sait pas si votre contexte justifie une exception

2. **Plus on génère vite, plus on a besoin de vision**
   - Sans direction claire → accumulation rapide de dette technique
   - L'IA produit du code cohérent *localement*, mais pas toujours *globalement*

3. **L'IA est un amplificateur**
   - Bonne architecture + IA → productivité décuplée ✅
   - Pas d'architecture + IA → chaos à grande vitesse ❌

4. **Votre valeur = les décisions que l'IA ne peut pas prendre**
   - Où placer la frontière entre domaine et infrastructure ?
   - Ce couplage est-il acceptable *dans ce contexte* ?
   - Faut-il sacrifier la pureté pour la simplicité ici ?

---

## 🎯 À retenir !

> **L'IA est semblable à un développeur expérimenté et ultra-rapide…  
> …qui débarque sur votre projet sans en connaître l'histoire ni la vision.**

Elle code (en général) très bien. Mais elle a besoin que **vous** lui donniez :
- 🧭 La direction (quelle architecture ?)
- 🚧 Les contraintes (quelles règles respecter ?)
- ⚖️ Les arbitrages (quand faire une exception ?)

💡 **L'IA est une excellente codeuse, pas (encore) une ingénieure logicielle.**

Un **codeur** maîtrise un langage et produit du code qui fonctionne.  
Un **ingénieur logiciel** conçoit des systèmes cohérents, maintenables, évolutifs.

*Ce cours vise à faire de vous des ingénieurs, pas juste des codeurs assistés par IA.*

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

## 3.2 Le couplage — exemple concret

❌ **Fort couplage** — le service connaît l'implémentation :

```python
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # ❌ Dépendance directe à MySQL
        self.mailer = SmtpMailer() # ❌ Dépendance directe à SMTP
    
    def create_order(self, order):
        self.db.insert("orders", order)  # ❌ Couplé à MySQL
        self.mailer.send(order.customer_email, "Commande créée")
```

**Problèmes :**
- Impossible de tester sans MySQL et serveur SMTP
- Changer de base de données = réécrire le service
- Changer de système d'email = réécrire le service

---

## 3.2 Le couplage — solution

✅ **Faible couplage** — le service dépend d'abstractions :

```python
class OrderService:
    def __init__(self, repository: OrderRepository, notifier: Notifier):
        self.repository = repository  # ✅ Interface
        self.notifier = notifier      # ✅ Interface
    
    def create_order(self, order):
        self.repository.save(order)
        self.notifier.notify(order.customer_email, "Commande créée")
```

**Bénéfices :**
- ✅ Testable avec des mocks/fakes
- ✅ On peut changer MySQL → PostgreSQL sans toucher au service
- ✅ On peut changer SMTP → SMS → Push sans toucher au service

---

## 3.3 Les dépendances

Une **dépendance** = quelque chose dont votre code a besoin pour fonctionner.

Types de dépendances :

| Type | Exemples | Risque |
|------|----------|--------|
| **Infrastructure** | Base de données, système de fichiers | Changement coûteux |
| **Framework** | Spring, Django, Symfony | Couplage au cycle de vie du framework |
| **Services externes** | API paiement, météo, IA | Indisponibilité, changements d'API |
| **Bibliothèques** | PDF, logging, validation | Obsolescence, failles |

👉 **Plus votre code dépend directement de ces éléments, plus il est fragile.**

---

## 3.3 Visualiser les dépendances

```text
❌ Dépendances directes partout :

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Service   │────►│   MySQL     │     │   Stripe    │
│   Métier    │────►│   Driver    │     │    API      │
│             │────►│             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │
       └────────────────────────────────►┌─────────────┐
                                         │   SMTP      │
                                         └─────────────┘

Le code métier connaît TOUT. Impossible à tester, impossible à faire évoluer.
```

---

## 3.3 Dépendances — la bonne approche

```text
✅ Le métier ne connaît que des interfaces :

                    ┌─────────────────┐
                    │  MySQL Driver   │
                    └────────┬────────┘
                             │ implémente
                             ▼
┌─────────────┐     ┌─────────────────┐
│   Service   │────►│  <<interface>>  │
│   Métier    │     │   Repository    │
└─────────────┘     └─────────────────┘
       │                     ▲
       │                     │ implémente
       │            ┌────────┴────────┐
       │            │  Fake (tests)   │
       │            └─────────────────┘
       │
       └──────────►┌─────────────────┐
                   │  <<interface>>  │
                   │    Notifier     │
                   └─────────────────┘
```

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

```text
❌ Classique (problème) :              ✅ Inversé (solution) :

┌──────────────┐                      ┌──────────────┐
│    Métier    │                      │    Métier    │
└──────┬───────┘                      └──────┬───────┘
       │ dépend de                           │ définit
       ▼                                     ▼
┌──────────────┐                      ┌──────────────┐
│   Database   │                      │ <<interface>>│
└──────────────┘                      │  Repository  │
                                      └──────────────┘
Le métier connaît MySQL                      ▲
                                             │ implémente
                                      ┌──────┴───────┐
                                      │   Database   │
                                      └──────────────┘
                                      La DB connaît l'interface
```

---

## 3.5 Inversion — pourquoi c'est puissant ?

**Avant (dépendance classique) :**
- Le métier dépend de la base de données
- Pour tester le métier, il faut une vraie DB
- Changer de DB = modifier le métier

**Après (dépendance inversée) :**
- Le métier définit ce dont il a besoin (interface)
- La DB s'adapte au contrat du métier
- Pour tester : on injecte un fake
- Changer de DB : on crée un nouvel adaptateur

👉 **C'est le cœur de l'architecture hexagonale (CM2).**

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

## 🏛 4. Panorama des architectures (survol)

Il existe de nombreuses architectures. Voici les principales familles :

| Architecture | Idée clé |
|--------------|----------|
| **Monolithique** | Tout en un bloc déployable |
| **N-tiers / Couches** | Séparation horizontale (UI / Métier / Data) |
| **MVC / MVVM** | Pattern pour les interfaces utilisateur |
| **SOA** | Services métier mutualisés (grands SI) |
| **Microservices** | Petits services autonomes et indépendants |
| **Event-Driven** | Communication par événements asynchrones |
| **Hexagonale / Clean** | Le métier au centre, indépendant de la technique |

📖 **Document de référence détaillé** : `architectures_reference.md`

---

## 4.1 Ce qu'il faut retenir

**Monolithe vs Microservices :**
- Monolithe = simple, adapté aux petites équipes
- Microservices = complexe, pour grandes organisations
- 💡 Un **monolithe bien structuré** > des microservices mal maîtrisés

**Architecture en couches :**
- Modèle classique, compris par tous
- ⚠️ Attention aux "couches passoires" qui n'apportent rien

**Architectures centrées domaine (Hexagonale, Clean…) :**
- Le métier ne dépend pas de la technique
- C'est ce qu'on étudiera en **CM2** et dans le projet

---

## 4.2 Comment choisir ?

La bonne architecture dépend du **contexte** :

| Critère | Question |
|---------|----------|
| Taille de l'équipe | Petite équipe → monolithe. Grande → peut-être microservices |
| Complexité métier | Logique simple → couches. Complexe → hexagonale |
| Durée de vie | Court terme → simple. Long terme → investir dans la structure |
| Besoin de tests | Fort → architectures avec inversion de dépendances |
| Scalabilité | Forte et différenciée → microservices |

👉 **Pas de solution universelle.** L'important est de **justifier** son choix.

---

## 📝 5. Mini-exercice (discussion)

Contexte : application de **gestion d'emprunts de livres** pour une médiathèque.  

Fonctionnalités :
- Gérer les utilisateurs et les livres
- Gérer les emprunts & retours
- Envoyer des rappels par email
- Générer quelques statistiques

**Questions :**
1. Quels **principes** sont importants ici ?
2. Comment isoleriez-vous l'envoi d'email du métier ?
3. Quelle architecture vous semble adaptée ?

🎯 Objectif : **appliquer les principes** vus aujourd'hui.

---

## 🎯 Récapitulatif du CM1

Vous devez maintenant :

✅ Comprendre **pourquoi** l'architecture est essentielle (encore plus avec l'IA)

✅ Maîtriser les **principes fondamentaux** :
- Cohésion, couplage, dépendances
- Séparation des responsabilités
- Inversion de dépendances

✅ Connaître les **grandes familles d'architectures** (cf. document de référence)

➡ **Prochain cours (CM2)** : Architecture hexagonale (Ports & Adapters) en détail.

---

# 🏁 Fin du CM1

📂 Les slides et le document de référence sont disponibles sur le dépôt GitHub.

📖 **À consulter** : `architectures_reference.md` — fiches détaillées sur chaque architecture.

❓ Questions ?
