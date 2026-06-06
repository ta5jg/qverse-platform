// Q-Verse Web Console V10.1+
import React, { useState } from "react";

const ENDPOINT = "https://api.q-verse.io/agents/chat";

export default function QVerseConsole() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [raw, setRaw] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    setReply("");
    setRaw(null);
    try {
      const response = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          source: "web-console",
          user_id: "web-user",
          username: "web-user",
          context: { ui: "QVerseConsole" }
        })
      });
      const data = await response.json();
      setRaw(data);
      setReply(data.reply || JSON.stringify(data));
    } catch (error) {
      setReply(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section style={{ padding: 16, maxWidth: 900, margin: "0 auto" }}>
      <h2>Q-Verse Agent Console</h2>
      <textarea
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        placeholder="Ask Q-Verse Agent..."
        rows={6}
        style={{ width: "100%", padding: 12 }}
      />
      <button onClick={sendMessage} disabled={loading || !message.trim()} style={{ marginTop: 12 }}>
        {loading ? "Sending..." : "Send to Q-Verse"}
      </button>
      <div style={{ marginTop: 16 }}>
        <strong>Reply</strong>
        <pre style={{ whiteSpace: "pre-wrap" }}>{reply}</pre>
      </div>
      {raw && (
        <details>
          <summary>Raw Response</summary>
          <pre>{JSON.stringify(raw, null, 2)}</pre>
        </details>
      )}
    </section>
  );
}
