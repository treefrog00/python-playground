from sentence_transformers import SentenceTransformer
from shared.profile_ingestion import run_profile

class OnlyVectorization:
    def __init__(self, collection_name: str):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2', backend="onnx", model_kwargs={"file_name": "onnx/model.onnx"})

    def ingest(self, source: str, documents: list[str]):
        vectors = self.encoder.encode(documents)

if __name__ == "__main__":
    run_profile(OnlyVectorization)