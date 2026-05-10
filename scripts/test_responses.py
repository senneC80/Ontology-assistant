import os
from openai import OpenAI

VECTOR_STORE_ID = "vs_6a009d47becc8191a55feff45f454505" 

SYSTEM_PROMPT = "You are an OntoUML modeling assistant. Use the knowledge base."

USER_QUESTION = "What are the DPO modules? Answer in 3 sentences."


def main() -> None:
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4o",  # or whatever model you've been using
        instructions=SYSTEM_PROMPT,
        input=USER_QUESTION,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [VECTOR_STORE_ID],
        }],
    )

    # The response contains structured output; the easy accessor is output_text.
    print(response.output_text)


if __name__ == "__main__":
    main()