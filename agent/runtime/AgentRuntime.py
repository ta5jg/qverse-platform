from agent.orchestrator.AgentOrchestrator import AgentOrchestrator


class AgentRuntime:
    def __init__(self):
        self.orchestrator = AgentOrchestrator()

    def status(self):
        return {
            "status": "running",
            "version": "V9",
            "engine": "agent_runtime",
        }

    def run(self, prompt: str, context=None):
        return self.orchestrator.run(prompt=prompt, context=context or {})


def runtime_status():
    return AgentRuntime().status()


def run_agent(prompt: str, context=None):
    return AgentRuntime().run(prompt=prompt, context=context or {})
