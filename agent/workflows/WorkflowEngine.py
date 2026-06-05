class WorkflowEngine:
    def __init__(self):
        self.workflows = []

    def register_workflow(self, name: str, steps=None):
        workflow = {
            "name": name,
            "steps": steps or [],
            "status": "registered",
        }
        self.workflows.append(workflow)
        return workflow

    def list_workflows(self):
        return list(self.workflows)

    def run_workflow(self, name: str):
        return {
            "workflow": name,
            "status": "running",
        }
