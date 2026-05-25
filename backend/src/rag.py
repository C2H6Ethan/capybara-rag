import os
from pathlib import Path
from dotenv import load_dotenv
import anthropic
from retriever import retrieve

load_dotenv(Path(__file__).parent.parent.parent / ".env")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def build_prompt(query: str, chunks: list) -> str:
    context_parts = []
    for i, chunk in enumerate(chunks):
        source = chunk['source_file'].replace('.txt', '').replace('_', ' ')
        context_parts.append(
            f"[Source {i+1}: {source}]\n{chunk['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are a knowledgeable assistant specializing in capybaras. 
Answer the question using ONLY the information provided in the sources below.
If the answer is not contained in the sources, say "I don't have specific information about that in my sources."
Cite sources using [Source N] notation when using information from them.
Be concise and direct.

SOURCES:
{context}

QUESTION: {query}

ANSWER:"""

    return prompt


def ask(query: str, top_k: int = 5, stream: bool = False) -> str:
    # Step 1: retrieve relevant chunks
    chunks = retrieve(query, top_k=top_k)

    # Step 2: build prompt with retrieved context
    prompt = build_prompt(query, chunks)

    # Step 3: send to Claude and get answer
    if stream:
        return _ask_streaming(prompt, chunks)
    else:
        return _ask_complete(prompt, chunks)


def _ask_complete(prompt: str, chunks: list) -> dict:
    """
    Non-streaming version. Returns complete response.
    """
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = message.content[0].text

    return {
        "answer": answer,
        "sources": [
            {
                "source_file": c['source_file'],
                "distance": c['distance'],
                "text_preview": c['text'][:150]
            }
            for c in chunks
        ]
    }


def _ask_streaming(prompt: str, chunks: list):
    """
    Streaming version. Yields text as it arrives from Claude.
    Used by the FastAPI backend to stream responses to the frontend.
    """
    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield text


def ask_cli(query: str):
    """
    Interactive CLI version with nice formatting.
    """
    print(f"\nQuestion: {query}")
    print("=" * 60)
    print("Retrieving relevant chunks...")

    result = ask(query, top_k=5, stream=False)

    print(f"\nAnswer:\n{result['answer']}")

    print(f"\nSources used:")
    for i, source in enumerate(result['sources']):
        print(f"  [{i+1}] {source['source_file']} "
              f"(distance: {source['distance']})")
        print(f"      {source['text_preview']}...")


if __name__ == "__main__":
    questions = [
        "What do capybaras eat?",
        "How much does a capybara weigh?",
        "How many capybaras should I keep together?",
        "What animals prey on capybaras?",
        "Do capybaras live in Antarctica?",
    ]

    for question in questions:
        ask_cli(question)
        print("\n" + "=" * 60 + "\n")