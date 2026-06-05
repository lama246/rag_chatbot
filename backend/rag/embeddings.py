from sentence_transformers import SentenceTransformer

# Load once
embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def generate_embeddings(chunks):

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings