export default function SystemStatus({ status, onRefresh }) {
  const providers = status?.provider_admin || {};
  const projects = status?.projects || {};
  const agents = status?.agents || {};
  const plugins = status?.plugins || {};

  return (
    <section className="card system-card">
      <div className="card-header">
        <div>
          <p className="eyebrow">System</p>
          <h2>Runtime Status</h2>
        </div>
        <button className="btn ghost" onClick={onRefresh}>Refresh</button>
      </div>
      <div className="stats-grid compact">
        <div className="stat"><span>Providers</span><strong>{Object.keys(providers).length}</strong></div>
        <div className="stat"><span>Projects</span><strong>{Object.keys(projects).length}</strong></div>
        <div className="stat"><span>Agents</span><strong>{Object.keys(agents).length}</strong></div>
        <div className="stat"><span>Plugins</span><strong>{Object.keys(plugins).length}</strong></div>
      </div>
      <pre className="status-json">{JSON.stringify(status, null, 2)}</pre>
    </section>
  );
}
