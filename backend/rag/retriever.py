from rag.vectordb import collection
from rag.reranker import rerank_documents


def retrieve_context(query):

    results = collection.query(

        query_texts=[query],

        n_results=20
    )

    docs = (
        results["documents"][0]
    )

    metas = (
        results["metadatas"][0]
    )

    reranked_docs, reranked_meta = (

        rerank_documents(

            query,

            docs,

            metas,

            top_k=5
        )
    )

    return {

        "documents":
        [reranked_docs],

        "metadatas":
        [reranked_meta]
    }