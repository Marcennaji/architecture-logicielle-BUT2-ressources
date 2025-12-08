# 📚 Référence : Les grandes architectures logicielles

> **Document de référence** — À consulter quand vous rencontrez ces architectures en entreprise ou en stage.  
> Ce document complète le CM1 qui se concentre sur les **principes fondamentaux**.

---

## 🗺️ Vue d'ensemble

| Architecture | Idée principale | Quand l'utiliser |
|--------------|-----------------|------------------|
| Monolithique | Tout en un bloc | Petits projets, MVP, prototypes |
| N-tiers / Couches | Séparation par responsabilités horizontales | Applications classiques, équipes moyennes |
| MVC / MVVM | Séparation UI / logique / données | Interfaces utilisateur (web, mobile) |
| SOA | Services métier mutualisés | Grands SI d'entreprise |
| Microservices | Petits services autonomes | Grandes équipes, forte scalabilité |
| Event-Driven | Réaction à des événements | Systèmes asynchrones, découplage fort |
| Hexagonale / Clean | Le métier au centre, indépendant de la technique | Projets avec logique métier complexe |

---

## 1. Architecture monolithique

### Principe

```text
+-------------------------------------------+
|    UI + Logique métier + Accès données    |
|         (un seul bloc déployable)         |
+-------------------------------------------+
```

Tout le code de l'application est rassemblé dans **un seul artefact** déployable (un `.jar`, un `.war`, un binaire…).

### Avantages

- ✅ **Simple à démarrer** : pas de complexité réseau, pas d'orchestration
- ✅ **Déploiement facile** : un seul artefact à livrer
- ✅ **Debugging simple** : tout est dans le même processus
- ✅ **Performances** : pas de latence réseau entre composants

### Inconvénients

- ❌ **Scalabilité limitée** : on scale tout ou rien
- ❌ **Couplage risqué** : sans discipline, devient vite un "big ball of mud"
- ❌ **Déploiement tout-ou-rien** : une petite modif = redéployer toute l'appli
- ❌ **Équipes parallèles difficiles** : conflits fréquents sur le même code

### Quand l'utiliser ?

- Projet de petite/moyenne taille
- Équipe réduite (< 10 devs)
- MVP, prototype, proof of concept
- Domaine métier encore flou

### Quand l'éviter ?

- Application très grande avec besoins de scalabilité différenciés
- Plusieurs équipes autonomes travaillant en parallèle

### 💡 Point clé

> Un monolithe **bien structuré** (avec une bonne architecture interne) est souvent préférable à des microservices mal maîtrisés.

---

## 2. Architecture en couches (Layered / N-tiers)

### Principe

```text
┌─────────────────────────────────────┐
│         Couche Présentation         │  ← UI, API REST, pages web
├─────────────────────────────────────┤
│         Couche Métier / Service     │  ← Règles métier, orchestration
├─────────────────────────────────────┤
│         Couche Accès aux données    │  ← DAO, ORM, requêtes SQL
├─────────────────────────────────────┤
│         Base de données             │
└─────────────────────────────────────┘
```

Chaque couche a une **responsabilité** et ne communique qu'avec les couches adjacentes.

### Variantes

- **3-tiers** : Présentation → Métier → Données
- **4-tiers** : Présentation → Application → Domaine → Infrastructure
- **N-tiers** : autant de couches que nécessaire

### Avantages

- ✅ **Modèle universel** : compris par tous les développeurs
- ✅ **Séparation des responsabilités** : chaque couche a un rôle clair
- ✅ **Testabilité améliorée** : on peut mocker les couches inférieures
- ✅ **Réutilisation** : la couche métier peut servir plusieurs interfaces

### Inconvénients

- ❌ **Couches "passoires"** : si mal implémenté, les couches laissent tout passer
- ❌ **Couplage vertical** : un changement en base peut impacter toutes les couches
- ❌ **Rigidité** : les couches peuvent devenir des contraintes artificielles
- ❌ **Dépendances inversées** : le métier dépend souvent de la couche données (problème !)

### Quand l'utiliser ?

- Applications CRUD classiques
- Équipes habituées à ce modèle
- Projets sans logique métier très complexe

### 💡 Point clé

> L'architecture en couches est un **bon point de départ**, mais attention à l'évolution vers une "lasagne" où les couches ne servent plus à rien.

---

## 3. MVC (Model – View – Controller) / MVVM

### Principe MVC

```text
        ┌──────────┐
        │   View   │  ← Ce que voit l'utilisateur
        └────┬─────┘
             │ notifie
             ▼
        ┌──────────┐
        │Controller│  ← Reçoit les actions, orchestre
        └────┬─────┘
             │ manipule
             ▼
        ┌──────────┐
        │  Model   │  ← Données + logique métier locale
        └──────────┘
```

### Variante MVVM (Model – View – ViewModel)

Populaire en développement mobile et front-end moderne :
- **ViewModel** : expose les données du Model dans un format adapté à la View
- **Data binding** : la View se met à jour automatiquement quand le ViewModel change

### Avantages

- ✅ **Séparation claire** : affichage ≠ logique ≠ données
- ✅ **Réutilisation du Model** : même modèle pour web, mobile, API…
- ✅ **Testabilité** : on peut tester le Model sans l'interface
- ✅ **Standard de l'industrie** : frameworks web (Laravel, Django, Spring MVC…)

### Inconvénients

- ❌ **Ne structure pas tout** : MVC concerne l'interface, pas le back-end complet
- ❌ **Model obèse** : le Model finit souvent par tout faire
- ❌ **Confusion terminologique** : chaque framework a sa propre interprétation

### Quand l'utiliser ?

- Développement d'interfaces utilisateur (web, mobile, desktop)
- En complément d'une architecture plus globale (hexagonale, en couches…)

### 💡 Point clé

> MVC est un pattern d'**interface**, pas une architecture complète. On l'utilise **à l'intérieur** d'une architecture plus large.

---

## 4. SOA (Service-Oriented Architecture)

### Principe

```text
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│    Service      │   │    Service      │   │    Service      │
│   Facturation   │   │    Clients      │   │     Stock       │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         └──────────┬──────────┴──────────┬──────────┘
                    │                     │
              ┌─────▼─────────────────────▼─────┐
              │        ESB / Bus de services    │
              └─────────────────────────────────┘
```

Chaque **service** correspond à un grand domaine métier. Les services communiquent via un **bus** (ESB = Enterprise Service Bus).

### Caractéristiques

- Services **gros grain** (un service = un domaine métier entier)
- Communication via **contrats formels** (WSDL, SOAP, XML)
- Centralisation via un **ESB** qui orchestre les échanges
- Gouvernance forte (registre de services, versioning…)

### Avantages

- ✅ **Mutualisation** : un service peut être utilisé par plusieurs applications
- ✅ **Standardisation** : contrats clairs entre équipes
- ✅ **Adapté aux grands SI** : banques, assurances, administrations

### Inconvénients

- ❌ **Lourdeur** : mise en place complexe, outils coûteux
- ❌ **ESB = point de contention** : l'ESB devient un goulot d'étranglement
- ❌ **Couplage temporel** : les services dépendent souvent de la disponibilité des autres
- ❌ **Technos vieillissantes** : SOAP/WSDL moins populaires que REST/JSON

### Quand l'utiliser ?

- Grands systèmes d'information d'entreprise
- Besoin de mutualiser des services entre plusieurs applications
- Contexte avec gouvernance IT forte

### 💡 Point clé

> SOA est l'ancêtre des microservices. Vous le rencontrerez dans les **grands comptes** et les **SI historiques**.

---

## 5. Microservices

### Principe

```text
┌────────────┐       ┌────────────┐       ┌────────────┐
│ Service A  │ HTTP  │ Service B  │ HTTP  │ Service C  │
│  (Users)   │◄─────►│  (Orders)  │◄─────►│  (Stock)   │
└────────────┘       └────────────┘       └────────────┘
     │                     │                    │
     ▼                     ▼                    ▼
┌────────────┐       ┌────────────┐       ┌────────────┐
│   DB Users │       │  DB Orders │       │  DB Stock  │
└────────────┘       └────────────┘       └────────────┘
```

Chaque **microservice** est une petite application autonome :
- Son propre code
- Sa propre base de données
- Son propre déploiement
- Son propre cycle de vie

### Avantages

- ✅ **Déploiement indépendant** : on déploie un service sans toucher aux autres
- ✅ **Scalabilité fine** : on scale uniquement les services qui en ont besoin
- ✅ **Autonomie des équipes** : chaque équipe "possède" ses services
- ✅ **Liberté technologique** : chaque service peut utiliser des technos différentes
- ✅ **Résilience** : un service en panne n'affecte pas (théoriquement) les autres

### Inconvénients

- ❌ **Complexité opérationnelle** : monitoring, logs, tracing distribué
- ❌ **Réseau** : latence, pannes réseau, gestion des timeouts
- ❌ **Transactions distribuées** : pas de transaction ACID entre services
- ❌ **Cohérence des données** : eventual consistency, difficile à gérer
- ❌ **Overhead** : beaucoup d'infrastructure (Kubernetes, service mesh…)

### Quand l'utiliser ?

- ✅ Application très grande avec des domaines bien identifiés
- ✅ Équipes nombreuses (plusieurs dizaines de développeurs)
- ✅ Besoins de scalabilité différenciés selon les fonctionnalités
- ✅ Organisation capable de gérer la complexité infra (DevOps mature)

### Quand l'éviter ?

- ❌ Petite équipe (< 10 personnes)
- ❌ Domaine métier pas encore stabilisé
- ❌ Pas de compétences DevOps / infra
- ❌ Projet étudiant ou PME sans moyens

### 💡 Point clé

> **"Don't start with microservices"** — Commencez par un monolithe bien structuré, puis extrayez des microservices si/quand le besoin se fait sentir.

---

## 6. Event-Driven Architecture (EDA)

### Principe

```text
┌──────────────┐                              ┌──────────────┐
│  Service A   │──── publie un événement ────►│  Message     │
│ (Commandes)  │                              │    Broker    │
└──────────────┘                              │  (Kafka,     │
                                              │  RabbitMQ…)  │
┌──────────────┐                              │              │
│  Service B   │◄─── consomme l'événement ────│              │
│ (Facturation)│                              └──────────────┘
└──────────────┘
         ▲
         │
┌──────────────┐
│  Service C   │◄─── consomme aussi
│   (Stock)    │
└──────────────┘
```

Les services communiquent via des **événements** plutôt que des appels directs.

### Types d'événements

- **Événements métier** : "Commande créée", "Paiement validé", "Stock épuisé"
- **Événements techniques** : "Utilisateur connecté", "Fichier uploadé"

### Patterns associés

- **Event Sourcing** : l'état est reconstruit à partir de l'historique des événements
- **CQRS** : séparation des lectures (Query) et écritures (Command)
- **Saga** : orchestration de transactions distribuées via événements

### Avantages

- ✅ **Découplage fort** : les producteurs ne connaissent pas les consommateurs
- ✅ **Scalabilité** : les événements peuvent être traités en parallèle
- ✅ **Asynchrone** : pas d'attente de réponse
- ✅ **Extensibilité** : ajouter un nouveau consommateur sans modifier le producteur
- ✅ **Audit trail** : historique naturel des événements

### Inconvénients

- ❌ **Complexité cognitive** : difficile de suivre le flux d'exécution
- ❌ **Debugging difficile** : les erreurs peuvent se propager de façon non évidente
- ❌ **Consistance éventuelle** : les données ne sont pas immédiatement cohérentes
- ❌ **Ordre des événements** : peut être difficile à garantir

### Quand l'utiliser ?

- Systèmes nécessitant un découplage fort
- Intégration de systèmes hétérogènes
- Besoins de scalabilité et de résilience
- Cas d'usage asynchrones naturels (notifications, analytics…)

### 💡 Point clé

> L'EDA est souvent **combinée** avec d'autres architectures (microservices + events, hexagonale + events…).

---

## 7. Architectures centrées domaine (Hexagonale / Clean / Onion)

### Principe commun

> **Le code métier (domaine) est au centre et ne dépend de rien d'externe.**  
> C'est la technique (framework, base de données, UI) qui dépend du domaine.

### Architecture Hexagonale (Ports & Adapters)

```text
                    Adaptateur REST
                         │
                         ▼
              ┌─────────────────────┐
              │     Port Entrant    │
              │    (Interface)      │
              └──────────┬──────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │                                │
        │      DOMAINE MÉTIER            │
        │   (Entités, Règles métier,     │
        │    Services de domaine)        │
        │                                │
        └────────────────┬───────────────┘
                         │
              ┌──────────▼──────────┐
              │     Port Sortant    │
              │    (Interface)      │
              └──────────┬──────────┘
                         │
                         ▼
                  Adaptateur SQL
```

- **Ports** : interfaces définies par le domaine
- **Adaptateurs** : implémentations concrètes (REST, SQL, fichiers…)

### Clean Architecture (Uncle Bob)

```text
        ┌─────────────────────────────────────┐
        │  Frameworks & Drivers (externe)     │
        │  ┌─────────────────────────────┐    │
        │  │  Interface Adapters         │    │
        │  │  ┌─────────────────────┐    │    │
        │  │  │  Application        │    │    │
        │  │  │  ┌─────────────┐    │    │    │
        │  │  │  │  Entities   │    │    │    │
        │  │  │  │  (Domain)   │    │    │    │
        │  │  │  └─────────────┘    │    │    │
        │  │  └─────────────────────┘    │    │
        │  └─────────────────────────────┘    │
        └─────────────────────────────────────┘
```

Les dépendances pointent **vers l'intérieur** (vers le domaine).

### Avantages

- ✅ **Testabilité maximale** : le domaine se teste sans infrastructure
- ✅ **Indépendance technique** : changer de framework ou de DB sans toucher au métier
- ✅ **Clarté du code métier** : les règles métier sont isolées et lisibles
- ✅ **Longévité** : le cœur de l'application survit aux changements technologiques

### Inconvénients

- ❌ **Courbe d'apprentissage** : concepts à maîtriser (ports, adapters, use cases…)
- ❌ **Verbosité** : plus de fichiers, plus d'interfaces
- ❌ **Overhead pour projets simples** : trop complexe pour un simple CRUD

### Quand l'utiliser ?

- Logique métier complexe et évolutive
- Projet de longue durée (plusieurs années)
- Besoin de tester le métier en isolation
- Équipe prête à investir dans la structure

### 💡 Point clé

> C'est l'architecture que vous étudierez en détail dans le **CM2** et que vous mettrez en œuvre dans le **projet fil rouge**.

---

## 🎯 Tableau récapitulatif : comment choisir ?

| Critère | Monolithe | N-tiers | Microservices | Hexagonale |
|---------|-----------|---------|---------------|------------|
| Taille d'équipe | Petite | Moyenne | Grande | Toute |
| Complexité métier | Faible | Moyenne | Variable | Forte |
| Besoin de tests | Basique | Moyen | Fort | Très fort |
| Scalabilité | Limitée | Moyenne | Forte | Dépend infra |
| Courbe apprentissage | Faible | Faible | Forte | Moyenne |

---

## 📖 Pour aller plus loin

- **Clean Architecture** — Robert C. Martin (Uncle Bob)
- **Domain-Driven Design** — Eric Evans
- **Building Microservices** — Sam Newman
- **Patterns of Enterprise Application Architecture** — Martin Fowler

---

> 💡 **Rappel** : Ces architectures ne sont pas mutuellement exclusives.  
> On peut avoir un **monolithe** structuré en **hexagonal**, ou des **microservices** communiquant via **events**.  
> L'important est de comprendre les **principes** pour faire des choix éclairés.
