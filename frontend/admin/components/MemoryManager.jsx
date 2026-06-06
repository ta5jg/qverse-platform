export default function MemoryManager({ memoryKey, setMemoryKey, memoryValue, setMemoryValue, onSave }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Memory</h2>
      <input value={memoryKey} onChange={(e) => setMemoryKey(e.target.value)} placeholder="Memory key" />
      <input
        value={memoryValue}
        onChange={(e) => setMemoryValue(e.target.value)}
        placeholder="Memory value"
        style={{ marginLeft: 8, width: 360 }}
      />
      <button onClick={onSave} style={{ marginLeft: 8 }}>Save Memory</button>
    </section>
  );
}
