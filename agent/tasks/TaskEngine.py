class TaskEngine:
    def __init__(self):
        self.tasks = []

    def create_task(self, title: str, payload=None):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "payload": payload or {},
            "status": "queued",
        }
        self.tasks.append(task)
        return task

    def list_tasks(self):
        return list(self.tasks)

    def complete_task(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                return task
        return {"status": "not_found", "task_id": task_id}
