import requests
from typing import List, Dict
from src.config import SEMANTIC_SCHOLAR_API_KEY

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_semantic_scholar(query: str, limit: int = 5) -> List[Dict]:
    headers = {}
    if SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,externalIds,openAccessPdf"
    }

    response = requests.get(BASE_URL, params=params, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()
    results = []

    for paper in data.get("data", []):
        arxiv_id = None
        pmc_id = None

        external_ids = paper.get("externalIds", {})
        if "ArXiv" in external_ids:
            arxiv_id = external_ids["ArXiv"]
        if "PubMedCentral" in external_ids:
            pmc_id = external_ids["PubMedCentral"]

        if not arxiv_id and not pmc_id:
            continue

        results.append({
            "title": paper.get("title"),
            "authors": ", ".join(a["name"] for a in paper.get("authors", [])),
            "year": paper.get("year"),
            "arxiv_id": arxiv_id,
            "pmc_id": pmc_id,
            "source": "arxiv" if arxiv_id else "pmc"
        })

    return results

