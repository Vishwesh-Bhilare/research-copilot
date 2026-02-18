import json
import faiss
import numpy as np
from pathlib import Path
from src.config import CHUNKS_FILE, FAISS_INDEX_FILE, MAPPING_FILE


def build_faiss_index(embeddings: np.ndarray, chunk_ids):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    FAISS_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX_FILE))

    mapping = {i: chunk_id for i, chunk_id in enumerate(chunk_ids)}
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)

    return index


def load_faiss_index():
    if not FAISS_INDEX_FILE.exists():
        raise Exception("FAISS index not found. Build index first.")

    index = faiss.read_index(str(FAISS_INDEX_FILE))

    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    return index, mapping


def load_chunks():
    if not CHUNKS_FILE.exists():
        return []

    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    return chunks

