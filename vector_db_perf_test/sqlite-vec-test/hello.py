from pathlib import Path
import sqlite3
import sqlite_vec
from sentence_transformers import SentenceTransformer
from shared.profile_ingestion import run_profile
import sqlite3
import sqlite_vec
import numpy as np


class SqliteVecDb:
    db: sqlite3.Connection
    encoder: SentenceTransformer
    row_number = 0

    def __init__(self, collection_name: str):
        # TODO not currently persisting, which will affect performance
        self.db = sqlite3.connect(":memory:")
        self.db.enable_load_extension(True)
        sqlite_vec.load(self.db)
        self.db.enable_load_extension(False)

        self.encoder = SentenceTransformer('all-MiniLM-L6-v2', backend="onnx", model_kwargs={"file_name": "onnx/model.onnx"})

        self.db.execute("CREATE VIRTUAL TABLE vec_items USING vec0(embedding float[384])")

    def ingest(self, source: str, documents: list[str]):
        vectors = self.encoder.encode(documents, convert_to_numpy=True)

        # TODO include document and source name, not just vectors
        # TODO insert many in a batch?
        # TODO somehow ensure float 32 when first created?
        # TODO rowid is currently manually auto-incremented in this Python code
        """
        https://alexgarcia.xyz/sqlite-vec/python.html

        If your vectors are NumPy arrays, the Python SQLite package allows you to pass it along as-is, since NumPy arrays implement the Buffer protocol. Make sure you cast your array elements to 32-bit floats with .astype(np.float32), as some embeddings will use np.float64.
        """
        print(f"got {len(vectors)} vectors")
        self.row_number += 1
        for i, vec in enumerate(vectors):
            self.row_number += i
            self.db.execute(
                "INSERT INTO vec_items(rowid, embedding) VALUES (?, ?)",
                [self.row_number, vec.astype(np.float32)],
            )

    def query(self, embedding):
        self.db.execute(
        "SELECT vec_length(?)", [embedding.astype(np.float32)]
        )
if __name__ == "__main__":
    run_profile(SqliteVecDb)