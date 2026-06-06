export default function SystemStatus({ status, onRefresh }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>System Status</h2>
      <button onClick={onRefresh}>Refresh</button>
      <pre style={{ background: "#111", color: "#0f0", padding: 16, overflow: "auto" }}>
        {JSON.stringify(status, null, 2)}
      </pre>
    </section>
  );
}
