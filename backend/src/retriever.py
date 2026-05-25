import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
from .config import ENV_PATH

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Load model once at module level
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model ready")


def retrieve(query: str, top_k: int = 5, distance_threshold: float = 0.45) -> list:
    # Step 1: embed the query
    query_embedding = model.encode(query).tolist()

    # Step 2: find similar chunks using cosine distance
    with engine.connect() as conn:
        results = conn.execute(
            text("""
                SELECT 
                    chunk_id,
                    source_file,
                    chunk_index,
                    text,
                    embedding <=> CAST(:embedding AS vector) AS distance
                FROM chunks
                ORDER BY distance ASC
                LIMIT :top_k
            """),
            {
                "embedding": str(query_embedding),
                "top_k": top_k
            }
        )

        chunks = []
        for row in results:
            chunks.append({
                "chunk_id": row.chunk_id,
                "source_file": row.source_file,
                "chunk_index": row.chunk_index,
                "text": row.text,
                "distance": round(float(row.distance), 4)
            })
        
        # Filter out chunks above distance threshold
        # If best result is still above threshold, the query
        # is likely outside our knowledge base entirely
        if chunks and chunks[0]['distance'] > distance_threshold:
            return []

    return chunks


def retrieve_and_display(query: str, top_k: int = 5):
    """
    Wrapper that retrieves and prints results nicely.
    Used for testing and debugging retrieval quality.
    """
    print(f"\nQuery: '{query}'")
    print(f"Top {top_k} results:\n")

    chunks = retrieve(query, top_k)

    for i, chunk in enumerate(chunks):
        print(f"--- Result {i+1} ---")
        print(f"Source: {chunk['source_file']}")
        print(f"Distance: {chunk['distance']} (lower = more similar)")
        print(f"Text: {chunk['text'][:300]}...")
        print()

    return chunks


if __name__ == "__main__":
    # Test with several different query types
    # This tells you immediately if retrieval is working

    # Factual question
    retrieve_and_display("what do capybaras eat")

    # Specific number question  
    retrieve_and_display("how much does a capybara weigh")

    # Care question
    retrieve_and_display("how many capybaras should I keep together")

    # Predator question
    retrieve_and_display("what animals eat capybaras")

    # Negative test - something not in corpus
    retrieve_and_display("do capybaras live in Antarctica")