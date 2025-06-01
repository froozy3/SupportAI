import { useState } from "react";                // Import React hook for state
import supportIcon from "./chatgpt.png";         // Import support icon image
const URL = "http://localhost:8000/api/";        // Base API URL

export default function App() {
  const [question, setQuestion] = useState("");    // User's question input
  const [data, setData] = useState(null);          // Final answer from backend
  const [error, setError] = useState(null);        // Error message if any
  const [loading, setLoading] = useState(false);   // Loading state while waiting for response
  const [history, setHistory] = useState([]);      // Last 3 question-answer pairs

  const handleSubmit = async () => {
    if (!question.trim()) return; // Don't send empty question

    setLoading(true);             // Start loading
    setError(null);               // Clear previous error
    setData(null);                // Clear previous data

    try {
      // Send POST request to backend
      const res = await fetch(URL + "ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const json = await res.json();  // Parse response

      if (!res.ok) throw new Error(json.detail || "Server error"); // Handle backend error

      setData(json.response); // Save the answer
      setHistory((prev) => {
        const updated = [...prev, { question, answer: json.response }]; // Add to history
        return updated.slice(-3); // Keep only last 3
      });
      setQuestion(""); // Clear input

    } catch (err) {
      setError(err.message); // Show error
    } finally {
      setLoading(false); // End loading
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      {/* App title with icon */}
      <h1 style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <img src={supportIcon} alt="Support Icon" style={{ width: 80, height: 40 }} />
        Support Question Assistant
      </h1>

      {/* Input field */}
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Type your question here..."
        style={{ width: "100%", padding: 8, fontSize: 16 }}
        disabled={loading}
      />

      {/* Ask button */}
      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{ marginTop: 10, padding: 10, fontSize: 16 }}
      >
        {loading ? "Loading..." : "Ask"}
      </button>

      {/* Error message */}
      {error && (
        <div
          style={{
            marginTop: 20,
            padding: 10,
            border: "1px solid red",
            background: "#ffe6e6",
            color: "red",
          }}
        >
          <strong>Error:</strong>
          <p>{error}</p>
        </div>
      )}

      {/* Answer display */}
      {data && (
        <div style={{ marginTop: 20, padding: 10, border: "1px solid #ccc" }}>
          <strong>Answer from Support Bot:</strong>
          <p>{data}</p>
        </div>
      )}

      {/* History block */}
      {history.length > 0 && (
        <div style={{ marginTop: 40 }}>
          <h2 style={{ borderBottom: "2px solid #ddd", paddingBottom: 5 }}>Recent History</h2>
          {history.map(({ question, answer }, idx) => (
            <div
              key={idx}
              style={{
                marginBottom: 15,
                padding: 15,
                border: "1px solid #ddd",
                borderRadius: 8,
                backgroundColor: "#f9f9f9",
                boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              }}
            >
              <p style={{ marginBottom: 6 }}><strong>Q:</strong> {question}</p>
              <p><strong>A:</strong> {answer}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
