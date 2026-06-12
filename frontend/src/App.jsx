import { useState } from "react";
import axios from "axios";
import {
  FiSearch,
  FiSend,
  FiRefreshCw,
  FiDatabase
} from "react-icons/fi";

import "./App.css";
import { useRef } from "react";
export default function App() {
  const [indexExists, setIndexExists] = useState(false);
  const [url, setUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [indexed, setIndexed] = useState(false);
  const [showIndexChoice, setShowIndexChoice] = useState(false);
  const [progress, setProgress] = useState(0);
  const messageRefs = useRef({});
  const [pagesIndexed,setPagesIndexed] = useState(0);
  

  const [pendingUrl, setPendingUrl] = useState("");
  
  const [loading, setLoading] = useState(false);

  const API = "https://amal1357-rag.hf.space";

  const checkAndIndex = async () => {

    if (!url) return;

    const res = await axios.post(
      `${API}/check-index`,
      {
        url,
      }
    );

    if (res.data.exists) {

      setPendingUrl(url);
      setIndexExists(true);

      return;
    }

    await indexWebsite(false);
  };
  const indexWebsite = async (refresh) => {

    setLoading(true);

    setProgress(0);

    const interval = setInterval(
      async () => {

        try {

          const res =
            await axios.get(
              `${API}/progress`
            );

          const current =
            res.data.current;

          const total =
            res.data.total;

          if (total > 0) {

            const percent =
              Math.floor(
                (current / total) * 100
              );

            setProgress(percent);
          }

        } catch (err) {
          console.log(err);
        }

      },
      500
    );

    try {

      const res = await axios.post(
        `${API}/index`,
        {
          url: pendingUrl || url,
          refresh
        }
      );

      setPagesIndexed(
        res.data.pages_indexed
      );

      setIndexed(true);

    } finally {

      clearInterval(interval);

      setProgress(100);

      setLoading(false);

      setShowIndexChoice(false);
    }
  };

  const handleAsk = async () => {
    if (!question) return;

    const userQuestion = question;
    const targetMessageIndex = messages.length;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    const res = await axios.post(`${API}/ask`, {
      url,
      question: userQuestion,
    });

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: res.data.answer,
        sources: res.data.sources || [],
      },
    ]);
    setHistory((prev) => [
      {
        url,
        question: userQuestion,
        answer: res.data.answer,
        timestamp: new Date().toLocaleString(),
        targetIndex: targetMessageIndex
      },
      ...prev,
    ]);

    setLoading(false);
  };

  return (
    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        

        <div className="searchBar">
          <FiSearch />
          <input placeholder="Search history" />
        </div>

        <div className="history">
          {history.map((item, i) => (
            <div 
              key={i} 
              className="historyItem"
              onClick={() =>
                messageRefs.current[item.targetIndex]?.scrollIntoView({
                  behavior: "smooth",
                  block: "start"
                })
              }
            
            >
            
                    {item.question}
            </div>
          ))}
        </div>

      </aside>

      {/* MAIN */}

      <main className="main">

        {messages.length === 0 ? (
          <div className="welcome">

            <h1>
              AI Website Assistant
            </h1>

            <p>
              Index any website and chat with its content
            </p>

            <div className="urlCard">

              <input
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
              />
              {indexExists && (

                  <div className="existingIndexBox">

                    <p>
                      ⚠ This website is already indexed.
                    </p>

                    <div className="existingButtons">

                      <button
                        onClick={() => {
                          setIndexExists(false);
                          indexWebsite(false);
                        }}
                      >
                        Use Existing URL
                      </button>

                      <button
                        className="refreshBtn"
                        onClick={() => {
                          setHistory([]);
                          setMessages([]);
                          setIndexExists(false);
                          indexWebsite(true);
                        }}
                      > <FiRefreshCw />
                        Refresh URL
                      </button>

                    </div>

                  </div>

                )}

              <div className="urlActions">

                <button
                  onClick={checkAndIndex}
                >
                  <FiDatabase />
                  Index Website
                </button>

              </div>
              {loading && (

                <div className="progressContainer">

                  <div
                    className="progressBar"
                    style={{
                      width: `${progress}%`
                    }}
                  />

                  <span>
                    Crawling Website...
                    {progress}%
                  </span>

                </div>

              )}

            </div>

            {indexed && (
              <>
                <div className="indexedTag">
                  ✓ Website Indexed
                </div>

                <div className="ragStats">

                  <div>
                    🌐 Website Indexed
                  </div>

                  <div>
                    📄 Pages: {pagesIndexed}
                  </div>

                  <div>
                    🧠 RAG Enabled
                  </div>

                  <div>
                    🔎 Vector Search Active
                  </div>

                </div>
              </>
            )}

          </div>
        ) : (
          <div className="chatArea">

            {messages.map((msg, index) => (
              <div
                ref={(el) => {
                  messageRefs.current[index] = el;
                }}
                key={index}
                className={`message ${msg.role}`}
              >
                <div className="messageContent">
                  {msg.content}
                </div>

                {msg.sources &&
                  msg.sources.length > 0 && (
                    <div className="sources">

                      <h4>Retrieved Sources</h4>

                      {msg.sources.map((s,i)=>(
                        <div
                          key={i}
                          className="sourceCard"
                        >
                          <strong>{s.title}</strong>

                          <p>{s.chunk}</p>

                          <a
                            href={s.url}
                            target="_blank"
                          >
                            Open Source
                          </a>
                        </div>
                      ))}

                    </div>
                  )}
              </div>
            ))}

            {loading && (
              <div className="spinner"></div>
            )}

          </div>
        )}

        {/* INPUT */}

        <div className="chatInput">

          <input
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            placeholder="Ask anything about the website..."
            disabled={!indexed}
          />

          <button
            onClick={handleAsk}
            disabled={!indexed}
          >
            <FiSend />
          </button>

        </div>
            {showIndexChoice && (

  <div className="modalOverlay">

    <div className="modal">

      <h2>
        Website Already Indexed
      </h2>

      <p>
        This website already exists in the index.
      </p>

      <div className="urlActions">

        <button onClick={checkAndIndex}>
          <FiDatabase />
          Index Website
        </button>

      </div>
      

    </div>

  </div>

)}
      </main>
    </div>
  );
}
