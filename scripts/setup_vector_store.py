from pathlib import Path
from openai import OpenAI

# Files to upload.
KNOWLEDGE_FILES = [
    "knowledge/system_prompt_short.md",  # actually the system prompt, separate from KB
    "knowledge/dpo_module_patterns.md",
    "knowledge/platform_examples.md",
    "knowledge/ontouml_rules_for_platforms.md",
    "knowledge/ontouml_stereotypes_reference.md",
    "knowledge/output_formats_and_templates3.md",
]


KB_FILES = [
    "knowledge/dpo_module_patterns.md",
    "knowledge/platform_examples.md",
    "knowledge/ontouml_rules_for_platforms.md",
    "knowledge/ontouml_stereotypes_reference.md",
    "knowledge/output_formats_and_templates3.md",
]


def main() -> None:
    client = OpenAI()  # reads OPENAI_API_KEY from env

    print("Uploading files...")
    file_ids = []
    for path_str in KB_FILES:
        path = Path(path_str)
        if not path.exists():
            raise FileNotFoundError(f"Missing: {path}")
        with path.open("rb") as f:
            uploaded = client.files.create(file=f, purpose="assistants")
        print(f"  {path.name} -> {uploaded.id}")
        file_ids.append(uploaded.id)

    print("\nCreating vector store...")
    vs = client.vector_stores.create(
        name="ontology-assistant-kb",
        file_ids=file_ids,
    )
    print(f"\nVector store created: {vs.id}")
    print("\nPaste this into .streamlit/secrets.toml:")
    print(f'vector_store_id = "{vs.id}"')


if __name__ == "__main__":
    main()
