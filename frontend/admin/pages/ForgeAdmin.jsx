import { useEffect, useState } from "react";
import AgentManager from "../components/AgentManager.jsx";
import MemoryManager from "../components/MemoryManager.jsx";
import PluginManager from "../components/PluginManager.jsx";
import ProjectManager from "../components/ProjectManager.jsx";
import ProviderManager from "../components/ProviderManager.jsx";
import SystemStatus from "../components/SystemStatus.jsx";
import TwitterDraftManager from "../components/TwitterDraftManager.jsx";

const API_BASE = "https://api.q-verse.io";

export default function ForgeAdmin() {
  const [status, setStatus] = useState(null);
  const [provider, setProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [projectName, setProjectName] = useState("");
  const [agentName, setAgentName] = useState("");
  const [pluginName, setPluginName] = useState("");
  const [memoryKey, setMemoryKey] = useState("");
  const [memoryValue, setMemoryValue] = useState("");
  const [draftText, setDraftText] = useState("");
  const [message, setMessage] = useState("");

  async function refresh() {
    const res = await fetch(`${API_BASE}/forge/status`);
    setStatus(await res.json());
  }

  async function postJson(path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await res.json();
    setMessage(JSON.stringify(data, null, 2));
    await refresh();
    return data;
  }

  async function saveProviderKey() {
    await postJson("/forge/providers/key", { provider, api_key: apiKey });
    setApiKey("");
  }

  async function addProject() {
    await postJson("/forge/projects", { name: projectName, config: { source: "admin" } });
    setProjectName("");
  }

  async function addAgent() {
    await postJson("/forge/agents", { name: agentName, config: { source: "admin" } });
    setAgentName("");
  }

  async function addPlugin() {
    await postJson("/forge/plugins", { name: pluginName, config: { source: "admin" } });
    setPluginName("");
  }

  async function saveMemory() {
    await postJson("/forge/memory/save", { namespace: "admin", key: memoryKey, value: memoryValue });
    setMemoryKey("");
    setMemoryValue("");
  }

  async function createTwitterDraft() {
    await postJson("/forge/twitter/draft", { text: draftText });
    setDraftText("");
  }

  useEffect(() => { refresh(); }, []);

  return (
    <main style={{ padding: 24, fontFamily: "system-ui", maxWidth: 1100 }}>
      <h1>Q-Verse Forge Admin V12.1</h1>
      <p>Manage providers, API keys, projects, agents, plugins, workflows, memory and integrations.</p>

      <ProviderManager provider={provider} setProvider={setProvider} apiKey={apiKey} setApiKey={setApiKey} onSave={saveProviderKey} />
      <ProjectManager projectName={projectName} setProjectName={setProjectName} onAdd={addProject} />
      <AgentManager agentName={agentName} setAgentName={setAgentName} onAdd={addAgent} />
      <PluginManager pluginName={pluginName} setPluginName={setPluginName} onAdd={addPlugin} />
      <MemoryManager memoryKey={memoryKey} setMemoryKey={setMemoryKey} memoryValue={memoryValue} setMemoryValue={setMemoryValue} onSave={saveMemory} />
      <TwitterDraftManager draftText={draftText} setDraftText={setDraftText} onDraft={createTwitterDraft} />
      <SystemStatus status={status} onRefresh={refresh} />

      {message && (
        <section style={{ marginTop: 24 }}>
          <h2>Last Action</h2>
          <pre style={{ background: "#f5f5f5", padding: 16 }}>{message}</pre>
        </section>
      )}
    </main>
  );
}
