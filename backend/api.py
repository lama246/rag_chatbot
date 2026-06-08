from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from index_website import index_website
from rag.retriever import retrieve_context
from rag.generator import generate_answer
from utils.cache import get_db_path
import os
from progress import crawl_progress
app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Request Models
# ----------------------------
class IndexRequest(BaseModel):
    url: str
    refresh: bool = False


class AskRequest(BaseModel):
    url: str
    question: str


# ----------------------------
# INDEX WEBSITE
# ----------------------------
@app.post("/index")
def index_site(req: IndexRequest):

    db_path,pages_count = index_website(
        req.url,
        refresh=req.refresh
    )

    return {
        "status": "success",
        "db_path": db_path,
        "pages_indexed": pages_count
    }


# ----------------------------
# ASK QUESTION
# ----------------------------
@app.post("/ask")
def ask_question(req: AskRequest):

    db_path = index_website(req.url)

    results = retrieve_context(req.question, db_path)

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context = ""
    sources = []

    for doc, meta in zip(docs, metas):
        context += f"Title: {meta.get('title','')}\nContent: {doc}\n\n"
        sources.append({
            "title": meta.get("title", ""),
            "url": meta.get("url", ""),
            "chunk": doc[:250]
        })

    answer = generate_answer(req.question, context)

    return {
        "answer": answer,
        "sources": sources
    }
@app.post("/check-index")
def check_index(req: IndexRequest):

    db_path = get_db_path(req.url)

    return {
        "exists": os.path.exists(db_path)
    }
@app.get("/progress")
def get_progress():

    return crawl_progress