export default function TwitterDraftManager({ draftText, setDraftText, onDraft }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Twitter/X Draft Queue</h2>
      <textarea
        value={draftText}
        onChange={(e) => setDraftText(e.target.value)}
        placeholder="Draft safe-mode post"
        rows={4}
        style={{ width: "100%" }}
      />
      <button onClick={onDraft} style={{ marginTop: 8 }}>Create Draft</button>
    </section>
  );
}
