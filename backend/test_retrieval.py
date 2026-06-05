from rag.retriever import retrieve_context

question = input(
    "Ask Question: "
)

results = retrieve_context(
    question
)

for i, doc in enumerate(
        results["documents"][0]):

    print("\n")
    print("=" * 50)

    print(
        results["metadatas"][0][i]["url"]
    )

    print(doc[:500])