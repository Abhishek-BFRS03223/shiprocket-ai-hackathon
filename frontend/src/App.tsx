import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const mutation = useMutation({
    mutationFn: async (text: string) => {
      const res = await axios.post("/api/chat", { prompt: text });
      return res.data;
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    mutation.mutate(prompt);
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
        <button type="submit" disabled={mutation.isLoading} style={{ marginTop: 8 }}>
          {mutation.isLoading ? "Sending…" : "Send"}
        </button>
      </form>
      {mutation.data && (
        <div style={{ marginTop: 24 }}>
          <strong>Response:</strong>
          <pre>{mutation.data.response}</pre>
        </div>
      )}
      {mutation.isError && <p style={{ color: "red" }}>{(mutation.error as any)?.message}</p>}
    </div>
  );
}

export default App; 