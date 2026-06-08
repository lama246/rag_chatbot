import os
import json

from utils.cache import get_db_path
from utils.metadata_manager import save_metadata, load_metadata
from crawler.crawl4ai_recursive import crawl_website
from rag.chunker import chunk_documents
from rag.vectordb import store_chunks


def index_website(url, refresh=False):

    db_path = get_db_path(url)

    metadata = load_metadata(url)

    # USE EXISTING INDEX
    if (
        os.path.exists(db_path)
        and metadata
        and not refresh
    ):

        print("Using existing index...")
        return db_path

    # REFRESH INDEX
    if refresh:

        print("Refreshing website index...")

        import shutil

        if os.path.exists(db_path):
            shutil.rmtree(
                db_path,
                ignore_errors=True
            )

    print("Indexing website...")

    pages = crawl_website(url)

    chunks = chunk_documents(
        pages
    )

    store_chunks(
        chunks,
        db_path
    )

    save_metadata(
        url,
        len(pages)
    )

    print("Index created successfully.")

    return db_path, len(pages)