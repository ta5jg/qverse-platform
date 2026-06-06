import { useEffect, useState } from "react";

const API_BASE = "https://api.q-verse.io";

export default function ForgeAdmin() {
  const [status, setStatus] = useState(null);
  const [provider, setProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [projectName, setProjectName] = useState("");
  const [agentName, setAgentName] = useState("");
  const [message, setMessage] = useState("");

  async function refresh() {
    const res = await fetch(`${API_BASE}/forge/status`);
    setStatus(await res.json());
  }

  async function saveProviderKey() {
    const res = await fetch(`${API_BASE}/forge/providers/key`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ provider, api_key: apiKey })
    });
    const data = await res.json();
    setMessage(JSON.stringify(data, null, 2));
    setApiKey("");
    refresh();
  }

  async function addProject() {
    const res = await fetch(`${API_BASE}/forge/projects`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: projectName, config: { source: "admin" } })
    });
    setMessage(JSON.stringify(await res.json(), null, 2));
    setProjectName("");
    refresh();
  }

  async function addAgent() {
    const res = await fetch(`${API_BASE}/forge/agents`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: agentName, config: { source: "admin" } })
    });
    setMessage(JSON.stringify(await res.json(), null, 2));
    setAgentName("");
    refresh();
  }

  useEffect(() => { refresh(); }, []);

  return (
    <main style={{ padding: 24, fontFamily: "system-ui", maxWidth: 1000 }}>
      <h1>Q-Verse Forge Admin</h1>
      <p>Manage providers, API keys, projects, agents, plugins, workflows, memory and integrations.</p>

      <section style={{ marginTop: 24 }}>
        <h2>Provider API Keys</h2>
        <select value={provider} onChange={(e) => setProvider(e.target.value)}>
          <option value="openai">OpenAI</option>
          <option value="claude">Claude</option>
          <option value="gemini">Gemini</option>
          <option value="deepseek">DeepSeek</option>
          <option value="qwen">Qwen</option>
        </select>
        <input
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="Enter API key"
          type="text"
          style={{ marginLeft: 8, width: 360 }}
        />
        <button onClick={saveProviderKey} style={{ marginLeft: 8 }}>Save Key</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Projects</h2>
        <input value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Project name" />
        <button onClick={addProject} style={{ marginLeft: 8 }}>Add Project</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Agents</h2>
        <input value={agentName} onChange={(e) => setAgentName(e.target.value)} placeholder="Agent name" />
        <button onClick={addAgent} style={{ marginLeft: 8 }}>Add Agent</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Live Forge Status</h2>
        <button onClick={refresh}>Refresh</button>
        <pre style={{ background: "#111", color: "#0f0", padding: 16, overflow: "auto" }}>
          {JSON.stringify(status, null, 2)}
        </pre>
      </section>

      {message && (
        <section style={{ marginTop: 24 }}>
          <h2>Last Action</h2>
          <pre style={{ background: "#f5f5f5", padding: 16 }}>{message}</pre>
        </section>
      )}
    </main>
  );
}
