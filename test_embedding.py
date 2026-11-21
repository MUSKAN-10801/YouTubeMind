
from backend.ingestion.transcript_extractor import fetch_transcript
from backend.ingestion.transcript_processor import process_transcript
from backend.rag.embedding import EmbeddingModel


# Step 1: Fetch YouTube transcript
video_url = "https://youtu.be/O_ewDn_vVz8"

print("\nFetching transcript...")

transcript = fetch_transcript(video_url, language="hi")

print("Transcript fetched successfully!")


# Step 2: Process transcript into chunks
print("\nProcessing transcript...")

chunks = process_transcript(
    transcript["segments"],
    chunk_size=1000,
    chunk_overlap=200
)

print("Total chunks:", len(chunks))


# Step 3: Load embedding model
embedding_model = EmbeddingModel()


# Step 4: Extract text from chunks
texts = [chunk["text"] for chunk in chunks]


# Step 5: Generate embeddings
print("\nGenerating embeddings...")

embeddings = embedding_model.generate_embeddings(texts)


# Step 6: Display results
print("\nEmbedding Generation Completed!")

print("Number of chunks:", len(texts))
print("Embedding shape:", embeddings.shape)
print("Vector dimensions:", embeddings.shape[1])

print("\nFirst chunk embedding:")
print(embeddings[0][:10])


# Step 7: Test single embedding
query = "What is Artificial Intelligence?"

query_embedding = embedding_model.generate_single_embedding(query)

print("\nQuery embedding shape:", query_embedding.shape)

print("\nEmbedding test successful!")
