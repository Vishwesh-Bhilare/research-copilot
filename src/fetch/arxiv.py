import requests
from pathlib import Path
from src.config import ARXIV_DIR

ARXIV_PDF_URL = "https://arxiv.org/pdf/{arxiv_id}.pdf"


def download_arxiv_pdf(arxiv_id: str) -> Path:
    """
    Downloads arXiv PDF and saves locally.
    Returns local file path.
    """
    ARXIV_DIR.mkdir(parents=True, exist_ok=True)

    pdf_url = ARXIV_PDF_URL.format(arxiv_id=arxiv_id)
    output_path = ARXIV_DIR / f"{arxiv_id}.pdf"

    if output_path.exists():
        return output_path

    response = requests.get(pdf_url, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Failed to download arXiv PDF: {arxiv_id}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

