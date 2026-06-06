export default function ProjectManager({ projectName, setProjectName, onAdd }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Projects</h2>
      <input value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Project name" />
      <button onClick={onAdd} style={{ marginLeft: 8 }}>Add Project</button>
    </section>
  );
}
