import json
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel

from src.search.openalex import search_openalex
from src.search.semantic_scholar import search_semantic_scholar
from src.config import DISCOVERY_PROVIDER, PAPERS_FILE
from src.utils.io import write_json
from src.fetch.arxiv import download_arxiv_pdf
from src.fetch.pmc import download_pmc_pdf
from src.pdf.extract import extract_pdf_pages
from src.chunking.chunker import chunk_text
from src.embed.embedder import Embedder
from src.embed.index import build_faiss_index, load_chunks
from src.retrieve.retriever import Retriever
from src.llm.ollama import OllamaClient


console = Console()


def search_step():
    query = Prompt.ask("\n[bold cyan]Enter research query[/bold cyan]")
    limit = 5

    if DISCOVERY_PROVIDER == "semantic_scholar":
        results = search_semantic_scholar(query, limit)
    else:
        results = search_openalex(query, limit)

    if not results:
        console.print("[red]No open-access results found.[/red]")
        return None

    table = Table(title="Search Results")
    table.add_column("#", justify="right")
    table.add_column("Title")
    table.add_column("Year")

    for i, paper in enumerate(results, start=1):
        table.add_row(str(i), paper["title"], str(paper.get("year", "")))

    console.print(table)

    write_json(PAPERS_FILE, results)

    selection = Prompt.ask(
        "Select papers (comma-separated numbers)", default="1"
    )

    indices = [int(i.strip()) - 1 for i in selection.split(",")]
    selected = [results[i] for i in indices if i < len(results)]

    return selected


def ingest_step(selected_papers):
    console.print("\n[bold yellow]Ingesting papers...[/bold yellow]")

    embedder = Embedder()

    for paper in selected_papers:
        paper_id = paper.get("arxiv_id") or paper.get("pmc_id")

        if paper.get("arxiv_id"):
            pdf_path = download_arxiv_pdf(paper["arxiv_id"])
        elif paper.get("pmc_id"):
            pdf_path = download_pmc_pdf(paper["pmc_id"])
        else:
            continue

        pages = extract_pdf_pages(pdf_path, paper_id, paper["title"])
        chunk_text(pages)

    chunks = load_chunks()
    texts = [c["text"] for c in chunks]
    embeddings = embedder.embed_texts(texts)

    build_faiss_index(embeddings, [c["chunk_id"] for c in chunks])

    console.print("[green]Index built successfully.[/green]")


def ask_loop():
    retriever = Retriever()
    llm = OllamaClient()

    while True:
        query = Prompt.ask("\n[bold cyan]Ask question (or 'exit')[/bold cyan]")

        if query.lower() == "exit":
            break

        chunks = retriever.retrieve(query)

        if not chunks:
            console.print("Not supported by the provided papers.")
            continue

        answer = llm.generate(query, chunks)

        if answer.strip() == "Not supported by the provided papers.":
            console.print(answer)
            continue

        # Tightened citation binding: top 5 chunks only
        unique_sources = sorted(
            {f"{c['paper_id']}, p.{c['page']}" for c in chunks[:5]}
        )

        console.print(Panel(answer, title="Answer", expand=False))

        console.print("\n[bold]Sources:[/bold]")
        for src in unique_sources:
            console.print(f"- {src}")


def main():
    console.print("\n[bold magenta]Local-First Research Co-Pilot[/bold magenta]")

    selected = search_step()
    if not selected:
        return

    ingest_step(selected)
    ask_loop()


if __name__ == "__main__":
    main()

