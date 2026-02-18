import numpy as np
from src.embed.embedder import Embedder
from src.embed.index import load_faiss_index, load_chunks
from src.config import TOP_K


class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.index, self.mapping = load_faiss_index()
        self.chunks = load_chunks()
        self.chunk_lookup = {c["chunk_id"]: c for c in self.chunks}

    def retrieve(self, query: str, top_k: int = None):
        if top_k is None:
            top_k = TOP_K

        query_embedding = self.embedder.embed_query(query)
        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for idx in indices[0]:
            chunk_id = self.mapping.get(str(idx)) or self.mapping.get(idx)
            if not chunk_id:
                continue

            chunk = self.chunk_lookup.get(chunk_id)
            if chunk:
                results.append(chunk)

        return results

