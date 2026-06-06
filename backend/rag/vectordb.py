import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def get_collection(db_path):

    client = chromadb.PersistentClient(
        path=db_path
    )

    collection = client.get_or_create_collection(
        "website_data"
    )

    return collection


import uuid


def store_chunks(chunks, db_path):

    collection = get_collection(
        db_path
    )

    documents = []
    metadatas = []
    embeddings = []
    ids = []

    for chunk in chunks:

        embedding = model.encode(
            chunk["content"]
        ).tolist()

        documents.append(
            chunk["content"]
        )

        embeddings.append(
            embedding
        )

        metadatas.append({

            "url":
            chunk["url"],

            "title":
            chunk["title"]

        })

        ids.append(
            str(uuid.uuid4())
        )

    collection.add(

        ids=ids,

        embeddings=embeddings,

        documents=documents,

        metadatas=metadatas

    )

    return collection