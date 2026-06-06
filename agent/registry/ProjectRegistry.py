class ProjectRegistry:
    def __init__(self):
        self.projects = {}

    def add_project(self, name, config=None):
        self.projects[name] = config or {"status": "active"}
        return {"project": name, "config": self.projects[name]}

    def list_projects(self):
        return self.projects

project_registry = ProjectRegistry()\n