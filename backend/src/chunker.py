import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List

PROJECT_ROOT = Path(__file__).parent.parent.parent
FILTERED_DIR = PROJECT_ROOT / "data" / "filtered"
CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class Chunk:
    chunk_id: str
    source_file: str
    chunk_index: int
    text: str
    word_count: int


def split_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    words = text.split()
    chunks = []
    
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)
        chunks.append(chunk_text)
        
        # Move forward by (chunk_size - overlap)
        # So next chunk starts overlap words before this one ended
        start += chunk_size - overlap
        
        # If remaining words are less than half a chunk, 
        # absorb them into the last chunk instead of making
        # a tiny orphan chunk
        if start < len(words) and len(words) - start < chunk_size // 2:
            chunk_words = words[start:]
            chunk_text = ' '.join(chunk_words)
            chunks.append(chunk_text)
            break
    
    return chunks


def chunk_file(filepath: Path, chunk_size: int, overlap: int) -> List[Chunk]:
    text = filepath.read_text(encoding='utf-8')
    source_name = filepath.name
    
    raw_chunks = split_into_chunks(text, chunk_size, overlap)
    
    chunks = []
    for i, chunk_text in enumerate(raw_chunks):
        chunk = Chunk(
            chunk_id=f"{source_name}_chunk_{i:03d}",
            source_file=source_name,
            chunk_index=i,
            text=chunk_text,
            word_count=len(chunk_text.split())
        )
        chunks.append(chunk)
    
    return chunks


def chunk_all_files(chunk_size: int = 200, overlap: int = 50) -> List[Chunk]:
    all_chunks = []
    files = sorted(FILTERED_DIR.glob("*.txt"))
    
    print(f"Chunking {len(files)} files")
    print(f"Chunk size: {chunk_size} words, Overlap: {overlap} words\n")
    
    for filepath in files:
        chunks = chunk_file(filepath, chunk_size, overlap)
        all_chunks.extend(chunks)
        print(f"  {filepath.name:<45} → {len(chunks)} chunks")
    
    print(f"\nTotal chunks: {len(all_chunks)}")
    return all_chunks


def save_chunks(chunks: List[Chunk], chunk_size: int, overlap: int):
    filename = f"chunks_size{chunk_size}_overlap{overlap}.json"
    output_path = CHUNKS_DIR / filename
    
    # Convert dataclasses to dicts for JSON serialization
    chunks_data = {
        "metadata": {
            "chunk_size": chunk_size,
            "overlap": overlap,
            "total_chunks": len(chunks),
            "source_files": list(set(c.source_file for c in chunks))
        },
        "chunks": [asdict(c) for c in chunks]
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to: data/chunks/{filename}")
    return output_path


def analyze_chunks(chunks: List[Chunk]):
    """
    Prints statistics about the chunks.
    Helps verify chunking worked correctly before embedding.
    """
    word_counts = [c.word_count for c in chunks]
    
    print(f"\n=== Chunk Analysis ===")
    print(f"Total chunks: {len(chunks)}")
    print(f"Min words: {min(word_counts)}")
    print(f"Max words: {max(word_counts)}")
    print(f"Avg words: {sum(word_counts) / len(word_counts):.1f}")
    
    print(f"\nSample chunks:")
    
    # Show first chunk
    print(f"\n--- Chunk 0 (first) ---")
    print(f"Source: {chunks[0].source_file}")
    print(f"Text preview: {chunks[0].text[:200]}...")
    
    # Show a middle chunk
    mid = len(chunks) // 2
    print(f"\n--- Chunk {mid} (middle) ---")
    print(f"Source: {chunks[mid].source_file}")
    print(f"Text preview: {chunks[mid].text[:200]}...")
    
    # Better overlap verification
    # Find two consecutive chunks from the same file
    # Then check the ACTUAL overlapping text matches
    print(f"\n--- Overlap verification ---")
    for i in range(len(chunks) - 1):
        if chunks[i].source_file == chunks[i+1].source_file:
            chunk_a = chunks[i]
            chunk_b = chunks[i+1]
            
            # The last 'overlap' words of chunk A should be
            # the first 'overlap' words of chunk B
            # We use 50 as that's our overlap setting
            last_50_of_a = ' '.join(chunk_a.text.split()[-50:])
            first_50_of_b = ' '.join(chunk_b.text.split()[:50])
            
            print(f"Last 50 words of chunk {i}:")
            print(f"  ...{last_50_of_a}")
            print(f"\nFirst 50 words of chunk {i+1}:")
            print(f"  {first_50_of_b}...")
            print(f"\nDo they match: {last_50_of_a == first_50_of_b}")
            break


if __name__ == "__main__":
    # Run with default settings first
    chunks = chunk_all_files(chunk_size=200, overlap=50)
    analyze_chunks(chunks)
    save_chunks(chunks, chunk_size=200, overlap=50)