import chromadb
from pathlib import Path
from shared.profile_ingestion import run_profile

class ChromaDb:
    def __init__(self, collection_name: str):
        client = chromadb.PersistentClient(path="./chroma_db")
        self.collection_name = collection_name
        self.collection = client.get_or_create_collection(collection_name)

    def ingest(self, source: str, documents: list[str]):
        self.collection.add(
            documents=documents,
            metadatas=[{"source": source} for _ in documents],
            ids=[f"para{j}" for j in range(i, i + len(documents))],
        )

if __name__ == "__main__":
    run_profile(ChromaDb)