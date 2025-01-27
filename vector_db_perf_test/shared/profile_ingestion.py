from pathlib import Path
import time
from typing import Iterable

# caused qdrant to time out
LARGE_BATCH_SIZE = 5000

MEDIUM_BATCH_SIZE = 1000

def ingest(file: Path, vector_db):
    text = file.read_text()
    # Split into paragraphs (chunks separated by blank lines)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    batch_size = MEDIUM_BATCH_SIZE
    for i in range(0, len(paragraphs), batch_size):
        batch = paragraphs[i:i + batch_size]
        vector_db.ingest(file, batch)

def query(collection, query):
    results = collection.query(
        query_texts=[query],
        n_results=2,
    )

    print("\nQuery Results:")
    for doc in results['documents'][0]:
        print(f"\n{doc}\n")

def time_ingest(file: Path, vector_db):
    start_time = time.time()
    ingest(file, vector_db)
    duration = time.time() - start_time
    print(f"Ingest duration {file}: {duration} seconds")

def time_ingest_many(files: Iterable[Path], vector_db, one_giant_doc: bool, exclude: set[str]):
    start_time = time.time()

    paras = []
    if one_giant_doc:
        for file in files:
            if any(exclusion in file.parts for exclusion in exclude):
                continue
            print(f"Reading {file}")

            paras.extend(t.strip() for t in file.read_text().split('\n\n'))
            paras = [t for t in paras if t]
        print(f"{len(paras)} paragraphs read, total characters: {sum(len(p) for p in paras)}")

        batch_size = MEDIUM_BATCH_SIZE
        for i in range(0, len(paras), batch_size):
            batch = paras[i:i + batch_size]
            vector_db.ingest("one-giant-doc", batch)

    for file in files:
        print(f"Ingesting {file}")
        ingest(file.stem, vector_db)

    duration = time.time() - start_time
    print(f"Ingest duration complete: {duration} seconds")


def run_profile(vector_db_class):
    for file in [Path("documents/poem.txt"), Path("documents/complete_shakespeare.txt")]:
        time_ingest(file, vector_db_class(file.stem))