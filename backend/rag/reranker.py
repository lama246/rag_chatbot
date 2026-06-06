from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(
    query,
    documents,
    metadatas,
    top_k=5
):

    if not documents:
        return [], []

    pairs = [
        (query, doc)
        for doc in documents
    ]

    scores = reranker.predict(
        pairs
    )

    ranked = sorted(
        zip(
            documents,
            metadatas,
            scores
        ),
        key=lambda x: x[2],
        reverse=True
    )

    reranked_docs = [
        x[0]
        for x in ranked[:top_k]
    ]

    reranked_meta = [
        x[1]
        for x in ranked[:top_k]
    ]

    return (
        reranked_docs,
        reranked_meta
    )