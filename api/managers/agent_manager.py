class AgentManager:
    def __init__(self):
        self.name = "QVerseAgent"
        self.version = "V9"
        self.status = "active"

    def get_dashboard(self):
        return {
            "success": True,
            "agent": self.name,
            "version": self.version,
            "status": self.status,
            "capabilities": [
                "chat",
                "planning",
                "execution",
                "memory",
                "tools",
                "workflows",
                "ai_routing",
            ],
            "endpoints": [
                "/agents",
                "/agents/chat",
                "/agents/run",
            ],
        }

    def chat(self, message: str, source: str = "api", user_id: str = "anonymous", context=None):
        try:
            from agent.runtime.AgentRuntime import run_agent
            result = run_agent(message, context={
                "source": source,
                "user_id": user_id,
                "context": context or {},
            })
            ai_result = result.get("ai_response", {}).get("result", {})
            reply = ai_result.get("response") or result.get("execution", {}).get("result") or "Q-Verse Agent completed the request."
            return {
                "success": True,
                "agent": self.name,
                "reply": reply,
                "source": source,
                "user_id": user_id,
                "runtime": result,
            }
        except Exception as exc:
            return {
                "success": False,
                "agent": self.name,
                "error": type(exc).__name__,
                "message": str(exc),
            }

    def run(self, payload=None):
        payload = payload or {}
        message = payload.get("message") or payload.get("prompt") or ""
        return self.chat(
            message=message,
            source=payload.get("source", "api"),
            user_id=str(payload.get("user_id", "anonymous")),
            context=payload.get("context", {}),
        )


agent_manager = AgentManager()
