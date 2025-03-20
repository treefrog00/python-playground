from sentence_transformers import SentenceTransformer

def main():
    print("Hello from multihead-attention!")



def embed():
    model = SentenceTransformer(
        "nomic-ai/nomic-embed-text-v2-moe",
        trust_remote_code=True
    )

    sentences = ["Hello!", "¡Hola!"]

    embeddings = model.encode(sentences, prompt_name="passage")

    if __name__ == "__main__":
        main()
