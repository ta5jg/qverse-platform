export default function LiveChatTest({ chatMessage, setChatMessage, chatResult, onSend, loading }) {
  const provider = chatResult?.runtime?.ai_response?.result?.provider || chatResult?.ai_response?.result?.provider;
  const fallback = chatResult?.runtime?.ai_response?.result?.fallback_used ?? chatResult?.ai_response?.result?.fallback_used;

  return (
    <section className="card chat-card accent-purple">
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
        <div className="bubble bot">{chatResult?.reply || "Henüz test yapılmadı."}</div>
      </div>
      <div className="form-row">
        <input value={chatMessage} onChange={(e) => setChatMessage(e.target.value)} placeholder="Mesajınızı yazın..." />
        <button className="btn purple" onClick={onSend} disabled={loading}>{loading ? "Testing..." : "Gönder"}</button>
      </div>
      {provider && <p className="hint">Provider: {provider} · fallback: {String(Boolean(fallback))}</p>}
    </section>
  );
}
