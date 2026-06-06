from rag.retriever import retrieve_context
from rag.generator import generate_answer
from index_website import index_website

url = input(
    "Enter Website URL: "
)

db_path = index_website(
    url
)


while True:

    question = input(
        "\nAsk: "
    )

    results = retrieve_context(
        question,
        db_path
    )
    print("\n===== RETRIEVED DOCS =====\n")

    for i, doc in enumerate(results["documents"][0]):

        print(f"\nDOC {i+1}")
        print(doc[:1000])

    print("\n=========================\n")

    docs = (
        results["documents"][0]
    )

    metas = (
        results["metadatas"][0]
    )

    context = ""

    for doc, meta in zip(
        docs,
        metas
    ):

        context += f"""

Title:
{meta['title']}

Content:
{doc}

"""

    answer = generate_answer(
        question,
        context
    )

    print("\n")
    print("=" * 60)

    print(answer)

    print("\nSources:\n")

    shown = set()

    for meta in metas:

        if meta["url"] not in shown:

            shown.add(
                meta["url"]
            )

            print(
                meta["title"]
            )

            print(
                meta["url"]
            )

            print()