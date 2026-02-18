import typer
from rich import print
from src.search.semantic_scholar import search_semantic_scholar
from src.search.openalex import search_openalex
from src.config import DISCOVERY_PROVIDER

app = typer.Typer(help="Local-First Research Co-Pilot")

@app.command()
def search(query: str, limit: int = 5):
    """
    Search academic papers (metadata only).
    """
    print(f"\n[bold cyan]Searching:[/bold cyan] {query}\n")

    if DISCOVERY_PROVIDER == "semantic_scholar":
        results = search_semantic_scholar(query, limit)
    else:
        results = search_openalex(query, limit)

    if not results:
        print("[red]No results found.[/red]")
        return

    for i, paper in enumerate(results, start=1):
        print(f"[bold]{i}.[/bold] {paper['title']}")
        print(f"    Authors: {paper.get('authors', 'N/A')}")
        print(f"    Year: {paper.get('year', 'N/A')}")
        print(f"    Source: {paper.get('source', 'N/A')}")
        print()

if __name__ == "__main__":
    app()

