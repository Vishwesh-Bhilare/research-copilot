import json
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
from src.config import PAGES_FILE


def extract_pdf_pages(pdf_path: Path, paper_id: str, title: str) -> List[Dict]:
    """
    Extracts text page-by-page with page numbers.
    Stores results in pages.jsonl.
    """
    reader = PdfReader(str(pdf_path))
    extracted_pages = []

    for i, page in enumerate(reader.pages):
        page_number = i + 1
        text = page.extract_text()

        if not text:
            continue

        page_obj = {
            "paper_id": paper_id,
            "title": title,
            "page": page_number,
            "text": text.strip()
        }

        extracted_pages.append(page_obj)

    if extracted_pages:
        PAGES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PAGES_FILE, "a", encoding="utf-8") as f:
            for page in extracted_pages:
                f.write(json.dumps(page, ensure_ascii=False) + "\n")

    return extracted_pages

