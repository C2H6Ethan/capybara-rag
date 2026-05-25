import json
import os
import time
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .config import ENV_PATH, CHUNKS_DIR

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def load_chunks(chunk_size: int = 200, overlap: int = 50):
    filename = f"chunks_size{chunk_size}_overlap{overlap}.json"
    filepath = CHUNKS_DIR / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Chunks file not found: {filepath}. Run chunker.py first.")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    chunks = data['chunks']
    metadata = data['metadata']

    print(f"Loaded {len(chunks)} chunks")
    print(f"  Chunk size: {metadata['chunk_size']} words")
    print(f"  Overlap: {metadata['overlap']} words")
    print(f"  Sources: {len(metadata['source_files'])} files")

    return chunks


def embed_and_store(chunks, model_name: str = 'all-MiniLM-L6-v2', batch_size: int = 32):
    print(f"\nLoading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    print(f"Model loaded")

    # Check how many chunks already exist in db
    # This lets us resume if something fails halfway through
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM chunks"))
        existing_count = result.scalar()

    if existing_count > 0:
        print(f"\nFound {existing_count} chunks already in database")
        print(f"Clearing table for fresh embed...")
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM chunks"))
            conn.commit()

    print(f"\nEmbedding {len(chunks)} chunks in batches of {batch_size}...")
    start_time = time.time()

    # Process in batches
    db = SessionLocal()
    total_stored = 0

    try:
        for batch_start in range(0, len(chunks), batch_size):
            batch = chunks[batch_start:batch_start + batch_size]
            batch_texts = [c['text'] for c in batch]

            # Generate embeddings for this batch
            # This is the core operation — each text becomes 384 numbers
            embeddings = model.encode(batch_texts, show_progress_bar=False)

            # Store each chunk with its embedding
            for chunk, embedding in zip(batch, embeddings):
                db.execute(
                    text("""
                        INSERT INTO chunks 
                            (chunk_id, source_file, chunk_index, text, embedding)
                        VALUES 
                            (:chunk_id, :source_file, :chunk_index, :text, :embedding)
                        ON CONFLICT (chunk_id) DO UPDATE SET
                            text = EXCLUDED.text,
                            embedding = EXCLUDED.embedding
                    """),
                    {
                        "chunk_id": chunk['chunk_id'],
                        "source_file": chunk['source_file'],
                        "chunk_index": chunk['chunk_index'],
                        "text": chunk['text'],
                        "embedding": embedding.tolist()
                    }
                )
                total_stored += 1

            # Commit after each batch
            db.commit()

            elapsed = time.time() - start_time
            print(f"  Batch {batch_start // batch_size + 1}: "
                  f"stored chunks {batch_start + 1}-{min(batch_start + batch_size, len(chunks))} "
                  f"({elapsed:.1f}s elapsed)")

    finally:
        db.close()

    total_time = time.time() - start_time
    print(f"\nDone. Stored {total_stored} chunks in {total_time:.1f}s")
    print(f"Average: {total_time / total_stored * 1000:.1f}ms per chunk")


def verify_storage():
    print(f"\n=== Verifying storage ===")

    with engine.connect() as conn:
        # Total count
        count = conn.execute(text("SELECT COUNT(*) FROM chunks")).scalar()
        print(f"Total chunks in database: {count}")

        # Check embedding dimensions
        result = conn.execute(text("""
            SELECT chunk_id, source_file, 
                   vector_dims(embedding) as dims,
                   LEFT(text, 100) as preview
            FROM chunks 
            LIMIT 3
        """))

        print(f"\nSample rows:")
        for row in result:
            print(f"\n  chunk_id: {row.chunk_id}")
            print(f"  source: {row.source_file}")
            print(f"  embedding dims: {row.dims}")
            print(f"  text preview: {row.preview}...")

        # Verify all embeddings have correct dimensions
        wrong_dims = conn.execute(text("""
            SELECT COUNT(*) FROM chunks 
            WHERE vector_dims(embedding) != 384
        """)).scalar()

        if wrong_dims == 0:
            print(f"\nAll embeddings have correct dimensions (384)")
        else:
            print(f"\nWARNING: {wrong_dims} chunks have wrong embedding dimensions")


if __name__ == "__main__":
    chunks = load_chunks(chunk_size=200, overlap=50)
    embed_and_store(chunks)
    verify_storage()