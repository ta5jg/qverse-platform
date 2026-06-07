export default function AgentManager({ agentName, setAgentName, onAdd, agents = {} }) {
  return (
    <section className="card accent-purple">
      <div className="card-header">
        <div>
          <p className="eyebrow">Runtime</p>
          <h2>Agents</h2>
          <p className="muted">Create and manage AI agents.</p>
        </div>
        <span className="pill ok">{Object.keys(agents).length} Running</span>
      </div>
      <div className="form-row">
        <input value={agentName} onChange={(e) => setAgentName(e.target.value)} placeholder="Agent name" />
        <button className="btn purple" onClick={onAdd}>Add Agent</button>
      </div>
      <ul className="mini-list">
        {Object.entries(agents).slice(0, 5).map(([name, cfg]) => <li key={name}><span>{name}</span><b>{cfg?.status || "active"}</b></li>)}
      </ul>
    </section>
  );
}
