export default function TwitterDraftManager({ draftText, setDraftText, onDraft }) {
  return (
    <section className="card">
      <div className="card-header">
        <div>
          <p className="eyebrow">Integrations</p>
          <h2>Twitter/X Draft Queue</h2>
          <p className="muted">Create safe-mode social media drafts.</p>
        </div>
      </div>
      <textarea value={draftText} onChange={(e) => setDraftText(e.target.value)} placeholder="Draft safe-mode post" rows={4} />
      <button className="btn primary full" onClick={onDraft}>Create Draft</button>
    </section>
  );
}
