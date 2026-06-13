# 🌐 RAG-Powered Website Chatbot (Recursive Web Crawler + AI Q&A)

An AI-powered **Retrieval-Augmented Generation (RAG)** system that can ingest any website URL, recursively crawl linked pages, extract clean content, and answer user questions based only on the retrieved website data.

This project demonstrates a full **end-to-end RAG pipeline**:
- Web crawling (recursive link discovery)
- Content extraction (clean article text)
- Chunking & embedding
- Vector database storage (ChromaDB)
- Semantic retrieval + Cross-Encoder reranking
- LLM-based answer generation (Groq)

---
#how to run locally, 

open netlify frontend using the link-> https://6a297ede54540825c5a50a83--ragchatnew.netlify.app/

open git bash(right click and paste to paste code in git bash) or vscode terminal or command prompt,

git clone https://github.com/lama246/rag_chatbot

cd rag_chatbot

python -m venv venv

source venv/Scripts/activate(in git bash) or .\venv\Scripts\Activate.ps1(in vscode powershell) or venv\Scripts\activate(in command prompt)

cd backend

pip install -r requirements.txt

create an api key in groq(because git does not allow my groq api key)

export GROQ_API_KEY="use your api key here"

uvicorn api:app --reload

now the backend has loaded, not search for any website and ask question





## 🚀 Features

- 🔗 Accepts any website URL as input
- 🕷️ Recursive web crawling
- 🧹 Clean content extraction using **Crawl4AI + Trafilatura**
- 🧠 Semantic search using embeddings (SentenceTransformers)
- 📦 Vector storage using **ChromaDB**
- 🎯 Cross-Encoder reranking for high-accuracy retrieval
- 💬 AI chatbot answering using **Groq LLM**
- 📚 Source-aware responses (shows article URLs)
- important feature-if already searched url, then we can choose whether to use existing url or refresh url

---

Key Improvements (Over Basic RAG)
✔ Crawl4AI Recursive Crawling
Efficiently discovers internal website links.

✔ Trafilatura Extraction
Removes ads, menus, login pages, and extracts clean article text.

✔ Cross-Encoder Reranking
Improves retrieval accuracy by re-scoring semantic results.

✔ Source-aware Answers
Answers include article titles and URLs.
