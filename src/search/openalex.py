import requests
from typing import List, Dict

BASE_URL = "https://api.openalex.org/works"

def search_openalex(query: str, limit: int = 5) -> List[Dict]:
    params = {
        "search": query,
        "per-page": limit,
        "filter": "is_oa:true"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return []

    data = response.json()
    results = []

    for work in data.get("results", []):
        arxiv_id = None
        pmc_id = None

        locations = work.get("locations", [])
        for loc in locations:
            url = loc.get("pdf_url")
            if not url:
                continue
            if "arxiv.org" in url:
                arxiv_id = url.split("/")[-1].replace(".pdf", "")
            if "ncbi.nlm.nih.gov/pmc" in url:
                pmc_id = url.split("/")[-2]

        if not arxiv_id and not pmc_id:
            continue

        authors = ", ".join(
            a["author"]["display_name"]
            for a in work.get("authorships", [])
        )

        results.append({
            "title": work.get("display_name"),
            "authors": authors,
            "year": work.get("publication_year"),
            "arxiv_id": arxiv_id,
            "pmc_id": pmc_id,
            "source": "arxiv" if arxiv_id else "pmc"
        })

    return results

