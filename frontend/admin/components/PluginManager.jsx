export default function PluginManager({ pluginName, setPluginName, onAdd, plugins = {} }) {
  return (
    <section className="card accent-teal">
      <div className="card-header">
        <div>
          <p className="eyebrow">Extensions</p>
          <h2>Plugins</h2>
          <p className="muted">Install and manage integrations.</p>
        </div>
        <span className="pill ok">{Object.keys(plugins).length} Installed</span>
      </div>
      <div className="form-row">
        <input value={pluginName} onChange={(e) => setPluginName(e.target.value)} placeholder="Plugin name" />
        <button className="btn success" onClick={onAdd}>Add Plugin</button>
      </div>
      <ul className="mini-list">
        {Object.entries(plugins).slice(0, 5).map(([name, cfg]) => <li key={name}><span>{name}</span><b>{cfg?.enabled === false ? "disabled" : "enabled"}</b></li>)}
      </ul>
    </section>
  );
}
