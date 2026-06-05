export const MODELS = [
  "openai",
  "anthropic",
  "gemini",
  "deepseek",
  "qwen",
  "ollama",
  "openrouter",
  "groq",
  "together"
];

export function selectModel(preferred) {
  return preferred || MODELS[0];
}
