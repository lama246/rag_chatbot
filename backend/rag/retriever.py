from rag.vectordb import (
    get_collection,
    model
)
from rag.reranker import rerank_documents


def retrieve_context(query, db_path):

    collection = get_collection(
        db_path
    )

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=20
    )
    if len(results["documents"][0]) == 0:
        return {
            "documents": [[]],
            "metadatas": [[]]
        }
    docs = results["documents"][0]

    metas = results["metadatas"][0]

    reranked_docs, reranked_meta = (

        rerank_documents(
            query,
            docs,
            metas,
            top_k=5
        )
    )

    return {
        "documents": [reranked_docs],
        "metadatas": [reranked_meta]
    }