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

    pairs = [
        (query, doc)
        for doc in documents
    ]

    scores = reranker.predict(
        pairs
    )

    ranked = sorted(
        zip(
            scores,
            documents,
            metadatas
        ),
        reverse=True,
        key=lambda x: x[0]
    )

    top_docs = []
    top_meta = []

    for score, doc, meta in ranked[:top_k]:

        top_docs.append(doc)

        top_meta.append(meta)

    return top_docs, top_meta