import json
from src.search.semantic_scholar import search_semantic_scholar
from src.search.openalex import search_openalex
from src.config import DISCOVERY_PROVIDER, PAPERS_FILE
from src.utils.io import write_json


def main():
    query = input("Search query: ").strip()
    limit = 5

    if DISCOVERY_PROVIDER == "semantic_scholar":
        results = search_semantic_scholar(query, limit)
    else:
        results = search_openalex(query, limit)

    if not results:
        print("No results found.")
        return

    for i, paper in enumerate(results, start=1):
        print(f"[{i}] {paper['title']} ({paper.get('year', 'N/A')})")

    write_json(PAPERS_FILE, results)
    print("\nSaved results to data/metadata/papers.json")


if __name__ == "__main__":
    main()

