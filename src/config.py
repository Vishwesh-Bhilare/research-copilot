import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
METADATA_DIR = DATA_DIR / "metadata"
SEARCH_DIR = METADATA_DIR / "searches"
PDF_DIR = DATA_DIR / "pdfs"
ARXIV_DIR = PDF_DIR / "arxiv"
PMC_DIR = PDF_DIR / "pmc"
EXTRACTED_DIR = DATA_DIR / "extracted"
CHUNKS_DIR = DATA_DIR / "chunks"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"

PAPERS_FILE = METADATA_DIR / "papers.json"
PAGES_FILE = EXTRACTED_DIR / "pages.jsonl"
CHUNKS_FILE = CHUNKS_DIR / "chunks.jsonl"
FAISS_INDEX_FILE = EMBEDDINGS_DIR / "faiss.index"
MAPPING_FILE = EMBEDDINGS_DIR / "mapping.json"

DISCOVERY_PROVIDER = os.getenv("DISCOVERY_PROVIDER", "openalex")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b-instruct-q4_K_M")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", "6"))

