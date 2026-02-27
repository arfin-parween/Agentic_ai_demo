import React, { useState } from "react";
import { askBackend } from "./api";

export default function App() {
  const [message, setMessage] = useState("");
  const [tool, setTool] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  const send = async () => {
    setErr("");
    setTool("");
    setResponse("");
    setLoading(true);

    try {
      const data = await askBackend(message);
      setTool(data.tool_called || "None");
      setResponse(data.response || "");
    } catch (e) {
      setErr(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h1>SafeSpace AI Therapist (Demo)</h1>
        <p className="muted">
          Tip: To trigger demo call, include <b>CALL_DEMO_NOW</b> in your message (if enabled).
        </p>

        <textarea
          className="textarea"
          rows={6}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message here..."
        />

        <div className="row">
          <button className="btn" onClick={send} disabled={loading || !message.trim()}>
            {loading ? "Sending..." : "Ask"}
          </button>
          <button
            className="btn secondary"
            onClick={() => {
              setMessage("");
              setTool("");
              setResponse("");
              setErr("");
            }}
            disabled={loading}
          >
            Clear
          </button>
        </div>

        {err && <div className="error">⚠️ {err}</div>}

        {(tool || response) && (
          <div className="result">
            <div><b>Tool Called:</b> {tool || "None"}</div>
            <div className="hr" />
            <div className="response">{response}</div>
          </div>
        )}
      </div>
    </div>
  );
}