import json

from rag.chunker import chunk_documents
from rag.embeddings import generate_embeddings
from rag.vectordb import store_chunks


with open(
    "data/scraped_content.json",
    "r",
    encoding="utf-8"
) as f:

    docs = json.load(f)

chunks = chunk_documents(docs)

print("Chunks:", len(chunks))

embeddings = generate_embeddings(
    chunks
)

store_chunks(
    chunks,
    embeddings
)