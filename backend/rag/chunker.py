from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

    chunks = []

    for doc in documents:

        text_chunks = splitter.split_text(
            doc["content"]
        )

        for text in text_chunks:

            chunks.append({

                "url":
                doc["url"],

                "title":
                doc["title"],

                "content":
                text

            })

    return chunks