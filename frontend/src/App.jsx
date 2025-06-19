import { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    
    setLoading(true);
    setError("");
    setResponse("");
    
    try {
      const res = await axios.post("/api/chat", { prompt });
      setResponse(res.data.response || "No response");
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "3rem auto", fontFamily: "sans-serif" }}>
      <h1>AI Chat</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows={4}
          style={{ width: "100%" }}
          placeholder="Ask something…"
        />
        <button type="submit" disabled={loading} style={{ marginTop: 8 }}>
          {loading ? "Sending…" : "Send"}
        </button>
      </form>
      {response && (
        <div style={{ marginTop: 24 }}>
          <strong>Response:</strong>
          <pre>{response}</pre>
        </div>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App; 