class PlanningEngine:
    def create_plan(self, goal: str, context=None):
        context = context or {}
        return {
            "goal": goal,
            "context": context,
            "steps": [
                {"id": 1, "name": "understand_goal", "status": "ready"},
                {"id": 2, "name": "select_tools", "status": "ready"},
                {"id": 3, "name": "execute_task", "status": "ready"},
                {"id": 4, "name": "summarize_result", "status": "ready"},
            ],
            "status": "planned",
        }
