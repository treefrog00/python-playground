from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from shared.profile_ingestion import run_profile

class QdrantDb:
    def __init__(self, collection_name: str):
        self.client = QdrantClient("localhost", port=6333)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2', backend="onnx", model_kwargs={"file_name": "onnx/model.onnx"})
        # Create collection if it doesn't exist
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

        self.collection_name = collection_name

    def ingest(self, source: str, documents: list[str]):
        vectors = self.encoder.encode(documents)
        points = [
            PointStruct(
                id=i,
                vector=vector.tolist(),
                payload={"text": doc, "source": source}
            )
            for i, (doc, vector) in enumerate(zip(documents, vectors))
        ]
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

if __name__ == "__main__":
    run_profile(QdrantDb)