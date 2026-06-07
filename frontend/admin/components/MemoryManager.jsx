export default function MemoryManager({ memoryKey, setMemoryKey, memoryValue, setMemoryValue, onSave }) {
  return (
    <section className="card">
      <div className="card-header">
        <div>
          <p className="eyebrow">Memory</p>
          <h2>Memory Manager</h2>
          <p className="muted">Save persistent memory values.</p>
        </div>
      </div>
      <div className="form-row">
        <input value={memoryKey} onChange={(e) => setMemoryKey(e.target.value)} placeholder="Memory key" />
        <input value={memoryValue} onChange={(e) => setMemoryValue(e.target.value)} placeholder="Memory value" />
        <button className="btn primary" onClick={onSave}>Save Memory</button>
      </div>
    </section>
  );
}
