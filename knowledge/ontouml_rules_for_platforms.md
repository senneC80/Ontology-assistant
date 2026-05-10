# OntoUML Rules and Constraints for Digital Platform Ontologies

This document covers the structural constraints, common patterns, and frequent mistakes
when building OntoUML ontologies for digital platforms using the DPO (Digital Platform Ontology).
It complements the OntoUML Stereotypes reference with practical rules.

## Core Structural Constraints

### Identity Provider Rule
Every sortal class (role, subkind, phase) must ultimately trace its identity to exactly one
identity-providing class (kind, collective, quantity, or relator). This means:

- Every `«role»` must specialize (directly or transitively) a `«kind»`, `«subkind»`, or `«category»`
- Every `«subkind»` must specialize a `«kind»` (or another `«subkind»` that traces to a `«kind»`)
- Every `«roleMixin»` must specialize a `«kind»`, `«category»`, or `«mixin»`

In the DPO, this is often satisfied through the UFO-C foundation:
- User roles (Trip Provider, Airbnb Host, etc.) trace back to Person or Organization (both `«kind»`)
- Platform-specific subkinds (Listing, Booking, Transaction) trace to identity providers in the DPO base

**Common mistake:** Creating a `«role»` or `«roleMixin»` without any generalization to an identity provider. Every role needs an ancestor that is a `«kind»`.

### Relator Mediation Rule
Every `«relator»` must mediate at least two distinct classes via `«mediation»` relations.
A relator that mediates only one class (or none) is structurally invalid.

In platform ontologies, common relators include:
- Booking/Transaction: mediates Customer and Provider
- Review: mediates the reviewer and the reviewed entity (via the Transaction)
- User Affiliation Agreement: mediates User and Platform Company

**Common mistake:** Creating a `«relator»` connected only via generic relations instead of explicit `«mediation»` stereotyped relations.

### Non-Sortal Purity Rule
Non-sortals (`«category»`, `«mixin»`, `«roleMixin»`, `«phaseMixin»`) must NOT specialize sortals
(`«kind»`, `«subkind»`, `«role»`, `«phase»`, `«relator»`, `«collective»`, `«quantity»`).

The direction must always be: sortals specialize non-sortals, not the reverse.

**Common mistake:** Making a `«roleMixin»` a subtype of a `«kind»`. If Customer is a `«roleMixin»` and Person is a `«kind»`, then Customer should NOT specialize Person. Instead, a `«role»` like PersonCustomer should specialize both.

### Rigidity Constraint
Rigid types (`«kind»`, `«subkind»`, `«category»`) cannot specialize anti-rigid types
(`«role»`, `«phase»`, `«roleMixin»`, `«phaseMixin»`).

If something is necessarily of a type, it can't be a subtype of something that is only contingently true.

### No Generalization Cycles
The generalization hierarchy must be acyclic. A class cannot be both an ancestor and descendant of another class.

### No Orphan Classes
Every class should be connected to at least one relation or generalization. Disconnected "island" classes indicate missing structural connections.

## STRUCTURAL RELATION CONSTRAINTS (from OntoUML spec)

«mediation»:
  - Source MUST be a «relator»
  - A relator's mediations must sum to ≥2 minimum cardinality on mediated ends
  - Min cardinality on mediated end CANNOT be 0
  - Every «role»/«roleMixin» must connect (directly or indirectly) to a mediation

«characterization»:
  - Source MUST be a «quality» or «mode»
  - Bearer end multiplicity must be exactly 1

«componentOf»:
  - Both ends must be functional complexes (kinds/subkinds)
  - Whole must have at least 2 parts (weak supplementation)

«memberOf»:
  - Whole end MUST be a «collective»

«participation»:
  - One end MUST be an «event»

«creation»:
  - Source MUST be an «event», target is the created endurant

«historicalDependence»:
  - Links entities based on a past event (no class-type restrictions)

«material»:
  - Domain-level relation; ontologically derived from a relator + its mediations
  - Use for named domain relations between non-relator classes

## Stereotype Selection Guide for Digital Platforms

### When to use `«kind»`
Use for entities with independent identity that could exist outside the platform context:
- Person, Organization (from UFO-C, usually inherited)
- Park, Vehicle, Accommodation, Room (domain-specific physical entities)
- Digital Content, Software (domain-specific digital entities)

### When to use `«subkind»`
Use for rigid specializations that inherit identity from a kind:
- Listing (subkind of Offering On The Platform)
- Booking (subkind of Transaction)
- Commission Fee (subkind of Revenue Stream)
- Payment Provider (subkind of Organization or Software)

### When to use `«role»` vs `«roleMixin»`
- `«role»`: When the role applies to instances of exactly ONE kind. E.g., if only Persons can be Customers, use `«role»`.
- `«roleMixin»`: When the role can be played by instances of DIFFERENT kinds. E.g., if both Persons and Organizations can be Providers, use `«roleMixin»`.

In the DPO, most user roles are `«roleMixin»` because both Persons and Organizations can typically be platform users:
- User, Provider, Customer, Listing Creator → `«roleMixin»`
- Platform Visitor, Logged In User → `«roleMixin»`
- Trip Provider, Airbnb Host → `«roleMixin»` (renamed from generic Provider)

### When to use `«relator»`
Use for entities that exist solely to connect two or more other entities:
- Booking (connects Customer and Provider through a transaction)
- Review (connects reviewer, reviewed entity, and transaction)
- User Affiliation Agreement (connects User and Platform)
- Service Offering (connects Platform Company and Target Community)

The key test: if you remove either connected party, does this entity lose its reason to exist? If yes, it's a relator.

### When to use `«event»`
Use for things that happen (actions, occurrences) rather than things that exist persistently:
- Register, Login (user affiliation events)
- Add Listing, Listing Search, Set Filter (platform interaction events)
- Create Transaction, External Payment (transaction events)
- Review Creation, Send Message (content creation events)

Events connect to participants via `«participation»` relations, and to created entities via `«creation»` relations.

### When to use `«collective»`
Use for groups/collections of entities:
- Target Customer Community (collection of target customers)
- Listing Overview (collection of listings shown in search results)

### When to use `«type»`
Use for classification categories where instances are themselves types:
- Car Type, Accommodation Type, Activity Type
- User Role (types of roles a user can play)

### When to use `«quality»` and `«mode»`
- `«quality»`: Measurable/comparable properties → Price, Rating, Location coordinates
- `«mode»`: Non-measurable intrinsic properties → Permit, Skill, Belief

### When to use `«datatype»` and `«enumeration»`
- `«datatype»`: Value types → Coordinate [longitude, latitude], CurrencyAmount
- `«enumeration»`: Fixed value sets → Listing Status {active, inactive, archived}, Booking Status {pending, confirmed, cancelled}

## Relation Stereotype Guide for Digital Platforms

### `«mediation»`
Connects a `«relator»` to the entities it depends on. Every relator needs at least 2 mediations.
- Booking --mediation--> Customer
- Booking --mediation--> Provider

### `«participation»`
Connects an endurant (object/agent) to an `«event»` it participates in.
- User --participation--> Register (user participates in registration)
- Customer --participation--> Listing Search

### `«creation»`
Specialized participation where an event brings an entity into existence.
- Add Listing --creation--> Listing (the add listing event creates a listing)
- Review Creation --creation--> Review

### `«characterization»`
Connects a `«mode»` or `«quality»` to its bearer.
- Price --characterization--> Listing
- Rating --characterization--> Provider

### `«componentOf»`
Functional part-whole between objects.
- Trip Location --componentOf--> Trip
- Engine --componentOf--> Vehicle

### `«memberOf»`
Membership in a collective.
- Listing --memberOf--> Listing Overview
- Person --memberOf--> Target Customer Community

### `«historicalDependence»`
One entity depends on another due to a past event.
- Review --historicalDependence--> Booking (a review exists because a booking happened)
- Listing Search --historicalDependence--> Transaction Creation (search led to transaction)

### `«material»`
Domain-level relationship derived from a relator.
- Person --"is married to"--> Person (derived from Marriage relator)
- In DPO practice, domain-level relations are typically modeled as plain named associations rather than formal «material» relations.

### `«instantiation»`
Connects instances to their type classifier.
- Car --instantiation--> Car Type
- User Role Assignment --instantiation--> User Role

## Common Patterns in Digital Platform Ontologies

### The Registration Pattern
```
Platform Visitor --participation--> Register (event)
Register --creation--> User Affiliation Agreement (relator)
Register --creation--> Logged In User (roleMixin, replaces visitor status)
Logged In User --participation--> Login (event)
```

### The Listing Pattern (Decentralized)
```
Listing Creator --participation--> Add Listing (event)
Add Listing --creation--> Listing (subkind)
Listing has Listing Description, Offered Price
Target Customer --participation--> Listing Search (event)
Listing Search --historicalDependence--> Transaction Creation (event)
```

### The Transaction Pattern
```
Customer --mediation--> Transaction (relator)
Provider --mediation--> Transaction (relator)
Transaction links to Booking (subkind)
Booking tracks the agreement between parties
```

### The Review Pattern
```
Customer --participation--> Review Creation (event)
Review Creation --creation--> Review (relator)
Review --historicalDependence--> Booking
Review has score, comment attributes
```

## Scale Guidelines

Based on analysis of ~10 real platform ontologies:
- Small platforms (Couchsurfing, GetFit): 20-30 total classes
- Medium platforms (SafaRide, Pooly, RetroKicks): 28-35 total classes
- Large platforms (Airbnb, BlaBlaCar, Uber Eats): 35-50 total classes
- Very large platforms (CreateYourTrip): 50-70+ total classes

Of these, typically 5-15 are platform-specific NEW classes, and the rest come from DPO modules.

A good initial ontology should target the 25-35 class range unless the platform is exceptionally complex.
