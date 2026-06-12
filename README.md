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
frontend-npm run dev
backend-uvicorn api:app --reload

## 🚀 Features

- 🔗 Accepts any website URL as input
- 🕷️ Recursive web crawling (internal links only)
- 🧹 Clean content extraction using **Crawl4AI + Trafilatura**
- 🧠 Semantic search using embeddings (SentenceTransformers)
- 📦 Vector storage using **ChromaDB**
- 🎯 Cross-Encoder reranking for high-accuracy retrieval
- 💬 AI chatbot answering using **Groq LLM**
- 📚 Source-aware responses (shows article URLs)

---
1. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

2. Install Dependencies
pip install -r requirements.txt

Required Packages:
pip install crawl4ai
pip install trafilatura
pip install langchain-text-splitters
pip install sentence-transformers
pip install chromadb
pip install groq
pip install python-dotenv

 How to Run
Step 1: Crawl Website
python backend/crawl_website.py
Enter:
https://www.thehindu.com

Step 2: Build Vector Database
python backend/test_vector.py

Step 3: Start Chatbot
python backend/chat.py

Key Improvements (Over Basic RAG)
✔ Crawl4AI Recursive Crawling
Efficiently discovers internal website links.

✔ Trafilatura Extraction
Removes ads, menus, login pages, and extracts clean article text.

✔ Cross-Encoder Reranking
Improves retrieval accuracy by re-scoring semantic results.

✔ Source-aware Answers
Answers include article titles and URLs.
