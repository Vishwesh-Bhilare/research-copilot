from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL
import numpy as np


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(
            EMBEDDING_MODEL,
            cache_folder="models/embeddings"
        )

    def embed_texts(self, texts):
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings.astype("float32")

    def embed_query(self, query: str):
        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding.astype("float32")

