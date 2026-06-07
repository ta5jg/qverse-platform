export default function LiveChatTest({ chatMessage, setChatMessage, chatResult, onSend, loading }) {
  const aiResult = chatResult?.runtime?.ai_response?.result || chatResult?.ai_response?.result || {};
  const provider = aiResult?.provider;
  const fallback = aiResult?.fallback_used;
  const response = aiResult?.response || chatResult?.reply || "Henüz test yapılmadı.";

  return (
    <section className="card chat-card accent-purple" id="live-chat">
      <div className="card-header">
        <div>
          <p className="eyebrow">Live Runtime</p>
          <h2>Live Chat Test</h2>
          <p className="muted">Test the AI response engine in real time.</p>
        </div>
        <span className="pill purple">V12.2 Engine</span>
      </div>
      <div className="chat-window">
        <div className="bubble user">{chatMessage || "Bu cevabı hangi provider üretiyor?"}</div>
        <div className="bubble bot">{response}</div>
      </div>
      <div className="form-row chat-input-row">
        <input value={chatMessage} onChange={(e) => setChatMessage(e.target.value)} placeholder="Mesajınızı yazın..." />
        <button className="btn purple" onClick={onSend} disabled={loading}>{loading ? "Testing..." : "Gönder"}</button>
      </div>
      {provider && <p className="hint">Provider: {provider} · fallback: {String(Boolean(fallback))}</p>}
    </section>
  );
}
