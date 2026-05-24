from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "Capybaras are the world's largest rodents",
    "They live near rivers and lakes in South America",
    "What do capybaras eat?"
]

embeddings = model.encode(sentences)
print(f"Embedding shape: {embeddings.shape}")
print(f"Each embedding is {embeddings.shape[1]} numbers long")
print(f"First embedding preview: {embeddings[0][:5]}...")