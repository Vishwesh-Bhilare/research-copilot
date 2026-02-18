import json
from typing import List, Dict
from src.config import CHUNKS_FILE


def chunk_text(
    pages: List[Dict],
    chunk_size: int = 500,
    overlap: int = 80
) -> List[Dict]:
    """
    Chunks page-level text into smaller segments.
    Never mixes pages.
    """
    chunks = []

    for page in pages:
        text = page["text"]
        tokens = text.split()

        start = 0
        chunk_id_counter = 1

        while start < len(tokens):
            end = start + chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = " ".join(chunk_tokens).strip()

            if chunk_text:
                chunk_obj = {
                    "paper_id": page["paper_id"],
                    "title": page["title"],
                    "page": page["page"],
                    "chunk_id": f"{page['paper_id']}_p{page['page']}_c{chunk_id_counter}",
                    "text": chunk_text
                }
                chunks.append(chunk_obj)
                chunk_id_counter += 1

            start += chunk_size - overlap

    if chunks:
        CHUNKS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CHUNKS_FILE, "a", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    return chunks

