import chromadb

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="website_knowledge"
)


def store_chunks(chunks, embeddings):

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(str(i))

        documents.append(
            chunk["content"]
        )

        metadatas.append({

    "url":
    chunk["url"],

    "title":
    chunk["title"]

})

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=documents,
        metadatas=metadatas
    )

    print("Stored in ChromaDB")

