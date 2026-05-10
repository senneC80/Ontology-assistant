# DPO Module Patterns Reference

This document describes the Digital Platform Ontology (DPO/DPO+) modules — reusable ontological
patterns for digital platform conceptualization using OntoUML. Each module captures a specific
dimension of platform design.

**How to use this reference:** When building a platform-specific ontology, you select modules matching
your platform's properties. For each selected module, you adapt the pattern: rename generic roles
to domain-specific ones (e.g., Provider → Trip Provider), add domain-specific attributes, and
introduce NEW classes for concepts unique to your platform that aren't in any DPO module.

**Reading the patterns:** Each module shows its Classes (with OntoUML stereotypes and attributes),
Relations (with cardinalities: source [card] --name--> target [card]), and Generalizations
(inheritance: specific --|> general). Stereotypes in «angle brackets» follow OntoUML semantics.

---
## General Digital Platform (always included)

### General: User Actions

> The foundational module for any digital platform. Defines the core actors (Person, Organization, Agent), the Platform Company that operates the platform, Platform Software that enables it, and the Service Offering that connects them. Introduces User Actions (things users do on the platform) and distinguishes Platform Supported Actions from Offline Actions. Also defines Target Platform User Communities and User Affiliation Agreements that bind users to the platform.

**Classes (22):**

- `«category»` **Agent**
- `«relator»` **Digital Platform
(Service Offering)**
- `«roleMixin»` **Hired Service Provider**
- `«event»` **Offline Action**
- `«kind»` **Organization** [name, location, description]
- `«kind»` **Person** [firstName, lastName, email, birthDate]
- `«roleMixin»` **Platform Company** [name]
- `«event»` **Platform Company Action**
- `«subkind»` **Platform Software**
- `«event»` **Platform Software Action**
- `«event»` **Platform Supported Action **
- `«relator»` **Service Agreement**
- `«roleMixin»` **Service Customer**
- `«relator»` **Service Offering**
- `«roleMixin»` **Service Provider**
- `«kind»` **Software**
- `«roleMixin»` **Target Customer**
- `«collective»` **Target Customer Communty**
- `«roleMixin»` **Target Platform User**
- `«collective»` **Target Platform User Community**
- `«event»` **User Action**
- `«relator»` **User Affiliation Agreement**

**Relations (14):**

- Digital Platform
(Service Offering) [1] --supported by «mediation»--> Platform Software [1]
- Digital Platform
(Service Offering) [1..*] --offered by «mediation»--> Platform Company [1]
- Platform Company Action [1] --performed «participation»--> Platform Company [0..*]
- User Affiliation Agreement [0..*] --bounds organization «mediation»--> Platform Company [1]
- Service Agreement [None] --(unnamed)--> Hired Service Provider [None]
- Target Platform User [1..*] --is part of «memberOf»--> Target Platform User Community [1..*]
- Target Customer [1..*] --is part of «memberOf»--> Target Customer Communty [1..*]
- Service Offering [None] --(unnamed)--> Service Agreement [None]
- Service Offering [1..*] --involves «mediation»--> Service Provider [1]
- Target Customer Communty [1] --involves «mediation»--> Service Offering [1..*]
- Digital Platform
(Service Offering) [1..*] --designed for «mediation»--> Target Platform User Community [1]
- User Affiliation Agreement [0..*] --conforms to «mediation»--> Digital Platform
(Service Offering) [1]
- Service Customer [None] --(unnamed)--> Service Agreement [None]
- Platform Supported Action  [1] --enables «participation»--> Platform Software [1..*]

**Generalizations (10):**

- Platform Software Action --|> Platform Supported Action 
- Organization --|> Agent
- User Action --|> Platform Supported Action 
- Person --|> Agent
- Target Platform User --|> Agent
- Platform Company Action --|> Platform Supported Action 
- Platform Company --|> Organization
- Platform Software --|> Software
- Service Customer --|> Target Customer
- Hired Service Provider --|> Service Provider

### General: User Roles

> Extends the user model with role-based access. Defines User Roles (types that the Platform Company defines), User Role Assignments (relators that assign a role to a specific user), and how Platform Visitors can initiate User Affiliation Actions. Establishes the pattern: Platform Company defines roles → users get assigned to roles → roles determine which actions they can perform.

**Classes (10):**

- `«roleMixin»` **Platform Company** [name]
- `«roleMixin»` **Platform Visitor**
- `«roleMixin»` **Target Platform User**
- `«event»` **User Action**
- `«type»` **User Action Type**
- `«event»` **User Affiliation Action**
- `«relator»` **User Affiliation Agreement**
- `«type»` **User Role**
- `«event»` **User Role Action**
- `«relator»` **User Role Assignment**

**Relations (10):**

- User Role Assignment [1..*] --(unnamed) «mediation»--> Platform Company [1]
- User Role [1] --is intentiated in  «instantiation»--> User Role Assignment [0..*]
- User Role [1..*] --can perform--> User Action Type [1..*]
- Platform Company [1] --defines--> User Role [1..*]
- User Role Assignment [1] --changes--> User Role Action [0..*]
- Platform Visitor [1] --can initiate «participation»--> User Affiliation Action [0..1]
- User Action [0..*] --(unnamed) «instantiation»--> User Action Type [1]
- User Affiliation Agreement [0..*] --bounds organization «mediation»--> Platform Company [1]
- User Affiliation Agreement [1] --is followed by--> User Affiliation Action [1..*]
- User Role Assignment [1] --creates--> User Affiliation Action [0..1]

**Generalizations (2):**

- Platform Visitor --|> Target Platform User
- User Role Action --|> User Action

### General: Interactions

> Defines how users interact with the platform and each other through digital content. Introduces Content Creators who produce Digital Content via Content Creation events, and Content Consumers who consume it via Content Consumption events. Also defines Platform Supported Communication and Interaction as higher-level interaction patterns.

**Classes (8):**

- `«historicalRoleMixin»` **Content Consumer**
- `«historicalRoleMixin»` **Content Creator**
- `«kind»` **Digital Content**
- `«event»` **Digital Content Consumption**
- `«event»` **Digital Content Creation**
- `«event»` **Platform Supported Communication**
- `«event»` **Platform Supported Interaction**
- `«event»` **User Action**

**Relations (7):**

- Platform Supported Communication [2..*] --is part of--> Platform Supported Interaction [0..*]
- Digital Content Consumption [1..*] --consumed «participation»--> Digital Content [0..*]
- Digital Content Consumption [1] --performed «participation»--> Content Consumer [1..*]
- Digital Content Consumption [1..*] --is part of--> Platform Supported Communication [1..*]
- Digital Content Creation [1] --performed «participation»--> Content Creator [1..*]
- Digital Content Creation [1..*] --is part of--> Platform Supported Communication [0..*]
- Digital Content Creation [1] --was created in «participation»--> Digital Content [1]

**Generalizations (2):**

- Digital Content Creation --|> User Action
- Digital Content Consumption --|> User Action

---
## Market Sides

### Multi-sided

> A Multi-Sided (MS) platform operates in a multi-sided market, enabling interactions between users of different sides. Users of each side are bound to the platform via a user affiliation agreement. This affiliation can be registration, subscription, transaction and/or investment. The module introduces Target MS Platform Customer Community and shows how different sides interact through the platform's service offering. The platform enables interactions between at least two sides of users.

**Classes (15):**

- `«relator»` **Digital Platform
(Service Offering)**
- `«subkind»` **Investment**
- `«event»` **MS Platform Supported Interaction**
- `«roleMixin»` **MS Platform User**
- `«collective»` **MS Platform User Side**
- `«subkind»` **MS User Affiliation**
- `«subkind»` **Multi-Sided Platform
(Hagiu and Wright 2015)** [market sides]
- `«roleMixin»` **Platform Company** [name]
- `«event»` **Platform Supported Interaction**
- `«subkind»` **Registration**
- `«collective»` **Target MS Platform User Side**
- `«collective»` **Target Platform User Community**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]
- `«relator»` **User Affiliation Agreement**
- `«type»` **User Role**

**Relations (11):**

- MS Platform Supported Interaction [0..*] --involves «participation»--> MS Platform User Side [2..*]
- MS Platform User Side [1..*] --is part of «subCollectionOf»--> Target MS Platform User Side [1..*]
- Digital Platform
(Service Offering) [1..*] --relates to «mediation»--> Platform Company [1]
- MS Platform User [1..*] --is part of «memberOf»--> MS Platform User Side [1..*]
- User Role [2..*] --defines user role--> Multi-Sided Platform
(Hagiu and Wright 2015) [1]
- Multi-Sided Platform
(Hagiu and Wright 2015) [1..*] --designed for «mediation»--> Target MS Platform User Side [2..*]
- Multi-Sided Platform
(Hagiu and Wright 2015) [1] --conforms to «mediation»--> User Affiliation Agreement [0..*]
- MS User Affiliation [1..*] --bounds user «mediation»--> MS Platform User [1..*]
- Digital Platform
(Service Offering) [1..*] --designed for «mediation»--> Target Platform User Community [1]
- User Affiliation Agreement [0..*] --bounds organization «mediation»--> Platform Company [1]
- Target MS Platform User Side [2..*] --is part of «subCollectionOf»--> Target Platform User Community [1]

**Generalizations (6):**

- Transaction --|> MS User Affiliation
- Multi-Sided Platform
(Hagiu and Wright 2015) --|> Digital Platform
(Service Offering)
- Investment --|> MS User Affiliation
- MS User Affiliation --|> User Affiliation Agreement
- MS Platform Supported Interaction --|> Platform Supported Interaction
- Registration --|> MS User Affiliation

### One-sided

> A one-sided platform is a digital platform towards one community of target users where users cannot be classified into types with different interests in the service offering. Our taxonomic structure only allows users to affiliate to a one-sided platform by registration. The module is simpler than Multi-sided: a single Target OS Platform User Community connected to the Service Offering.

**Classes (9):**

- `«relator»` **Digital Platform
(Service Offering)**
- `«subkind»` **One-Sided Platform**
- `«roleMixin»` **One-Sided Platform User**
- `«roleMixin»` **Platform Company** [name]
- `«subkind»` **Registration**
- `«collective»` **Target One-Sided User Community**
- `«roleMixin»` **Target Platform User**
- `«collective»` **Target Platform User Community**
- `«relator»` **User Affiliation Agreement**

**Relations (7):**

- Registration [1..*] --bounds user «mediation»--> One-Sided Platform User [1]
- One-Sided Platform [1] --conforms to «mediation»--> Registration [0..*]
- User Affiliation Agreement [0..*] --bounds organization «mediation»--> Platform Company [1]
- Target One-Sided User Community [1] --is part of «subCollectionOf»--> Target Platform User Community [1]
- Target Platform User [1..*] --is part of «memberOf»--> Target Platform User Community [1..*]
- One-Sided Platform [1..*] --made towards «mediation»--> Target One-Sided User Community [1]
- Digital Platform
(Service Offering) [1..*] --designed for «mediation»--> Target Platform User Community [1]

**Generalizations (2):**

- Registration --|> User Affiliation Agreement
- One-Sided Platform --|> Digital Platform
(Service Offering)

---
## User Affiliation

### Registration

> Registration is a way for a user to affiliate to the platform. During the registration action, the user submits personal data (email, password, name). The module defines Register as an event performed by a Platform Visitor, resulting in the user becoming a Logged In User with access to further actions like Login. The Signup creates a User Affiliation Agreement. Registration can be fully automated or require manual verification by the Platform Company.

**Classes (9):**

- `«roleMixin»` **Logged In User**
- `«event»` **Login** [checkEmail, checkPassword]
- `«subkind»` **Personal Data**
- `«roleMixin»` **Platform Visitor**
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]
- `«subkind»` **Registration**
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]
- `«event»` **User Affiliation Action**
- `«relator»` **User Affiliation Agreement**

**Relations (7):**

- Register [1..*] --performed by «participation»--> User [1]
- Logged In User [1] --participates--> Login [1]
- Registration [1..*] --bounds user «mediation»--> User [1]
- Platform Visitor [1] --can initiate «participation»--> User Affiliation Action [0..1]
- Register [1] --followed by--> Login [0..*]
- Register [1] --collects «participation»--> Personal Data [1..*]
- Register [1] --creates «creation»--> Registration [1]

**Generalizations (3):**

- Registration --|> User Affiliation Agreement
- Register --|> User Affiliation Action
- Logged In User --|> User

### Transaction

> A transaction is a way for users to affiliate to the platform. The module defines how Providers create Offerings described by Offering Descriptions, and how Customers initiate Transactions by accepting offerings. Key roles: Listing Creator (creates offerings), Provider (fulfills), Customer (purchases), Target Customer (browses). Transactions are bound by Service Agreements and create commitments between parties. The Transaction class is a central relator mediating between Customer and Provider.

**Classes (21):**

- `«historicalRoleMixin»` **Content Consumer**
- `«historicalRoleMixin»` **Content Creator**
- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«event»` **Delivery**
- `«kind»` **Digital Content**
- `«event»` **Digital Content Creation**
- `«roleMixin»` **Listing Creator**
- `«collective»` **MS Platform User Side**
- `«event»` **Offering Creation**
- `«subkind»` **Offering Description**
- `«relator»` **Offering On The Platform** [attribute]
- `«roleMixin»` **Platform Company** [name]
- `«event»` **Platform Supported Interaction**
- `«roleMixin»` **Provider**
- `«roleMixin»` **Target Customer**
- `«subkind»` **Target MS Platform Customer Community**
- `«collective»` **Target MS Platform User Side**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]
- `«roleMixin»` **Transaction Platform Company**
- `«relator»` **User Affiliation Agreement**

**Relations (19):**

- Transaction [0..*] --conforms to  «historicalDependence»--> Offering On The Platform [1..*]
- Offering On The Platform [1..*] --offered by «mediation»--> Listing Creator [1]
- Content Creator [1] --performs «participation»--> Digital Content Creation [1..*]
- Create Transaction [1] --creates «creation»--> Transaction [1]
- Offering Creation [1..*] --is performed by «participation»--> Listing Creator [1]
- Offering On The Platform [1] --described by «mediation»--> Offering Description [1]
- Offering Creation [1] --creates «creation»--> Offering Description [1]
- Delivery [0..*] --received by «participation»--> Customer [1..*]
- Transaction [1] --partially fulfills--> Delivery [0..*]
- Transaction [1..*] --is bound to «mediation»--> Transaction Platform Company [1]
- Target Customer [1..*] --is part of «memberOf»--> Target MS Platform Customer Community [1..*]
- Create Transaction [1..*] --accepted by «participation»--> Provider [1]
- Offering Creation [1] --created «creation»--> Offering On The Platform [1]
- Offering On The Platform [0..*] --mediated by «mediation»--> Transaction Platform Company [1]
- Transaction [1..*] --binds «mediation»--> Provider [1..*]
- Digital Content Creation [1] --was created in «participation»--> Digital Content [1]
- Customer [1..*] --is part of «memberOf»--> MS Platform User Side [1..*]
- Offering On The Platform [1..*] --offered to «mediation»--> Target MS Platform Customer Community [1]
- Listing Creator [1..*] --is part of «memberOf»--> MS Platform User Side [1..*]

**Generalizations (10):**

- Transaction Platform Company --|> Platform Company
- Create Transaction --|> Platform Supported Interaction
- Offering Creation --|> Digital Content Creation
- Transaction --|> User Affiliation Agreement
- Listing Creator --|> Content Creator
- Provider --|> Listing Creator
- Target MS Platform Customer Community --|> Target MS Platform User Side
- Customer --|> Content Consumer
- Customer --|> Target Customer
- Offering Description --|> Digital Content

### Investment

> An affiliation by investment follows the theory of two-sided markets with financial intermediation. The module introduces Capital Givers and Capital Seekers connected through Investment transactions, Resource Claims (what the investor gets) and Reimbursement Commitments (what the seeker promises). Extends the Transaction pattern for crowdfunding-type platforms.

**Classes (12):**

- `«roleMixin»` **Capital-Giving Agent**
- `«roleMixin»` **Capital-Seeking Agent**
- `«roleMixin»` **Customer**
- `«subkind»` **Future Reimbursement Commitment**
- `«quality»` **Hired Provider Commitment**
- `«subkind»` **Investment**
- `«roleMixin»` **Provider**
- `«category»` **Reimbursement**
- `«category»` **Resource**
- `«subkind»` **Resource Claim**
- `«quality»` **Service Customer Claim**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

**Relations (14):**

- Future Reimbursement Commitment [1..*] --is part of--> Investment [1]
- Capital-Seeking Agent [1] --depends on «externalDependence»--> Resource Claim [1..*]
- Capital-Giving Agent [1] --inheres in «characterization»--> Resource Claim [1..*]
- Future Reimbursement Commitment [1..*] --depends on «externalDependence»--> Capital-Giving Agent [1]
- Hired Provider Commitment [1] --is counter part of--> Service Customer Claim [1]
- Investment [1..*] --bounds investor «mediation»--> Capital-Giving Agent [1]
- Investment [1] --is part of--> Resource Claim [1..*]
- Transaction [1..*] --binds «mediation»--> Provider [1..*]
- Future Reimbursement Commitment [1..*] --inheres in «characterization»--> Capital-Seeking Agent [1]
- Transaction [1..*] --binds «mediation»--> Customer [1]
- Resource Claim [0..1] --bounds  to «mediation»--> Resource [1..*]
- Investment [1..*] --bounds investee «mediation»--> Capital-Seeking Agent [1]
- Reimbursement [1..*] --bounds to «mediation»--> Future Reimbursement Commitment [0..1]
- Transaction [1] --is part of «componentOf»--> Investment [0..1]

**Generalizations (4):**

- Capital-Seeking Agent --|> Provider
- Capital-Giving Agent --|> Customer
- Future Reimbursement Commitment --|> Hired Provider Commitment
- Resource Claim --|> Service Customer Claim

---
## Participation

### P2P

> A P2P (peer-to-peer) platform intermediates interaction between users as equal participants (prosumers) who can alternate between producer and consumer roles. Peer users can easily alternate as producer and consumer and thus perform the same actions. Peer users can automatically affiliate to the platform. The module defines Peer User as a role that can perform both provider-type and consumer-type actions, with near-zero cost affiliation.

**Classes (7):**

- `«event»` **Automated Affiliation Action**
- `«event»` **Peer Action**
- `«roleMixin»` **Peer Consumer**
- `«roleMixin»` **Peer Producer**
- `«roleMixin»` **Peer User**
- `«event»` **User Action**
- `«event»` **User Affiliation Action**

**Relations (2):**

- Automated Affiliation Action [1..*] --performed by «participation»--> Peer User [1]
- Peer User [1..*] --performed by «participation»--> Peer Action [0..*]

**Generalizations (4):**

- Automated Affiliation Action --|> User Affiliation Action
- Peer Action --|> User Action
- Peer Consumer --|> Peer User
- Peer Producer --|> Peer User

### C2C

> In a C2C (consumer-to-consumer) market, both the customer and the provider are persons (not organizations). The module adds Person-specific constraints: C2C Provider and C2C Customer both specialize Person, ensuring the platform connects individual people rather than businesses.

**Classes (8):**

- `«subkind»` **C2C Transaction**
- `«roleMixin»` **Customer**
- `«kind»` **Person** [firstName, lastName, email, birthDate]
- `«role»` **Person Platform Customer**
- `«role»` **Person Platform Provider**
- `«roleMixin»` **Provider**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

**Relations (2):**

- Person Platform Provider [1..*] --binds «mediation»--> C2C Transaction [1]
- C2C Transaction [1..*] --binds «mediation»--> Person Platform Customer [1]

**Generalizations (7):**

- Person Platform Provider --|> Person
- Person Platform Provider --|> Provider
- Person Platform Provider --|> User
- Person Platform Customer --|> User
- C2C Transaction --|> Transaction
- Person Platform Customer --|> Person
- Person Platform Customer --|> Customer

### Non-P2P

> The inverse of P2P: defines a Non-P2P platform where users have fixed, distinct roles (not interchangeable prosumers). Providers and Customers are separate groups with different action sets.

**Classes (6):**

- `«event»` **Manual Affiliation Check**
- `«event»` **Manually-Checked Affiliation Action**
- `«roleMixin»` **Non-Peer User**
- `«event»` **Platform Company Action**
- `«event»` **User Action**
- `«event»` **User Affiliation Action**

**Relations (2):**

- Manually-Checked Affiliation Action [1..*] --performed by «participation»--> Non-Peer User [1]
- Manual Affiliation Check [1..*] --is part of--> Manually-Checked Affiliation Action [1]

**Generalizations (3):**

- Manual Affiliation Check --|> Platform Company Action
- User Affiliation Action --|> User Action
- Manually-Checked Affiliation Action --|> User Affiliation Action

---
## Centralization

### Decentralized

> A decentralized digital platform offers a simple list-based solution as the basic matching mechanism. Platform customers can choose themselves with which other users to interact by performing a search through the content (Listings). The module introduces Listing (subkind, with attributes like name, description, picture, status), Listing Description, Listing Search (event), Listing Overview (collective), and the flow: Provider creates Listing via Add Listing event → Customer searches via Listing Search → Search results in Decentralized Transaction Creation.

**Classes (16):**

- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«roleMixin»` **Decentralized Platform Customer**
- `«roleMixin»` **Decentralized Target Platform Customer**
- `«collective»` **Decentralized Target Platform Customer Community**
- `«subkind»` **Decentralized Transaction**
- `«event»` **Decentralized Transaction Creation**
- `«event»` **Digital Content Consumption**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«subkind»` **Listing Description**
- `«collective»` **Listing Overview**
- `«event»` **Listing Search**
- `«subkind»` **Offering Description**
- `«relator»` **Offering On The Platform** [attribute]
- `«subkind»` **Target MS Platform Customer Community**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

**Relations (14):**

- Listing [1] --described by «mediation»--> Listing Description [1]
- Listing Search [1..*] --performed by «participation»--> Decentralized Target Platform Customer [1]
- Decentralized Transaction Creation [1] --performed by «mediation»--> Decentralized Platform Customer [1..*]
- Offering On The Platform [1] --described by «mediation»--> Offering Description [1]
- Offering On The Platform [1..*] --offered to «mediation»--> Target MS Platform Customer Community [1]
- Decentralized Target Platform Customer [1..*] --is part of «memberOf»--> Decentralized Target Platform Customer Community [1]
- Transaction [1..*] --binds «mediation»--> Customer [1]
- Listing Description [1..*] --is part of «memberOf»--> Listing Overview [1]
- Target MS Platform Customer Community [0..*] --is part of «subCollectionOf»--> Decentralized Target Platform Customer Community [1]
- Listing Search [1..*] --uses «participation»--> Listing Overview [1]
- Decentralized Transaction Creation [1] --results in «creation»--> Decentralized Transaction [1]
- Decentralized Transaction [0..*] --conforms to «historicalDependence»--> Listing [1]
- Listing Search [1..*] --results in «historicalDependence»--> Decentralized Transaction Creation [0..1]
- Create Transaction [1] --creates «creation»--> Transaction [1]

**Generalizations (7):**

- Listing Description --|> Offering Description
- Listing --|> Offering On The Platform
- Decentralized Transaction --|> Transaction
- Listing Search --|> Digital Content Consumption
- Decentralized Platform Customer --|> Decentralized Target Platform Customer
- Decentralized Platform Customer --|> Customer
- Decentralized Transaction Creation --|> Create Transaction

### Centralized

> A centralized digital platform offers matching based on optimization procedures of supply and demand. A customer doesn't need to scroll through a list but gets automatically matched. The module introduces Centralized Matching (event) performed by Platform Software, Customer Request, and Centralized Transaction Creation. The key difference from Decentralized: matching is done by the platform software, not by the customer browsing listings.

**Classes (13):**

- `«subkind»` **Centralized Offering**
- `«roleMixin»` **Centralized Platform Customer**
- `«roleMixin»` **Centralized Target Platform Customer**
- `«collective»` **Centralized Target Platform Customer Community**
- `«subkind»` **Centralized Transaction**
- `«event»` **Centralized Transaction Creation**
- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«event»` **Match Target Customer To Offering**
- `«relator»` **Offering On The Platform** [attribute]
- `«event»` **Platform Software Action**
- `«subkind»` **Target MS Platform Customer Community**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

**Relations (9):**

- Centralized Target Platform Customer [1..*] --is part of «memberOf»--> Centralized Target Platform Customer Community [1]
- Match Target Customer To Offering [1..*] --is part of--> Centralized Transaction Creation [1]
- Transaction [1..*] --binds «mediation»--> Customer [1]
- Centralized Target Platform Customer Community [0..*] --is part fo «subCollectionOf»--> Target MS Platform Customer Community [1]
- Centralized Transaction [1..*] --bounds customer «mediation»--> Centralized Platform Customer [1]
- Offering On The Platform [1..*] --offered to «mediation»--> Target MS Platform Customer Community [1]
- Centralized Offering [1..*] --towards--> Match Target Customer To Offering [0..*]
- Centralized Transaction Creation [1..*] --performs «participation»--> Centralized Platform Customer [1]
- Centralized Transaction Creation [1] --creates «creation»--> Centralized Transaction [1]

**Generalizations (6):**

- Centralized Transaction Creation --|> Create Transaction
- Centralized Transaction --|> Transaction
- Centralized Platform Customer --|> Centralized Target Platform Customer
- Centralized Platform Customer --|> Customer
- Centralized Offering --|> Offering On The Platform
- Match Target Customer To Offering --|> Platform Software Action

---
## Offering Orientation

### product, result and user oriented

> Defines the offering orientation spectrum. Product-oriented offerings involve delivery of a physical or digital product. Result-oriented offerings involve a service performed by a provider. User-oriented offerings combine both (e.g., product leasing, renting, sharing). The module introduces Product Delivery, Service Delivery, and the Delivery superclass, connecting them to the Transaction pattern.

**Classes (8):**

- `«roleMixin»` **Customer**
- `«event»` **Delivery**
- `«kind»` **Good**
- `«event»` **Product-Oriented Delivery**
- `«roleMixin»` **Provider**
- `«event»` **Result-Oriented Delivery**
- `«event»` **Service Delivery**
- `«event»` **User-Oriented Delivery**

**Relations (4):**

- Result-Oriented Delivery [1] --equal to «comparative»--> Service Delivery [1]
- Product-Oriented Delivery [0..*] --involves «participation»--> Good [1..*]
- Delivery [0..*] --received by «participation»--> Customer [1..*]
- Result-Oriented Delivery [1..*] --performed by «participation»--> Provider [1..*]

**Generalizations (4):**

- User-Oriented Delivery --|> Product-Oriented Delivery
- Result-Oriented Delivery --|> Delivery
- User-Oriented Delivery --|> Result-Oriented Delivery
- Product-Oriented Delivery --|> Delivery

---
## Special Dimensions

### Immediate access

> An immediate access-based platform relies on an immediate temporal pattern: minimal time between matching and delivery. After the transaction, a customer expects and claims immediate access to the service. The module introduces Immediate Access Transaction, Immediate Access Claim, and Immediate Access Provider commitment, specializing the general Transaction pattern for on-demand services like Uber or Bolt.

**Classes (10):**

- `«roleMixin»` **Customer**
- `«quality»` **Hired Provider Commitment**
- `«subkind»` **Immediate Acces Transaction**
- `«subkind»` **Immediate Access Claim**
- `«subkind»` **Immediate Access Commitment**
- `«roleMixin»` **Immediate Access Customer**
- `«roleMixin»` **Provider**
- `«quality»` **Service Customer Claim**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]
- `«roleMixin»` **immediate Access Provider**

**Relations (10):**

- Immediate Access Customer [1] --inheres in  «characterization»--> Immediate Access Claim [1..*]
- immediate Access Provider [1..*] --inheres in «characterization»--> Immediate Access Commitment [1..*]
- Immediate Access Claim [1..*] --is part of--> Immediate Acces Transaction [1]
- Transaction [1..*] --binds «mediation»--> Customer [1]
- Immediate Access Customer [1] --depends on «externalDependence»--> Immediate Access Commitment [1..*]
- Immediate Acces Transaction [1] --is part of--> Immediate Access Commitment [0..*]
- Immediate Access Claim [1..*] --depends on «externalDependence»--> immediate Access Provider [1..*]
- Immediate Acces Transaction [1..*] --binds «mediation»--> immediate Access Provider [1..*]
- Transaction [1..*] --binds «mediation»--> Provider [1..*]
- Immediate Acces Transaction [1..*] --binds «mediation»--> Immediate Access Customer [1]

**Generalizations (5):**

- Immediate Access Claim --|> Service Customer Claim
- Immediate Acces Transaction --|> Transaction
- immediate Access Provider --|> Provider
- Immediate Access Customer --|> Customer
- Immediate Access Commitment --|> Hired Provider Commitment

### Under-Utilized

> Under-utilization of products exists when there is excess capacity, giving the offering creator an opportunity to lend out or rent out their own goods. The product involved in the delivery is also personally used by the provider. The module introduces Physical Good, Under-Utilized Good (subkind), and the key relation: Provider 'uses' the same good that is being offered. This distinguishes sharing platforms (BlaBlaCar) from service platforms (Uber).

**Classes (7):**

- `«kind»` **Good**
- `«subkind»` **Physical Good**
- `«roleMixin»` **Provider**
- `«event»` **Under-Utilized Delivery**
- `«subkind»` **Under-Utilized Good**
- `«event»` **User-Oriented Delivery**
- `«event»` **Uses**

**Relations (5):**

- Uses [0..*] --performed by «participation»--> Provider [0..1]
- Uses [0..*] --includes «participation»--> Under-Utilized Good [0..*]
- User-Oriented Delivery [0..*] --performed by--> Provider [1..*]
- Under-Utilized Delivery [0..*] --during or between--> Uses [1..*]
- Good [1..*] --involves--> User-Oriented Delivery [0..*]

**Generalizations (3):**

- Under-Utilized Delivery --|> User-Oriented Delivery
- Physical Good --|> Good
- Under-Utilized Good --|> Physical Good

---
## Business Models — DPO+ Extensions

### User Type

> Specifies whether platform users are Persons, Organizations, or both. This dimension affects which UFO-C base classes are instantiated in the platform ontology.

**Classes (7):**

- `«relator»` **Member**
- `«kind»` **Organization** [name, location, description]
- `«kind»` **Person** [firstName, lastName, email, birthDate]
- `«roleMixin»` **Platform Company** [name]
- `«roleMixin»` **Professional User**
- `«event»` **Registers Organisation**
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

**Relations (5):**

- Member [1..*] --of a--> Organization [1]
- Member [1..*] --is a--> Professional User [1]
- Organization [0..*] --Recognized by «mediation»--> Platform Company [1..*]
- Professional User [1] --participates in--> Registers Organisation [0..*]
- Registers Organisation [1] --to create--> Organization [1]

**Generalizations (2):**

- Professional User --|> User
- User --|> Person

### Listing Kind

> Distinguishes what kind of resource is being listed: a Good (physical or digital product) or a Service. Affects the Listing and Delivery modules downstream.

**Classes (5):**

- `«subkind»` **Booking** [personsBooked]
- `«kind»` **Good**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«mode»` **Time**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

**Relations (4):**

- Listing [1] --involves--> Good [1..*]
- Transaction [0..*] --confirms to--> Listing [1]
- Transaction [0..1] --confirm the--> Good [1..*]
- Booking [0..*] --according--> Time [1]

**Generalizations (1):**

- Booking --|> Transaction

### Listing Type

> Further refines what the listing represents: Physical Good, Digital Good, Offline Service, or Digital Service. Determines the nature of the delivery and whether physical logistics are involved.

**Classes (16):**

- `«subkind»` **Booking** [personsBooked]
- `«roleMixin»` **Customer**
- `«mode»` **Delivery Location**
- `«subkind»` **Digital Good**
- `«event»` **Digital Good Transfer**
- `«event»` **Digital Good Upload**
- `«kind»` **Good**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«roleMixin»` **Listing Creator**
- `«mode»` **Listing Location**
- `«mode»` **Location** [latitude, longitude]
- `«mode»` **Meeting link**
- `«event»` **Physical Delivery**
- `«subkind»` **Physical Good**
- `«roleMixin»` **Provider**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

**Relations (17):**

- Listing Creator [1] --does--> Digital Good Upload [1..*]
- Physical Delivery [0..1] --(unnamed)--> Physical Good [1..*]
- Meeting link [1] --includes--> Booking [1]
- Transaction [0..1] --confirm the--> Good [1..*]
- Physical Delivery [0..*] --(unnamed)--> Provider [None]
- Physical Delivery [1..*] --(unnamed)--> Customer [1]
- Transaction [0..*] --confirms to--> Listing [1]
- Listing [1] --involves--> Good [1..*]
- Digital Good Transfer [0..1] --concerning--> Digital Good [1..*]
- Transaction [1..*] --binds «mediation»--> Provider [1..*]
- Transaction [1..*] --binds «mediation»--> Customer [1]
- Meeting link [0..*] --captures--> Listing [0..*]
- Delivery Location [0..*] --(unnamed)--> Physical Delivery [0..*]
- Listing [0..*] --captures--> Listing Location [1..*]
- Digital Good Transfer [1..*] --(unnamed)--> Customer [1]
- Digital Good Upload [1] --(unnamed)--> Digital Good [1]
- Provider [None] --(unnamed)--> Digital Good Transfer [1..*]

**Generalizations (6):**

- Delivery Location --|> Location
- Booking --|> Transaction
- Provider --|> Listing Creator
- Listing Location --|> Location
- Physical Good --|> Good
- Digital Good --|> Good

### Quantity

> Specifies whether a single transaction involves One unit or Many units of the offering (e.g., one room vs. multiple seats). Affects cardinality on the Transaction-to-Delivery relationship.

**Classes (4):**

- `«subkind»` **Available Quantity**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«mode»` **Quantity**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]

**Relations (3):**

- Transaction [0..*] --confirms to--> Listing [1]
- Transaction [1] --(unnamed)--> Quantity [1]
- Available Quantity [1] --of--> Listing [1]

### Price Discovery

> How the price is determined: Set by Provider (fixed price), Set by Customer (name-your-price), Set by Market (auction/bidding), or Quote-based. Each introduces different events and relations around price setting.

**Classes (9):**

- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«roleMixin»` **Listing Creator**
- `«quality»` **Price**
- `«event»` **Price Setting Action by Customer**
- `«event»` **Price Setting action by Provider** [setPricePerSeat]
- `«subkind»` **Price set by Provider**
- `«subkind»` **Suggested Price**
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

**Relations (9):**

- Listing Creator [1] --participates--> Add Listing [1..*]
- Listing [1..*] --(unnamed)--> Price set by Provider [1..*]
- Add Listing [1] --includes «participational»--> Price Setting action by Provider [1..*]
- Suggested Price [0..*] --(unnamed)--> Listing [1]
- User [1] --does--> Price Setting Action by Customer [0..*]
- Price Setting action by Provider [1] --sets--> Price set by Provider [1..*]
- Price Setting Action by Customer [1] --of--> Suggested Price [1]
- Listing Creator [1] --changes--> Price Setting action by Provider [0..*]
- Add Listing [1] --creates «creation»--> Listing [1]

**Generalizations (3):**

- Suggested Price --|> Price
- Listing Creator --|> User
- Price set by Provider --|> Price

### Price Calculation

> How the total price is calculated once the base price is known: By Quantity (price × units), By Feature (base + optional features), Auction (bidding process), or Quote (custom negotiation). Each pattern introduces specific price-related classes and events.

**Classes (23):**

- `«subkind»` **Accepted Quote**
- `«subkind»` **Accepted Quote Price**
- `«event»` **Accepts Quote**
- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«subkind»` **Available Quantity**
- `«event»` **Bid**
- `«subkind»` **Bid Price**
- `«roleMixin»` **Customer**
- `«mode»` **Feature**
- `«type»` **Feature Type**
- `«subkind»` **Feature-Based Price**
- `«subkind»` **Highest Bid Price**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«quality»` **Price**
- `«subkind»` **Price per Item**
- `«subkind»` **Price set by Provider**
- `«roleMixin»` **Provider**
- `«kind»` **Quote**
- `«None»` **Quote Price**
- `«relator»` **Quote Request**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]
- `«subkind»` **Transaction Price**
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

**Relations (27):**

- Price per Item [1] --for--> Available Quantity [1]
- Bid Price [0..*] --has--> Listing [1]
- Listing [0..*] --(unnamed)--> Quote Request [0..*]
- Transaction [1] --(unnamed)--> Highest Bid Price [1]
- Customer [1] --(unnamed)--> Accepts Quote [1..*]
- User [1] --does--> Bid [0..*]
- Bid Price [1] --(unnamed)--> Bid [1]
- Transaction Price [0..1] --(unnamed)--> Highest Bid Price [1]
- Transaction [0..*] --confirms to--> Listing [1]
- Listing [1..*] --(unnamed)--> Price set by Provider [1..*]
- Accepted Quote [1] --(unnamed)--> Accepts Quote [1]
- Transaction [1] --(unnamed)--> Transaction Price [1]
- Quote Price [None] --has--> Quote [None]
- Transaction [1..*] --binds «mediation»--> Provider [1..*]
- Feature [1] --has--> Transaction [0..*]
- Accepted Quote Price [1] --(unnamed)--> Accepted Quote [1]
- Feature Type [1] --instantiates--> Feature [0..*]
- Accepted Quote [1] --includes--> Transaction [1]
- Add Listing [1] --creates «creation»--> Listing [1]
- Provider [1] --submit--> Quote [1..*]
- Feature-Based Price [0..*] --(unnamed)--> Feature Type [1]
- Quote Request [1] --(unnamed) «creation»--> Quote [0..*]
- Price per Item [1] --used for--> Transaction Price [0..*]
- Available Quantity [1] --of--> Listing [1]
- Feature Type [0..*] --sets--> Add Listing [0..*]
- User [1] --does--> Quote Request [0..*]
- Transaction Price [0..*] --(unnamed)--> Feature-Based Price [1]

**Generalizations (8):**

- Bid Price --|> Price
- Customer --|> User
- Highest Bid Price --|> Bid Price
- Accepted Quote --|> Quote
- Transaction Price --|> Price
- Accepted Quote Price --|> Quote Price
- Price set by Provider --|> Price
- Feature-Based Price --|> Price set by Provider

### Frequency

> Whether the transaction is One-Time or Recurring. Recurring transactions introduce Subscription patterns with periodic billing and renewal events.

**Classes (8):**

- `«phase»` **Available time slot**
- `«phase»` **Booked Time Slot**
- `«subkind»` **Booking** [personsBooked]
- `«None»` **End Time**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«None»` **Start Time**
- `«mode»` **Time**
- `«quality»` **Time Slot**

**Relations (8):**

- Listing [1] --conforms to--> Booking [0..*]
- Booking [0..*] --according--> Time [1]
- Listing [0..*] --indicated--> Time [1]
- Start Time [1] --has--> Time Slot [0..*]
- Listing [1] --captures--> Available time slot [0..*]
- Booking [1] --captures--> Booked Time Slot [1..*]
- Available time slot [1] --becomes «historicalDependence»--> Booked Time Slot [0..1]
- End Time [1] --has--> Time Slot [0..*]

**Generalizations (4):**

- Start Time --|> Time
- Available time slot --|> Time Slot
- Booked Time Slot --|> Time Slot
- End Time --|> Time

### Payment

> Defines the payment system: Internal Payment (handled by the platform), External Payment (handled by third-party providers like Stripe/PayPal), or No Payment (free platform). Each introduces different Payment-related classes and events.

**Classes (16):**

- `«roleMixin»` **Customer**
- `«event»` **External Payment**
- `«event»` **In-house Payment**
- `«event»` **Offline Action**
- `«event»` **Offline Payment**
- `«kind»` **Organization** [name, location, description]
- `«subkind»` **Paid Transaction Price**
- `«event»` **Payment Action**
- `«subkind»` **Payment Provider**
- `«event»` **Platform Supported Action **
- `«quality»` **Price**
- `«roleMixin»` **Provider**
- `«subkind»` **Received Transaction Price**
- `«event»` **Transaction Payment**
- `«subkind»` **Transaction Price**
- `«event»` **User Action**

**Relations (7):**

- Customer [None] --(unnamed)--> Paid Transaction Price [None]
- Paid Transaction Price [1] --(unnamed)--> Transaction Payment [1]
- Customer [1] --by--> In-house Payment [0..*]
- Transaction Payment [0..*] --towards--> Provider [1]
- External Payment [1..*] --intermediates--> Payment Provider [1]
- Customer [1] --by--> Transaction Payment [0..*]
- Received Transaction Price [None] --(unnamed)--> Provider [None]

**Generalizations (12):**

- Paid Transaction Price --|> Transaction Price
- In-house Payment --|> User Action
- Offline Payment --|> Offline Action
- Transaction Payment --|> Payment Action
- Received Transaction Price --|> Transaction Price
- Transaction Price --|> Price
- Payment Provider --|> Organization
- Offline Payment --|> Transaction Payment
- Paid Transaction Price --|> Price
- External Payment --|> Transaction Payment
- In-house Payment --|> Transaction Payment
- Payment Action --|> Platform Supported Action 

### Revenue Stream

> How the platform makes money: Subscription (recurring fee), Commission (percentage of transaction), Fixed Fee (per-transaction flat fee), or Listing Fee (fee to list). Introduces Revenue Stream class and connects to specific fee structures.

**Classes (20):**

- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«subkind»` **Commission Fee**
- `«event»` **Create Transaction**
- `«subkind»` **Fixed Fee**
- `«roleMixin»` **Listing Creator**
- `«subkind»` **Listing Fee**
- `«event»` **Listing Fee Payment**
- `«roleMixin»` **Marketplace Company**
- `«subkind»` **Paid Transaction Price**
- `«event»` **Payment Action**
- `«roleMixin»` **Platform Company** [name]
- `«event»` **Register** [setPassword, setEmail, setFirstName, setLastName]
- `«mode»` **Revenue Stream**
- `«roleMixin»` **Subscribed Platform User**
- `«event»` **Subscription Action**
- `«subkind»` **Subscription Fee**
- `«event»` **Subscription Payment Plan**
- `«event»` **Transaction Payment**
- `«subkind»` **Transaction Price**
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]

**Relations (15):**

- Subscription Action [1..*] --performed by «participation»--> Subscribed Platform User [1]
- Commission Fee [None] --(unnamed)--> Create Transaction [None]
- Transaction Price [1] --adds--> Commission Fee [0..1]
- Listing Fee Payment [0..1] --includes--> Add Listing [1]
- Listing Fee [1] --includes--> Add Listing [1]
- Create Transaction [None] --(unnamed)--> Fixed Fee [None]
- Register [1..*] --performed by «participation»--> User [1]
- Subscription Action [0..1] --Followed by «historicalDependence»--> Register [1]
- Listing Creator [1] --participates--> Add Listing [1..*]
- Transaction Price [None] --(unnamed)--> Fixed Fee [None]
- Revenue Stream [0..*] --(unnamed)--> Marketplace Company [1]
- Listing Fee [None] --(unnamed)--> Listing Fee Payment [None]
- Subscription Fee [1..*] --of--> Subscription Payment Plan [1]
- Subscription Payment Plan [1] --includes «participational»--> Subscription Action [1]
- Paid Transaction Price [1] --(unnamed)--> Transaction Payment [1]

**Generalizations (11):**

- Paid Transaction Price --|> Transaction Price
- Marketplace Company --|> Platform Company
- Subscribed Platform User --|> User
- Listing Fee --|> Revenue Stream
- Transaction Payment --|> Payment Action
- Subscription Payment Plan --|> Payment Action
- Listing Creator --|> User
- Commission Fee --|> Revenue Stream
- Fixed Fee --|> Revenue Stream
- Subscription Fee --|> Revenue Stream
- Listing Fee Payment --|> Payment Action

### Revenue Source

> Who pays the platform: Customer, Provider, or both. Determines which side of the transaction bears the platform fee.

**Classes (5):**

- `«roleMixin»` **Customer**
- `«roleMixin»` **Provider**
- `«mode»` **Revenue Stream**
- `«subkind»` **Revenue Stream Payed by Customer**
- `«subkind»` **Revenue Stream Payed by Provider**

**Relations (2):**

- Provider [1] --by--> Revenue Stream Payed by Provider [0..*]
- Customer [1] --by--> Revenue Stream Payed by Customer [0..*]

**Generalizations (2):**

- Revenue Stream Payed by Provider --|> Revenue Stream
- Revenue Stream Payed by Customer --|> Revenue Stream

### Conversation System

> Defines messaging between users. Two patterns: Listing Conversation (messages about a listing before transaction) and Transaction Conversation (messages during/after a transaction). Both introduce Conversation (subkind), Send Message (event), and connect participants to specific roles.

**Classes (18):**

- `«event»` **Add Listing** [setName, setDescription, setPicture]
- `«event»` **Create Transaction**
- `«roleMixin»` **Customer**
- `«event»` **Digital Communication**
- `«event»` **Inter-User Conversation**
- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«event»` **Listing Conversation**
- `«roleMixin»` **Listing Creator**
- `«subkind»` **Listing Message**
- `«subkind»` **Message**
- `«kind»` **Notification** [notificationID, viewed, receiverID]
- `«event»` **Send Message**
- `«roleMixin»` **Target Customer**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]
- `«event»` **Transaction Conversation** [sendMessage]
- `«subkind»` **Transaction Message**
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]
- `«event»` **User Action**

**Relations (17):**

- Target Customer [1..*] --(unnamed)--> Inter-User Conversation [0..*]
- Transaction [1] --(unnamed)--> Transaction Message [0..*]
- Inter-User Conversation [0..*] --participates--> Listing Creator [1]
- Customer [1] --participates--> Transaction Conversation [1..*]
- Send Message [1..*] --(unnamed) «componentOf»--> Inter-User Conversation [1]
- Target Customer [1] --initiates--> Listing Conversation [0..*]
- Listing Creator [1] --participates--> Add Listing [1..*]
- Add Listing [1] --creates «creation»--> Listing [1]
- Create Transaction [1] --creates «creation»--> Transaction [1]
- Transaction [0..*] --confirms to--> Listing [1]
- Create Transaction [1..*] --initiates «participation»--> Customer [1]
- Listing Message [0..*] --(unnamed)--> Listing [1]
- Send Message [1] --(unnamed)--> Message [1]
- Transaction [1] --(unnamed)--> Transaction Conversation [0..*]
- Listing [1] --concerns--> Listing Conversation [0..*]
- User [None] --(unnamed)--> Message [0..*]
- Message [0..1] --(unnamed)--> Notification [1..*]

**Generalizations (9):**

- Inter-User Conversation --|> Digital Communication
- Customer --|> Target Customer
- Transaction Conversation --|> Inter-User Conversation
- Send Message --|> User Action
- Transaction Message --|> Message
- Listing Creator --|> User
- Listing Conversation --|> Inter-User Conversation
- Listing Message --|> Message
- Customer --|> User

### Review By

> Defines who can write reviews: Review by Customer (customer reviews provider), Review by Provider (provider reviews customer), or both. Introduces Review (relator), Review Creation (event), and score/comment attributes.

**Classes (10):**

- `«roleMixin»` **Customer**
- `«subkind»` **Customer Review**
- `«roleMixin»` **Provider**
- `«subkind»` **Provider Review**
- `«relator»` **Review** [score, comment]
- `«event»` **Review Creation** [setScore, givesComment]
- `«event»` **Review Creation by Customer**
- `«event»` **Review Creation by Provider**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]
- `«event»` **User Action**

**Relations (8):**

- Customer [1] --does--> Review Creation by Customer [0..*]
- Review Creation [1] --creates--> Review [1]
- Provider [1] --does--> Review Creation by Provider [0..*]
- Review [0..2] --concerning--> Transaction [1]
- Transaction [1..*] --binds «mediation»--> Customer [1]
- Transaction [1..*] --binds «mediation»--> Provider [1..*]
- Review Creation by Customer [1] --By--> Customer Review [1]
- Review Creation by Provider [1] --by--> Provider Review [1]

**Generalizations (5):**

- Customer Review --|> Review
- Review Creation by Provider --|> Review Creation
- Review Creation by Customer --|> Review Creation
- Provider Review --|> Review
- Review Creation --|> User Action

### Review Of

> Defines what gets reviewed: the Provider, the Customer, or the Listing/Offering itself. Complements the 'Review By' module.

**Classes (5):**

- `«subkind»` **Listing** [listingID, name, description, picture, status, providerID]
- `«roleMixin»` **Provider**
- `«relator»` **Review** [score, comment]
- `«subkind»` **Reviewed Listing** [numberOfReviews, averageScore]
- `«roleMixin»` **Reviewed Provider** [numberOfReviews, averageScore]

**Relations (2):**

- Review [1..*] --of--> Reviewed Provider [1]
- Review [1..*] --of--> Reviewed Listing [1]

**Generalizations (2):**

- Reviewed Listing --|> Listing
- Reviewed Provider --|> Provider

### Digital Good Transfer

> Specific module for platforms transferring digital goods (e-books, software, media). Introduces Digital Good and the transfer mechanism.

**Classes (6):**

- `«event»` **Delivery**
- `«subkind»` **Digital Good**
- `«event»` **Digital Good Transfer**
- `«event»` **Digital Good Upload**
- `«event»` **Offering Creation**
- `«event»` **Platform Software Action**

**Relations (1):**

- Digital Good Upload [0..*] --(unnamed)--> Offering Creation [None]

**Generalizations (1):**

- Digital Good Transfer --|> Platform Software Action

### Trust and Safety

> Introduces identity verification, trust mechanisms, and safety features. Defines Verified User, Identity Verification (event), Trust Score (quality), and Report/Flag mechanisms for content moderation.

**Classes (14):**

- `«event»` **Achievement**
- `«category»` **Badge**
- `«event»` **Files Claim**
- `«mode»` **Identity Document**
- `«relator»` **Insurance Policy**
- `«subkind»` **Insurer**
- `«mode»` **Payout**
- `«relator»` **Report** [status]
- `«roleMixin»` **ReportedUser**
- `«event»` **Review Process**
- `«subkind»` **Transaction** [transactionID, Status, listingID, buyerID]
- `«roleMixin»` **User** [userID, userName, UserID, authID, email]
- `«event»` **Verification Process**
- `«roleMixin»` **Verified User**

**Relations (16):**

- User [1] --does--> Review Process [0..*]
- Transaction [1] --is covered by--> Insurance Policy [0..*]
- Verified User [1] --provides--> Identity Document [1..*]
- User [1] --starts--> Transaction [0..*]
- ReportedUser [1] --targets--> Report [1..*]
- Files Claim [1] --results in--> Payout [0..*]
- Files Claim [0..*] --is based on--> Insurance Policy [1]
- Insurer [1] --is provided by--> Insurance Policy [1..*]
- User [1] --has--> Badge [0..*]
- User [1] --does--> Achievement [0..*]
- Achievement [1] --results in--> Badge [0..*]
- Review Process [1] --results in--> Report [1]
- Verified User [1] --does--> Verification Process [1]
- User [1] --submits--> Report [0..*]
- Verification Process [1] --is used in--> Identity Document [1]
- User [1] --does--> Files Claim [0..*]

**Generalizations (2):**

- ReportedUser --|> User
- Verified User --|> User
