export default function ProviderTest({ providers = {}, onTest, loading }) {
  return (
    <section className="card accent-yellow">
      <div className="card-header">
        <div>
          <p className="eyebrow">Diagnostics</p>
          <h2>Provider Test</h2>
          <p className="muted">Check configured provider status.</p>
        </div>
        <button className="btn ghost" onClick={onTest} disabled={loading}>{loading ? "Testing..." : "Test All"}</button>
      </div>
      <div className="provider-table">
        {Object.entries(providers).map(([name, info]) => (
          <div className="provider-row" key={name}>
            <strong>{name}</strong>
            <span className={info?.configured ? "status ok" : "status warn"}>{info?.configured ? "Configured" : "Missing"}</span>
            <small>{info?.masked || info?.env_key}</small>
          </div>
        ))}
      </div>
    </section>
  );
}
