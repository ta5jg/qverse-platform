export default function AgentManager({ agentName, setAgentName, onAdd }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Agents</h2>
      <input value={agentName} onChange={(e) => setAgentName(e.target.value)} placeholder="Agent name" />
      <button onClick={onAdd} style={{ marginLeft: 8 }}>Add Agent</button>
    </section>
  );
}
