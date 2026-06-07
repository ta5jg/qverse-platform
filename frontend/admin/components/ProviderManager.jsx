const providerLabels = {
  openai: "OpenAI",
  claude: "Claude",
  gemini: "Gemini",
  deepseek: "DeepSeek",
  qwen: "Qwen",
};

export default function ProviderManager({ provider, setProvider, apiKey, setApiKey, onSave, providers = {} }) {
  const active = providers?.[provider];

  return (
    <section className="card accent-blue">
      <div className="card-header">
        <div>
          <p className="eyebrow">Providers</p>
          <h2>Provider API Keys</h2>
          <p className="muted">Manage live AI provider keys securely.</p>
        </div>
        <span className={active?.configured ? "pill ok" : "pill warn"}>{active?.configured ? "Configured" : "Missing"}</span>
      </div>
      <div className="form-row">
        <select value={provider} onChange={(e) => setProvider(e.target.value)}>
          {Object.entries(providerLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
        </select>
        <input value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="Enter API key" type="password" />
        <button className="btn primary" onClick={onSave}>Save Key</button>
      </div>
      <p className="hint">Current key: {active?.masked || "not configured"}</p>
    </section>
  );
}
