import json

from rag.chunker import chunk_documents
from rag.vectordb import store_chunks

DB_PATH = "indexes/test_db"

with open(
    "data/scraped_content.json",
    "r",
    encoding="utf-8"
) as f:

    docs = json.load(f)

chunks = chunk_documents(
    docs
)

print(
    "Chunks:",
    len(chunks)
)

store_chunks(
    chunks,
    DB_PATH
)

print(
    "Vector database created successfully."
)