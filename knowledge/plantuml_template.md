
## PlantUML Template

PlantUML's auto-layout degrades badly on dense class diagrams unless you give it structural hints. The template below uses three techniques to keep output readable even at 20+ classes:

1. **`top to bottom direction`** — forces a vertical hierarchy that matches how humans read ontologies (generalizations flow downward, event-class pairs sit side-by-side).
2. **`together { … }` blocks** — cluster semantically related classes so PlantUML places them near each other, reducing crossing lines.
3. **Ordered source** — declare classes inside `together` blocks grouped by semantic cluster (user hierarchy, listing+creation, booking+payment, trip+locations, community, etc.), then emit **generalizations first** and **relations second**, relations grouped by the same clusters.

### Template

```plantuml
@startuml PlatformName

' ── Layout directives ─────────────────────────────────────────────────
top to bottom direction
skinparam linetype ortho
skinparam nodesep 60
skinparam ranksep 70
skinparam classFontSize 12
skinparam classAttributeIconSize 0
hide circle
hide empty members

' ── Stereotype color coding ───────────────────────────────────────────
skinparam class {
  BackgroundColor<<kind>>         #A9DCDF
  BackgroundColor<<subkind>>      #C9E8EA
  BackgroundColor<<phase>>        #C9E8EA
  BackgroundColor<<role>>         #EDCCF5
  BackgroundColor<<roleMixin>>    #EDCCF5
  BackgroundColor<<relator>>      #F9E79F
  BackgroundColor<<event>>        #F5B7B1
  BackgroundColor<<category>>     #E8DAEF
  BackgroundColor<<collective>>   #FAD7A0
  BackgroundColor<<quantity>>     #FAD7A0
  BackgroundColor<<quality>>      #D2B4DE
  BackgroundColor<<mode>>         #D2B4DE
  BackgroundColor<<type>>         #D5DBDB
  BackgroundColor<<enumeration>>  #ECF0F1
}

' ── Cluster 1: User hierarchy + auth events ──────────────────────────
together {
  class "Platform Visitor" <<roleMixin>>
  class "User"             <<roleMixin>> {
    userID
    email
  }
  class "Logged In User"   <<roleMixin>>
  class "Traveller"        <<roleMixin>>
  class "Host"             <<roleMixin>>
  class "Register"         <<event>> {
    setEmail
    setPassword
  }
  class "Login"            <<event>> {
    checkEmail
    checkPassword
  }
}

' ── Cluster 2: Listing + its creation event ──────────────────────────
together {
  class "Listing"          <<kind>> {
    name
    description
    price
    status
  }
  class "Add Listing"      <<event>> {
    setName
    setDescription
  }
}

' ── Cluster 3: Booking + payment ─────────────────────────────────────
together {
  class "Booking"          <<relator>> {
    startDate
    endDate
    totalPrice
  }
  class "Create Booking"   <<event>>
  class "External Payment" <<event>>
}

' ── Cluster 4: Review ────────────────────────────────────────────────
together {
  class "Review"           <<relator>> {
    score
    comment
  }
  class "Review Creation"  <<event>>
}

' ── Generalizations (emit BEFORE relations) ──────────────────────────
"Platform Visitor" --|> "User"
"Logged In User"   --|> "User"
"Host"             --|> "Logged In User"
"Traveller"        --|> "Logged In User"

' ── Relations (grouped by cluster) ───────────────────────────────────
' Auth
"Register" "1..*" -- "1"    "Platform Visitor" : <<participation>>
"Register" "1"    -- "1"    "User"             : <<creation>>
"Login"    "1..*" -- "1"    "Logged In User"   : <<participation>>

' Listing
"Add Listing" "1"    -- "1"    "Listing" : <<creation>>
"Add Listing" "1..*" -- "1"    "Host"    : <<participation>>
"Listing"     "0..*" -- "1"    "Host"    : <<mediation>>

' Booking
"Create Booking"   "1"    -- "1"    "Booking"   : <<creation>>
"Create Booking"   "1..*" -- "1"    "Traveller" : <<participation>>
"Booking"          "0..*" -- "1"    "Traveller" : <<mediation>>
"Booking"          "0..*" -- "1"    "Listing"   : <<mediation>>
"External Payment" "1"    -- "1"    "Booking"   : <<participation>>

' Review
"Review Creation" "1"    -- "1" "Review"    : <<creation>>
"Review Creation" "1..*" -- "1" "Traveller" : <<participation>>
"Review"          "0..*" -- "1" "Listing"   : <<mediation>>
"Review"          "0..*" -- "1" "Traveller" : <<mediation>>
"Review"          "0..*" -- "1" "Booking"   : <<historicalDependence>>

@enduml
```

### Authoring rules the assistant MUST follow

1. **Always emit `top to bottom direction`**, `skinparam linetype ortho`, `skinparam nodesep`, and `skinparam ranksep` at the top. Do not omit them — they are the single biggest contributor to readability.
2. **Wrap every semantic cluster in a `together { }` block.** Default clusters: (a) user hierarchy + auth events, (b) each `kind` with its `<<creation>>` event, (c) each `relator` with its `<<creation>>` event and any adjacent events like payment, (d) trip/location if present, (e) community/membership if present. Do not put more than ~7 classes in a single `together` block; split if needed.
3. **Declare classes grouped by cluster, not in alphabetical or arbitrary order.** The declaration order strongly influences layout.
4. **Emit generalizations before relations.** PlantUML uses generalizations to anchor the hierarchy; if relations come first, the hierarchy ends up sideways or fragmented.
5. **Group relations by cluster with section comments** (`' ── Booking ──`), matching the class clusters.
6. **Use `<<stereotype>>` as the relation label** (e.g., `: <<mediation>>`), not a prose label. Add a short disambiguating word only when two relations connect the same pair of classes (e.g., `: <<mediation>> booking of` vs `: <<mediation>> booked by`).
7. **Do NOT use inline `#color` overrides on class declarations.** Let the `skinparam` block color by stereotype. This keeps the palette consistent across ontologies.
8. **Omit empty attribute blocks.** `hide empty members` handles this visually, but also don't write `{ }` after a class with no attributes.

### When to produce PlantUML

- Small ontologies (≤15 classes): fine as a default preview.
- Larger ontologies (>15 classes): produce only if the user asks, and warn the user that for a publication-quality diagram they should use the OntoUML Schema JSON export and import it into Visual Paradigm.
