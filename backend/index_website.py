import os

from utils.cache import (
    get_db_path
)

from utils.metadata_manager import (
    save_metadata,
    load_metadata
)

from crawler.crawl4ai_recursive import (
    crawl_website
)

from rag.chunker import (
    chunk_documents
)

from rag.vectordb import (
    store_chunks
)


def index_website(url):

    db_path = get_db_path(url)

    metadata = load_metadata(url)

    if os.path.exists(db_path):

        print("\nWebsite already indexed.")

        print(
            "Last indexed:",
            metadata["last_indexed"]
        )

        choice = input(
            "\n1 = Use Existing Index\n"
            "2 = Refresh Index\n\n"
            "Choose: "
        )

        if choice == "1":

            print(
                "\nLoading existing index..."
            )

            return db_path

        print(
            "\nRefreshing website..."
        )

    else:

        print(
            "\nIndexing website..."
        )

    pages = crawl_website(url)
    import json

    with open(
        "data/scraped_content.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            pages,
            f,
            indent=4,
            ensure_ascii=False
        )
    if len(pages) == 0:

        raise Exception(
            "No content could be extracted from website."
        )
    print("Pages crawled:", len(pages))

    chunks = chunk_documents(
        pages
    )
    if len(chunks) == 0:

        raise Exception(
            "No chunks generated."
        )
    print("Chunks:", len(chunks))

    store_chunks(
        chunks,
        db_path
    )

    save_metadata(
        url,
        len(pages)
    )

    print(
        "\nIndex created successfully."
    )

    return db_path