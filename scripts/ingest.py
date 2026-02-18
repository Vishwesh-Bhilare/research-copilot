from src.utils.io import read_json
from src.config import PAPERS_FILE
from src.fetch.arxiv import download_arxiv_pdf
from src.fetch.pmc import download_pmc_pdf
from src.pdf.extract import extract_pdf_pages
from src.chunking.chunker import chunk_text
from src.embed.embedder import Embedder
from src.embed.index import build_faiss_index
from src.embed.index import load_chunks


def main():
    papers = read_json(PAPERS_FILE)

    if not papers:
        print("No papers found. Run search first.")
        return

    all_chunk_ids = []
    embedder = Embedder()

    for paper in papers:
        paper_id = (
            paper.get("arxiv_id")
            or paper.get("pmc_id")
        )

        print(f"Ingesting: {paper['title']}")

        if paper.get("arxiv_id"):
            pdf_path = download_arxiv_pdf(paper["arxiv_id"])
        elif paper.get("pmc_id"):
            pdf_path = download_pmc_pdf(paper["pmc_id"])
        else:
            continue

        pages = extract_pdf_pages(pdf_path, paper_id, paper["title"])
        chunks = chunk_text(pages)

        for c in chunks:
            all_chunk_ids.append(c["chunk_id"])

    chunks = load_chunks()
    texts = [c["text"] for c in chunks]

    embeddings = embedder.embed_texts(texts)
    build_faiss_index(embeddings, [c["chunk_id"] for c in chunks])

    print("Index built successfully.")


if __name__ == "__main__":
    main()

