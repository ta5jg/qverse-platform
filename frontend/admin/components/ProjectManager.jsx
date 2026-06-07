export default function ProjectManager({ projectName, setProjectName, onAdd, projects = {} }) {
  return (
    <section className="card accent-green">
      <div className="card-header">
        <div>
          <p className="eyebrow">Core</p>
          <h2>Projects</h2>
          <p className="muted">Create and manage Q-Verse projects.</p>
        </div>
        <span className="pill ok">{Object.keys(projects).length} Active</span>
      </div>
      <div className="form-row">
        <input value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Project name" />
        <button className="btn success" onClick={onAdd}>Add Project</button>
      </div>
      <ul className="mini-list">
        {Object.entries(projects).slice(0, 5).map(([name, cfg]) => <li key={name}><span>{name}</span><b>{cfg?.status || "active"}</b></li>)}
      </ul>
    </section>
  );
}
