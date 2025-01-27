from pathlib import Path
import weaviate
from shared.profile_ingestion import run_profile
from weaviate.classes.config import Configure

class WeaviateDb:
    def __init__(self, collection_name: str):
        self.client = weaviate.Client("http://localhost:8080")
        self.collection_name = collection_name
        self.class_name = collection_name.capitalize()


        self.client.collections.create(
            self.class_name,
            vectorizer_config=[
                Configure.NamedVectors.text2vec_transformers(
                    name="paragraph_vector",
                    source_properties=["text"]
                )
            ]
        )

    def ingest(self, source: str, documents: list[str]):
        with self.client.batch as batch:
            for doc in documents:
                batch.add_data_object(
                    {"text": doc, "source": source},
                    self.class_name
                )


if __name__ == "__main__":
    run_profile(WeaviateDb)