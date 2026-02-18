from src.retrieve.retriever import Retriever
from src.llm.ollama import OllamaClient


def main():
    query = input("Ask a research question: ").strip()

    retriever = Retriever()
    llm = OllamaClient()

    chunks = retriever.retrieve(query)

    if not chunks:
        print("Not supported by the provided papers.")
        return

    answer = llm.generate(query, chunks)

    if answer.strip() == "Not supported by the provided papers.":
        print(answer)
        return

    unique_sources = sorted(
        {f"{c['paper_id']}, p.{c['page']}" for c in chunks[:5]}
    )

    print("\nAnswer:\n")
    print(answer)

    print("\nSources:")
    for src in unique_sources:
        print(f"- {src}")


if __name__ == "__main__":
    main()

