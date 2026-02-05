# Annexe 04 - Les Principes SOLID

> **Objectif** : Comprendre les 5 principes fondamentaux de la conception logicielle pour écrire du code maintenable, testable et évolutif.

## 📖 Introduction

**SOLID** est un acronyme qui représente 5 principes de conception logicielle, popularisés par Robert C. Martin (Uncle Bob). Bien qu'initialement formulés dans un contexte orienté objet, ces principes s'appliquent plus largement à toute conception logicielle (modules, fonctions, composants).

Ces principes aident à créer du code :
- **Maintenable** : Facile à modifier sans tout casser
- **Testable** : Facile à isoler et à tester
- **Compréhensible** : Chaque élément a un rôle clair
- **Évolutif** : Facile d'ajouter de nouvelles fonctionnalités

Les 5 principes sont :
- **S** - Single Responsibility Principle (SRP)
- **O** - Open/Closed Principle (OCP)
- **L** - Liskov Substitution Principle (LSP)
- **I** - Interface Segregation Principle (ISP)
- **D** - Dependency Inversion Principle (DIP)

---

## 🎯 S - Single Responsibility Principle (SRP)

### Définition

> Une classe ne devrait avoir qu'**une seule raison de changer**.

Autrement dit : **Une classe = Une responsabilité**.

### Pourquoi c'est important ?

- **Maintenabilité** : Si une classe fait plusieurs choses, modifier l'une peut casser les autres
- **Testabilité** : Tester une classe qui fait tout est complexe (beaucoup de dépendances)
- **Réutilisabilité** : Une classe focalisée peut être réutilisée ailleurs facilement

### ❌ Violation du SRP

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_database(self):
        """Sauvegarde en base de données."""
        # Code SQL ici...
    
    def send_welcome_email(self):
        """Envoie un email de bienvenue."""
        # Code SMTP ici...
    
    def generate_report(self):
        """Génère un rapport PDF."""
        # Code de génération PDF...
```

**Problèmes** :
- La classe `User` a **4 responsabilités** : représentation, persistance, email, rapports
- Si le format de la base change → modifier `User`
- Si le serveur SMTP change → modifier `User`
- Si le format PDF change → modifier `User`
- Impossible de tester la logique métier sans DB/Email/PDF

### ✅ Respect du SRP

```python
# Responsabilité 1 : Représenter un utilisateur (entité métier)
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Responsabilité 2 : Persistance
class UserRepository:
    def save(self, user):
        # Code SQL ici...

# Responsabilité 3 : Notifications
class EmailService:
    def send_welcome_email(self, user):
        # Code SMTP ici...

# Responsabilité 4 : Génération de rapports
class ReportGenerator:
    def generate_user_report(self, user):
        # Code PDF ici...
```

**Avantages** :
- Chaque classe a **une seule raison de changer**
- `User` peut être testé sans DB/Email/PDF
- On peut changer de DB sans toucher aux emails
- Réutilisable : `EmailService` peut envoyer d'autres types d'emails

---

## 🔓 O - Open/Closed Principle (OCP)

### Définition

> Une classe devrait être **ouverte à l'extension** mais **fermée à la modification**.

Autrement dit : On peut **ajouter** de nouveaux comportements sans **modifier** le code existant.

### Pourquoi c'est important ?

- **Stabilité** : Le code existant (testé, en production) n'est pas modifié → pas de régression
- **Évolutivité** : Ajout de fonctionnalités sans risque
- **Séparation des préoccupations** : Chaque comportement dans sa propre classe

### ❌ Violation de l'OCP

```python
class DiscountCalculator:
    def calculate(self, customer_type, amount):
        if customer_type == "regular":
            return amount * 0.95  # 5% de réduction
        elif customer_type == "premium":
            return amount * 0.90  # 10% de réduction
        elif customer_type == "vip":
            return amount * 0.80  # 20% de réduction
        else:
            return amount
```

**Problèmes** :
- Pour ajouter un nouveau type de client → **modifier** `DiscountCalculator`
- Chaque ajout = risque de casser les cas existants
- Tests à relancer pour tout à chaque fois

### ✅ Respect de l'OCP

```python
# Abstraction (port)
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount):
        pass

# Extension 1
class RegularDiscount(DiscountStrategy):
    def calculate(self, amount):
        return amount * 0.95

# Extension 2
class PremiumDiscount(DiscountStrategy):
    def calculate(self, amount):
        return amount * 0.90

# Extension 3 (ajoutée SANS modifier le code existant)
class VIPDiscount(DiscountStrategy):
    def calculate(self, amount):
        return amount * 0.80

# Utilisation
class DiscountCalculator:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy
    
    def calculate(self, amount):
        return self.strategy.calculate(amount)
```

**Avantages** :
- Ajouter un nouveau type de réduction = créer une nouvelle classe (pas de modification)
- Code existant **stable** et **non touché**
- Facile de tester chaque stratégie isolément

---

## 🔄 L - Liskov Substitution Principle (LSP)

### Définition

> Les objets d'une classe dérivée doivent pouvoir **remplacer** les objets de la classe parente **sans altérer le comportement du programme**.

Autrement dit : Si B hérite de A, on doit pouvoir utiliser B partout où on utilise A.

### Pourquoi c'est important ?

- **Polymorphisme correct** : L'héritage fonctionne comme prévu
- **Pas de surprises** : Le comportement reste cohérent
- **Contrats respectés** : Les sous-classes honorent les promesses de la classe parente

### ❌ Violation du LSP

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
    
    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def set_width(self, width):
        self.width = width
        self.height = width  # Force hauteur = largeur
    
    def set_height(self, height):
        self.width = height  # Force largeur = hauteur
        self.height = height

# Test
def test_rectangle(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20  # Attendu : 5 * 4 = 20

rect = Rectangle(0, 0)
test_rectangle(rect)  # ✅ OK : area = 20

square = Square(0, 0)
test_rectangle(square)  # ❌ FAIL : area = 16 (4 * 4), pas 20 !
```

**Problème** : `Square` ne peut **pas** remplacer `Rectangle` → violation du LSP.

### ✅ Respect du LSP

```python
# Abstraction commune
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

# Rectangle : hauteur et largeur indépendantes
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

# Carré : un seul paramètre (côté)
class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side * self.side

# Utilisation polymorphique
def print_area(shape: Shape):
    print(f"Area: {shape.area()}")

print_area(Rectangle(5, 4))  # ✅ Area: 20
print_area(Square(4))         # ✅ Area: 16
```

**Avantages** :
- Pas d'héritage artificiel (`Square` n'hérite plus de `Rectangle`)
- Chaque classe a son **propre contrat** cohérent
- Pas de surprises lors de la substitution

---

## 🧩 I - Interface Segregation Principle (ISP)

### Définition

> Un client ne devrait pas dépendre de méthodes qu'il n'utilise pas.

Autrement dit : **Interfaces petites et spécialisées** plutôt qu'une grosse interface universelle.

### Pourquoi c'est important ?

- **Couplage réduit** : Les clients ne dépendent que de ce dont ils ont besoin
- **Flexibilité** : Facile d'implémenter seulement une partie des fonctionnalités
- **Testabilité** : Moins de méthodes à mocker

### ❌ Violation de l'ISP

```python
class Printer(ABC):
    @abstractmethod
    def print(self, document):
        pass
    
    @abstractmethod
    def scan(self, document):
        pass
    
    @abstractmethod
    def fax(self, document):
        pass

# Imprimante simple : n'a pas de scanner ni de fax
class SimplePrinter(Printer):
    def print(self, document):
        print(f"Printing: {document}")
    
    def scan(self, document):
        raise NotImplementedError("Cette imprimante ne peut pas scanner")
    
    def fax(self, document):
        raise NotImplementedError("Cette imprimante ne peut pas faxer")
```

**Problèmes** :
- `SimplePrinter` doit implémenter des méthodes qu'elle n'utilise pas
- Violation du contrat : les méthodes lèvent des exceptions
- Tout client de `Printer` pense pouvoir scanner/faxer

### ✅ Respect de l'ISP

```python
# Interfaces ségrégées (petites et spécialisées)
class Printable(ABC):
    @abstractmethod
    def print(self, document):
        pass

class Scannable(ABC):
    @abstractmethod
    def scan(self, document):
        pass

class Faxable(ABC):
    @abstractmethod
    def fax(self, document):
        pass

# Imprimante simple : implémente uniquement Printable
class SimplePrinter(Printable):
    def print(self, document):
        print(f"Printing: {document}")

# Imprimante multifonction : implémente plusieurs interfaces
class MultiFunctionPrinter(Printable, Scannable, Faxable):
    def print(self, document):
        print(f"Printing: {document}")
    
    def scan(self, document):
        print(f"Scanning: {document}")
    
    def fax(self, document):
        print(f"Faxing: {document}")

# Utilisation
def send_document(printer: Printable, doc):
    printer.print(doc)  # Fonctionne avec n'importe quelle imprimante

def digitize_document(scanner: Scannable, doc):
    return scanner.scan(doc)  # Uniquement pour les scanners
```

**Avantages** :
- Chaque interface est **focalisée**
- Les clients dépendent **uniquement** de ce dont ils ont besoin
- Pas de méthodes "stub" qui lèvent des exceptions

---

## 🔀 D - Dependency Inversion Principle (DIP)

### Définition

> 1. Les modules de haut niveau ne doivent pas dépendre des modules de bas niveau. Les deux doivent dépendre d'**abstractions**.
> 2. Les abstractions ne doivent pas dépendre des détails. Les détails doivent dépendre des **abstractions**.

Autrement dit : **Dépendre d'interfaces, pas d'implémentations concrètes**.

### Pourquoi c'est important ?

- **Découplage** : Les modules sont indépendants
- **Testabilité** : On peut injecter des mocks/stubs
- **Flexibilité** : Facile de changer d'implémentation (DB, API, etc.)

### ❌ Violation du DIP

```python
# Module de bas niveau (détail d'implémentation)
class MySQLDatabase:
    def save(self, data):
        print(f"Saving to MySQL: {data}")

# Module de haut niveau (logique métier)
class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # ❌ Dépendance directe vers MySQL
    
    def register_user(self, user):
        # Logique métier...
        self.db.save(user)
```

**Problèmes** :
- `UserService` **dépend directement** de `MySQLDatabase`
- Impossible de tester `UserService` sans MySQL
- Impossible de changer de DB (PostgreSQL, MongoDB) sans modifier `UserService`
- Couplage fort entre logique métier et infrastructure

### ✅ Respect du DIP

```python
# Abstraction (port)
class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

# Détail d'implémentation 1 (adapter)
class MySQLDatabase(Database):
    def save(self, data):
        print(f"Saving to MySQL: {data}")

# Détail d'implémentation 2 (adapter)
class PostgreSQLDatabase(Database):
    def save(self, data):
        print(f"Saving to PostgreSQL: {data}")

# Détail d'implémentation 3 (test double)
class InMemoryDatabase(Database):
    def __init__(self):
        self.data = []
    
    def save(self, data):
        self.data.append(data)

# Module de haut niveau (logique métier)
class UserService:
    def __init__(self, db: Database):  # ✅ Dépend de l'abstraction
        self.db = db
    
    def register_user(self, user):
        # Logique métier...
        self.db.save(user)

# Composition root (main.py)
# Production
db = MySQLDatabase()
service = UserService(db)

# Tests
db_test = InMemoryDatabase()
service_test = UserService(db_test)
```

**Avantages** :
- `UserService` ne connaît **pas** l'implémentation concrète de la DB
- Facile de changer de DB (injection de dépendance)
- Testable avec `InMemoryDatabase` (pas besoin de vraie DB)
- Respect de l'architecture hexagonale : logique métier isolée

---

## 🎯 SOLID et Architecture Hexagonale

Les principes SOLID sont **fondamentaux** pour réussir une architecture hexagonale :

| Principe | Rôle dans l'architecture hexagonale |
|----------|-------------------------------------|
| **SRP** | Chaque use case = une responsabilité. Séparation domain/adapters |
| **OCP** | Ajouter de nouveaux adapters sans modifier le domain |
| **LSP** | Les adapters respectent le contrat des ports |
| **ISP** | Ports focalisés (pas de "god interface") |
| **DIP** | Domain dépend des ports (abstractions), pas des adapters (implémentations) |

### Exemple : Architecture Hexagonale + SOLID

```
src/
├── domain/              # SRP : Logique métier pure
│   ├── book.py          # Entité (SRP)
│   └── loan.py          # Entité (SRP)
├── ports/               # ISP + DIP : Abstractions
│   ├── book_repository.py   # Interface (ISP)
│   └── clock.py             # Interface (ISP)
├── application/
│   └── usecases/        # SRP : Un use case = une classe
│       └── borrow_book.py   # DIP : Dépend des ports
└── adapters/            # OCP : Ajout de nouveaux adapters sans modification
    ├── book_repository_sqlite.py    # LSP : Respecte le contrat du port
    ├── book_repository_in_memory.py # LSP : Respecte le contrat du port
    └── system_clock.py              # LSP : Respecte le contrat du port
```

**Résultat** :
- **Testable** : Injection de test doubles (DIP)
- **Maintenable** : Chaque classe a une responsabilité (SRP)
- **Évolutif** : Nouveaux adapters sans modification (OCP)
- **Compréhensible** : Séparation claire des couches

---

## 📚 Ressources complémentaires

- **Livre de référence** : *Clean Architecture* - Robert C. Martin
- **Article fondateur** : [The SOLID Principles](https://en.wikipedia.org/wiki/SOLID) - Wikipedia

---

## 💡 En résumé

| Principe | Question clé | Réponse |
|----------|--------------|---------|
| **SRP** | Combien de responsabilités ? | **Une seule** |
| **OCP** | Modifier ou étendre ? | **Étendre** (sans modifier) |
| **LSP** | Peut-on substituer ? | **Oui** (sans casser le comportement) |
| **ISP** | Interface trop grosse ? | **Ségréguer** (petites interfaces) |
| **DIP** | Dépendre de quoi ? | **Abstractions** (pas de détails) |

**La règle d'or** : Si votre code respecte SOLID, il sera plus facile à **tester**, **maintenir** et **faire évoluer**.
