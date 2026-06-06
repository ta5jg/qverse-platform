class WorkflowEngine:
    def __init__(self):
        self.workflows = {}

    def create(self, name, steps=None):
        self.workflows[name] = {"steps": steps or [], "status": "ready"}
        return self.workflows[name]

    def run(self, name, payload=None):
        workflow = self.workflows.get(name)
        if not workflow:
            return {"success": False, "error": "workflow_not_found"}
        return {"success": True, "workflow": name, "payload": payload or {}, "steps": workflow["steps"]}

workflow_engine = WorkflowEngine()\n