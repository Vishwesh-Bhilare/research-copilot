import requests
from pathlib import Path
from src.config import PMC_DIR

PMC_PDF_URL = "https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/"


def download_pmc_pdf(pmc_id: str) -> Path:
    """
    Downloads PMC open-access PDF and saves locally.
    Returns local file path.
    """
    PMC_DIR.mkdir(parents=True, exist_ok=True)

    pdf_url = PMC_PDF_URL.format(pmc_id=pmc_id)
    output_path = PMC_DIR / f"{pmc_id}.pdf"

    if output_path.exists():
        return output_path

    response = requests.get(pdf_url, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Failed to download PMC PDF: {pmc_id}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

