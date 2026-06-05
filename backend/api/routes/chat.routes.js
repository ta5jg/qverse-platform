export const ROUTE = "/chat";

export async function chatRoute(req, res) {
  const message = req.body?.message || req.body?.prompt || "";
  return res.json({
    agent: "QVerseAgent",
    status: "ready",
    message,
    response: "Q-Verse Agent runtime is ready. Connect model provider for live AI responses.",
  });
}
