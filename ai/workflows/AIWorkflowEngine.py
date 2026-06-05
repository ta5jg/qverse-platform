class AIWorkflowEngine:
    def __init__(self):
        self.workflows = []

    def register(self, name: str, steps=None):
        workflow = {"name": name, "steps": steps or [], "status": "registered"}
        self.workflows.append(workflow)
        return workflow

    def list_workflows(self):
        return list(self.workflows)
