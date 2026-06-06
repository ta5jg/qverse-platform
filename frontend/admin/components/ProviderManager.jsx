export default function ProviderManager({ provider, setProvider, apiKey, setApiKey, onSave }) {
  return (
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
      <button onClick={onSave} style={{ marginLeft: 8 }}>Save Key</button>
    </section>
  );
}
