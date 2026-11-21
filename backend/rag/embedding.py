
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:
    """
    Generate numerical embeddings for transcript chunks
    using a HuggingFace Sentence Transformer model.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        print("Loading HuggingFace embedding model...")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded successfully!")

    def generate_embeddings(self, texts: list) -> np.ndarray:
        """
        Convert a list of text chunks into numerical vectors.
        """

        if not texts:
            raise ValueError("No text provided for embedding generation.")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        return embeddings

    def generate_single_embedding(self, text: str) -> np.ndarray:
        """
        Generate an embedding for a single text.
        """

        if not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding
