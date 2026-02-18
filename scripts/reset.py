import shutil
from pathlib import Path

DATA_DIR = Path("data")

def main():
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)

    (DATA_DIR / "metadata/searches").mkdir(parents=True)
    (DATA_DIR / "pdfs/arxiv").mkdir(parents=True)
    (DATA_DIR / "pdfs/pmc").mkdir(parents=True)
    (DATA_DIR / "extracted").mkdir(parents=True)
    (DATA_DIR / "chunks").mkdir(parents=True)
    (DATA_DIR / "embeddings").mkdir(parents=True)

    print("Project reset successfully.")


if __name__ == "__main__":
    main()

