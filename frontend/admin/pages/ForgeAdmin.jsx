import { useEffect, useMemo, useState } from "react";
import AgentManager from "../components/AgentManager.jsx";
import LiveChatTest from "../components/LiveChatTest.jsx";
import MemoryManager from "../components/MemoryManager.jsx";
import PluginManager from "../components/PluginManager.jsx";
import ProjectManager from "../components/ProjectManager.jsx";
import ProviderManager from "../components/ProviderManager.jsx";
import ProviderTest from "../components/ProviderTest.jsx";
import SystemStatus from "../components/SystemStatus.jsx";
import TwitterDraftManager from "../components/TwitterDraftManager.jsx";

const API_BASE = "https://api.q-verse.io";

const sections = [
  { id: "dashboard", label: "Dashboard" },
  { id: "providers", label: "Providers" },
  { id: "projects", label: "Projects" },
  { id: "agents", label: "Agents" },
  { id: "plugins", label: "Plugins" },
  { id: "live-chat", label: "Live Chat" },
  { id: "memory", label: "Memory" },
  { id: "twitter", label: "Twitter/X" },
  { id: "system", label: "System Status" },
];

export default function ForgeAdmin() {
  const [status, setStatus] = useState(null);
  const [activeSection, setActiveSection] = useState("dashboard");
  const [provider, setProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [projectName, setProjectName] = useState("");
  const [agentName, setAgentName] = useState("");
  const [pluginName, setPluginName] = useState("");
  const [memoryKey, setMemoryKey] = useState("");
  const [memoryValue, setMemoryValue] = useState("");
  const [draftText, setDraftText] = useState("");
  const [message, setMessage] = useState("");
  const [chatMessage, setChatMessage] = useState("Bu cevabı hangi provider üretiyor?");
  const [chatResult, setChatResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const providers = status?.provider_admin || {};
  const projects = status?.projects || {};
  const agents = status?.agents || {};
  const plugins = status?.plugins || {};

  const sectionTitle = useMemo(() => sections.find((item) => item.id === activeSection)?.label || "Dashboard", [activeSection]);

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
    if (!projectName.trim()) return;
    await postJson("/forge/projects", { name: projectName, config: { source: "admin", status: "active" } });
    setProjectName("");
  }

  async function addAgent() {
    if (!agentName.trim()) return;
    await postJson("/forge/agents", { name: agentName, config: { source: "admin", status: "running" } });
    setAgentName("");
  }

  async function addPlugin() {
    if (!pluginName.trim()) return;
    await postJson("/forge/plugins", { name: pluginName, config: { source: "admin", enabled: true } });
    setPluginName("");
  }

  async function saveMemory() {
    if (!memoryKey.trim()) return;
    await postJson("/forge/memory/save", { namespace: "admin", key: memoryKey, value: memoryValue });
    setMemoryKey("");
    setMemoryValue("");
  }

  async function createTwitterDraft() {
    if (!draftText.trim()) return;
    await postJson("/forge/twitter/draft", { text: draftText });
    setDraftText("");
  }

  async function sendChatTest() {
    setLoading(true);
    try {
      const data = await postJson("/agents/chat", { message: chatMessage, source: "forge-admin", user_id: "admin" });
      setChatResult(data);
    } finally {
      setLoading(false);
    }
  }

  async function testProviders() {
    setLoading(true);
    try {
      await sendChatTest();
    } finally {
      setLoading(false);
    }
  }

  function showSection(id) {
    setActiveSection(id);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  useEffect(() => { refresh(); }, []);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><div className="logo">Q</div><strong>Q-Verse Forge</strong></div>
        <nav>
          {sections.map((item) => (
            <button key={item.id} className={activeSection === item.id ? "active" : ""} onClick={() => showSection(item.id)}>
              {item.label}
            </button>
          ))}
        </nav>
        <div className="sidebar-foot"><span className="dot ok"></span> Ultimate V12.2</div>
      </aside>

      <main className="dashboard">
        <header className="topbar" id="dashboard">
          <div>
            <p className="eyebrow">Q-Verse Platform</p>
            <h1>Q-Verse Forge Admin <span>V12.2</span></h1>
            <p className="muted">{sectionTitle} paneli: providers, API keys, projects, agents, plugins, workflows, memory and integrations.</p>
          </div>
          <div className="user-card"><span className="dot ok"></span> System Online</div>
        </header>

        {activeSection === "dashboard" && (
          <>
            <section className="stats-grid">
              <div className="stat"><span>Providers</span><strong>{Object.keys(providers).length}</strong><small>Available</small></div>
              <div className="stat"><span>Projects</span><strong>{Object.keys(projects).length}</strong><small>Active</small></div>
              <div className="stat"><span>Agents</span><strong>{Object.keys(agents).length}</strong><small>Running</small></div>
              <div className="stat"><span>Plugins</span><strong>{Object.keys(plugins).length}</strong><small>Installed</small></div>
            </section>
            <section className="grid two">
              <ProviderManager provider={provider} setProvider={setProvider} apiKey={apiKey} setApiKey={setApiKey} onSave={saveProviderKey} providers={providers} />
              <LiveChatTest chatMessage={chatMessage} setChatMessage={setChatMessage} chatResult={chatResult} onSend={sendChatTest} loading={loading} />
            </section>
            <section className="grid two">
              <ProjectManager projectName={projectName} setProjectName={setProjectName} onAdd={addProject} projects={projects} />
              <ProviderTest providers={providers} onTest={testProviders} loading={loading} />
            </section>
          </>
        )}

        {activeSection === "providers" && <ProviderManager provider={provider} setProvider={setProvider} apiKey={apiKey} setApiKey={setApiKey} onSave={saveProviderKey} providers={providers} />}
        {activeSection === "projects" && <ProjectManager projectName={projectName} setProjectName={setProjectName} onAdd={addProject} projects={projects} />}
        {activeSection === "agents" && <AgentManager agentName={agentName} setAgentName={setAgentName} onAdd={addAgent} agents={agents} />}
        {activeSection === "plugins" && <PluginManager pluginName={pluginName} setPluginName={setPluginName} onAdd={addPlugin} plugins={plugins} />}
        {activeSection === "live-chat" && <LiveChatTest chatMessage={chatMessage} setChatMessage={setChatMessage} chatResult={chatResult} onSend={sendChatTest} loading={loading} />}
        {activeSection === "memory" && <MemoryManager memoryKey={memoryKey} setMemoryKey={setMemoryKey} memoryValue={memoryValue} setMemoryValue={setMemoryValue} onSave={saveMemory} />}
        {activeSection === "twitter" && <TwitterDraftManager draftText={draftText} setDraftText={setDraftText} onDraft={createTwitterDraft} />}
        {activeSection === "system" && <SystemStatus status={status} onRefresh={refresh} />}

        {message && <pre className="last-action">{message}</pre>}
      </main>
    </div>
  );
}
