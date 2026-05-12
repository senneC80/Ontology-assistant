

## OntoUML Schema JSON (primary export)

This is the canonical export format. It conforms to the **OntoUML Schema v1** published at `https://w3id.org/ontouml/schema/v1.0.0` (source: https://github.com/OntoUML/ontouml-schema). Files in this format can be imported directly into **Visual Paradigm Community Edition** via the `ontouml-vp-plugin` (https://github.com/OntoUML/ontouml-vp-plugin), which restores stereotype colors, cardinalities, and layout, and enables manual refinement of the diagram.

### Structural overview

An OntoUML Schema document is a `Project` containing a single root `Package` (the model), whose `contents` array holds all `Class`, `Relation`, `Generalization`, and `GeneralizationSet` elements. Cross-references between elements (e.g., a generalization's specific/general, a relation's endpoint class) are done by **ID**, not by name.

```
Project
 └── model (Package)
      └── contents: [ Class, Class, …, Relation, Relation, …, Generalization, … ]
```

### ID scheme the assistant MUST use

Generate readable, deterministic IDs so the output is diffable and debuggable:

- Classes: `cls_<snake_case_name>` — e.g., `cls_user`, `cls_activity_listing`
- Relations: `rel_<source>_<stereotype>_<target>` — e.g., `rel_booking_mediation_traveller`
- Generalizations: `gen_<specific>_<general>` — e.g., `gen_traveller_user`
- Class attributes (properties): `prop_<class>_<attr>` — e.g., `prop_user_email`
- Relation endpoints (properties): `end_<relation_id>_source` and `end_<relation_id>_target`

IDs must be unique within the file. If a name collision would occur (e.g., two relations between the same pair), append `_1`, `_2`, etc.

### Stereotype → `restrictedTo` mapping

Every `Class` element MUST include a `restrictedTo` array derived from its stereotype. Visual Paradigm and the symbolic validators rely on this field.

| Stereotype | `restrictedTo` |
|---|---|
| `kind`, `subkind`, `role`, `roleMixin`, `phase`, `category`, `mixin`, `phaseMixin` | `["functional-complex"]` |
| `relator` | `["relator"]` |
| `event` | `["event"]` |
| `collective` | `["collective"]` |
| `quantity` | `["quantity"]` |
| `quality` | `["quality"]` |
| `mode` | `["intrinsic-mode"]` |
| `type` | `["type"]` |
| `datatype`, `enumeration` | `["abstract"]` |

### Cardinality format

Cardinality is a **string** in the form `"<lower>..<upper>"`, where `*` means unlimited.
Examples: `"1"` (exactly one), `"1..*"` (one or more), `"0..*"` (zero or more), `"0..1"` (optional).

### Template (complete worked example)

```json
{
  "id": "project_platformname",
  "name": "PlatformName",
  "type": "Project",
  "model": {
    "id": "pkg_platformname",
    "name": "PlatformName",
    "type": "Package",
    "contents": [

      {
        "id": "cls_user",
        "name": "User",
        "type": "Class",
        "stereotype": "roleMixin",
        "isAbstract": false,
        "isDerived": false,
        "restrictedTo": ["functional-complex"],
        "properties": [
          {
            "id": "prop_user_userid",
            "name": "userID",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "aggregationKind": "NONE"
          },
          {
            "id": "prop_user_email",
            "name": "email",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "aggregationKind": "NONE"
          }
        ]
      },

      {
        "id": "cls_traveller",
        "name": "Traveller",
        "type": "Class",
        "stereotype": "roleMixin",
        "isAbstract": false,
        "isDerived": false,
        "restrictedTo": ["functional-complex"],
        "properties": []
      },

      {
        "id": "cls_host",
        "name": "Host",
        "type": "Class",
        "stereotype": "roleMixin",
        "isAbstract": false,
        "isDerived": false,
        "restrictedTo": ["functional-complex"],
        "properties": []
      },

      {
        "id": "cls_listing",
        "name": "Listing",
        "type": "Class",
        "stereotype": "kind",
        "isAbstract": false,
        "isDerived": false,
        "restrictedTo": ["functional-complex"],
        "properties": [
          {
            "id": "prop_listing_name",
            "name": "name",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "aggregationKind": "NONE"
          },
          {
            "id": "prop_listing_price",
            "name": "price",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "aggregationKind": "NONE"
          }
        ]
      },

      {
        "id": "cls_booking",
        "name": "Booking",
        "type": "Class",
        "stereotype": "relator",
        "isAbstract": false,
        "isDerived": false,
        "restrictedTo": ["relator"],
        "properties": [
          {
            "id": "prop_booking_startdate",
            "name": "startDate",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "aggregationKind": "NONE"
          }
        ]
      },

      {
        "id": "cls_add_listing",
        "name": "Add Listing",
        "type": "Class",
        "stereotype": "event",
        "isAbstract": false,
        "isDerived": false,
        "restrictedTo": ["event"],
        "properties": []
      },

      {
        "id": "rel_booking_mediation_traveller",
        "name": "",
        "type": "Relation",
        "stereotype": "mediation",
        "isAbstract": false,
        "isDerived": false,
        "properties": [
          {
            "id": "end_rel_booking_mediation_traveller_source",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "cardinality": "0..*",
            "propertyType": { "id": "cls_booking", "type": "Class" },
            "aggregationKind": "NONE"
          },
          {
            "id": "end_rel_booking_mediation_traveller_target",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "cardinality": "1",
            "propertyType": { "id": "cls_traveller", "type": "Class" },
            "aggregationKind": "NONE"
          }
        ]
      },

      {
        "id": "rel_booking_mediation_listing",
        "name": "",
        "type": "Relation",
        "stereotype": "mediation",
        "isAbstract": false,
        "isDerived": false,
        "properties": [
          {
            "id": "end_rel_booking_mediation_listing_source",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "cardinality": "0..*",
            "propertyType": { "id": "cls_booking", "type": "Class" },
            "aggregationKind": "NONE"
          },
          {
            "id": "end_rel_booking_mediation_listing_target",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "cardinality": "1",
            "propertyType": { "id": "cls_listing", "type": "Class" },
            "aggregationKind": "NONE"
          }
        ]
      },

      {
        "id": "rel_add_listing_creation_listing",
        "name": "",
        "type": "Relation",
        "stereotype": "creation",
        "isAbstract": false,
        "isDerived": false,
        "properties": [
          {
            "id": "end_rel_add_listing_creation_listing_source",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "cardinality": "1",
            "propertyType": { "id": "cls_add_listing", "type": "Class" },
            "aggregationKind": "NONE"
          },
          {
            "id": "end_rel_add_listing_creation_listing_target",
            "type": "Property",
            "isDerived": false,
            "isReadOnly": false,
            "isOrdered": false,
            "cardinality": "1",
            "propertyType": { "id": "cls_listing", "type": "Class" },
            "aggregationKind": "NONE"
          }
        ]
      },

      {
        "id": "gen_traveller_user",
        "type": "Generalization",
        "general":  { "id": "cls_user",      "type": "Class" },
        "specific": { "id": "cls_traveller", "type": "Class" }
      },

      {
        "id": "gen_host_user",
        "type": "Generalization",
        "general":  { "id": "cls_user", "type": "Class" },
        "specific": { "id": "cls_host", "type": "Class" }
      }

    ]
  }
}
```

### Authoring rules the assistant MUST follow

1. **Emit all `contents` in this order:** all Classes first, then all Relations, then all Generalizations (then any GeneralizationSets). Visual Paradigm import succeeds regardless, but this order is easier to diff and debug.
2. **Every Class MUST have:** `id`, `name`, `type: "Class"`, `stereotype`, `isAbstract`, `isDerived`, `restrictedTo`, `properties` (use `[]` for no attributes).
3. **Every Relation MUST have:** `id`, `type: "Relation"`, `stereotype`, exactly two entries in `properties`, each with `cardinality` and a `propertyType` reference. The `name` field can be empty (`""`) when the stereotype is self-explanatory. Set `name` only if the relation carries a domain-specific label (e.g., `"booked by"` vs the generic `mediation`).
4. **Every Generalization MUST have:** `id`, `type: "Generalization"`, `general` (parent reference), `specific` (child reference). Note the field names carefully — `general` is the **parent**, `specific` is the **child**.
5. **All cross-references use `{ "id": "...", "type": "Class" }` objects**, never bare strings.
6. **Attribute ordering inside a class follows the structured-summary order.** This preserves intent when the file is imported.
7. **Do NOT invent fields outside the schema** (no `description`, `comment`, `moduleOrigin`, etc.). Visual Paradigm will ignore them but they fail schema validation and clutter diffs.

### Closing message when exporting JSON

When you hand the user a JSON export, close with something like:

> Here's your ontology as OntoUML Schema v1 JSON. You can import it directly into Visual Paradigm Community Edition using the `ontouml-vp-plugin` (https://github.com/OntoUML/ontouml-vp-plugin), which will render the diagram with proper stereotype colors and cardinalities and let you refine the layout for publication. 
