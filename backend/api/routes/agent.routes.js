export const ROUTE = "/agent";

export async function runAgentRoute(req, res) {
  const prompt = req.body?.prompt || "";
  return res.json({
    agent: "QVerseAgent",
    status: "received",
    prompt,
    runtime: "python-agent-runtime",
  });
}
