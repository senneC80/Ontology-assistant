# Ontology Assistant

A Streamlit chatbot for designing OntoUML digital platform ontologies. The assistant guides users through platform elicitation, taxonomy classification, and ontology generation grounded in the **Digital Platform Ontology (DPO)** and **Unified Foundational Ontology (UFO)**. Every proposed ontology is automatically validated against a set of symbolic OntoUML rules; violations are surfaced in a side panel and can be sent back to the model as a structured repair prompt.

## Features

- **Guided conversation flow** — elicitation → taxonomy confirmation → ontology generation → iterative refinement
- **OntoUML JSON export** — every proposal includes a standards-compliant JSON envelope, available as a download or inline view
- **Symbolic validator** — 9 rules covering structural sanity, identity chains, relator mediation, rigidity constraints, and event connections
- **One-click repair** — select which findings to include, add free-text instructions, and send a structured repair prompt back to the assistant
- **Knowledge base** — DPO module patterns, worked platform examples, stereotype reference, schema spec, and output templates loaded into an OpenAI vector store for grounded retrieval

## Architecture

```
app.py                  Streamlit entry point; two-column layout (chat + validation panel)
backend/
  envelope.py           Extracts OntoUML JSON envelopes from raw LLM reply text
validator/
  __init__.py           Public API: validate(project) → Report
  models.py             Severity, Finding, Report, rule code constants
  graph.py              Builds NetworkX generalization graph + RDFLib graph from JSON
  rules.py              9 validation rules; registry-based (ALL_RULES list)
  repair.py             Formats structured repair prompts from a list of Findings
prompts/
  system_prompt.md      System prompt injected on every API call
knowledge/              Reference documents uploaded to the OpenAI vector store
tests/
  test_validator.py     Pytest suite for the validator package
```

## Validation rules

| Code | Severity | Rule |
|------|----------|------|
| STRUCT_001 | ERROR | JSON parse failure or invalid graph structure (short-circuits) |
| STRUCT_002 | WARNING | Bare Package without Project wrapper (auto-normalized) |
| SYMV_001 | WARNING | Class not connected to any relation or generalization |
| SYMV_002 | ERROR | Generalization cycle |
| SYMV_003 | ERROR | Relator's mediation target ends have minimum cardinality sum < 2 |
| SYMV_004 | ERROR | Role or phase has no identity-provider ancestor |
| SYMV_005 | WARNING | Subkind has no identity-provider ancestor |
| SYMV_006 | ERROR | Non-sortal (category, mixin, roleMixin, phaseMixin) specializes a sortal |
| SYMV_007 | ERROR | Rigid type (kind, subkind, category) specializes an anti-rigid type |
| SYMV_008 | ERROR | Participation relation has no event endpoint |
| SYMV_009 | ERROR | Creation relation source endpoint is not an event |

## Setup

**Prerequisites:** Python 3.12+, an OpenAI API key with a populated vector store.

```bash
# Clone and create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:

```toml
openai_api_key  = "sk-..."
vector_store_id = "vs_..."
model           = "gpt-4o"
app_password    = "your-password"
```

**Populating the vector store:** Upload every file in `knowledge/` to an OpenAI vector store and copy the resulting `vs_...` ID into `secrets.toml`.

```bash
streamlit run app.py
```

## Running tests

```bash
pytest tests/test_validator.py -v
```

The test suite covers `_lower_bound` cardinality parsing and one positive + one negative case for each of the five symbolic rules added in SYMV_003–009.

## Project structure notes

- `validator/graph.py` delegates JSON→RDF conversion to `ontouml-json2graph`. The resulting RDFLib graph is queried via SPARQL inside rules that need relational data (SYMV_003, SYMV_008, SYMV_009); the NetworkX generalization graph is used directly for graph-walk rules (SYMV_001–007).
- The `Relation.properties` array in OntoUML JSON holds the two endpoints. Never use a flat `source`/`target` shape — the validator and Visual Paradigm both require the `properties` structure.
- `restrictedTo` values are OntologicalNature vocabulary, not stereotype names. `kind` maps to `["functional-complex"]`, not `["kind"]`. See `knowledge/ontouml_json_schema.md` for the full mapping table.
