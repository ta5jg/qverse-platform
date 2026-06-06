export default function PluginManager({ pluginName, setPluginName, onAdd }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Plugins</h2>
      <input value={pluginName} onChange={(e) => setPluginName(e.target.value)} placeholder="Plugin name" />
      <button onClick={onAdd} style={{ marginLeft: 8 }}>Add Plugin</button>
    </section>
  );
}
