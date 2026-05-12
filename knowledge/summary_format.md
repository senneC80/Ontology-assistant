
## Structured Summary Format

Present the core ontology in this exact format:

```
CLASSES:
  «kind» Person [firstName, lastName, email]
  «roleMixin» User [userID, email]
  «roleMixin» Host
  «roleMixin» Traveller
  «subkind» Listing [name, description, price, status]
  «relator» Booking [startDate, endDate, persons, price]
  «event» Register [setEmail, setPassword]
  «event» Add Listing [setName, setDescription]
  «event» Listing Search

RELATIONS:
  Booking [1..*] --mediation--> Traveller [1]
  Booking [1..*] --mediation--> Host [1]
  Add Listing [1] --creation--> Listing [1]
  Traveller [1] --participation--> Listing Search [1..*]
  Review [0..*] --historicalDependence--> Booking [1]
  Register [1..*] --participation--> User [1]

GENERALIZATIONS:
  Host --|> User
  Traveller --|> User
  User --|> Platform Visitor
```

Each class line shows: «stereotype» Name [attributes if any]
Each relation line shows: Source [cardinality] --stereotype--> Target [cardinality]
Each generalization line shows: Specific --|> General

## Optional Extensions Format

After presenting the core ontology, list extensions as a menu:

"You could optionally extend this ontology with:
- **Reviews:** Add Review «relator» with score/comment, Review Creation «event», historicalDependence to Booking
- **Messaging:** Add Conversation «subkind», Send Message «event» between provider and customer roles
- **Payment details:** Add Payment «event», Payment Provider «subkind», Commission Fee «subkind»
- **Listing enrichment:** Add Listing Description «subkind», Listing Overview «collective» for search results
- **Trust & Safety:** Add Verified User «roleMixin», Identity Verification «event»

Would you like me to add any of these?"