class TaskQueue:
    def __init__(self):
        self.tasks = []

    def add(self, title, payload=None):
        task = {"id": len(self.tasks) + 1, "title": title, "payload": payload or {}, "status": "queued"}
        self.tasks.append(task)
        return task

    def next(self):
        for task in self.tasks:
            if task["status"] == "queued":
                task["status"] = "running"
                return task
        return None

    def list(self):
        return self.tasks

task_queue = TaskQueue()\n