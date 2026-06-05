from agent.execution.ExecutionEngine import ExecutionEngine
from agent.memory.MemoryManager import MemoryManager
from agent.planning.PlanningEngine import PlanningEngine
from agent.tasks.TaskEngine import TaskEngine
from agent.tools.ToolExecutionEngine import ToolExecutionEngine
from agent.workflows.WorkflowEngine import WorkflowEngine
from agent.orchestrator.MultiAgentCoordinator import MultiAgentCoordinator
from ai.orchestration.AIOrchestrator import AIOrchestrator


class AgentOrchestrator:
    def __init__(self):
        self.memory = MemoryManager()
        self.tasks = TaskEngine()
        self.planner = PlanningEngine()
        self.tools = ToolExecutionEngine()
        self.execution = ExecutionEngine()
        self.workflows = WorkflowEngine()
        self.coordinator = MultiAgentCoordinator()
        self.ai = AIOrchestrator()

    def status(self):
        return {
            "status": "active",
            "engine": "agent_orchestrator",
            "version": "V9",
        }

    def run(self, prompt: str, context=None):
        context = context or {}
        task = self.tasks.create_task("agent_request", {"prompt": prompt, "context": context})
        plan = self.planner.create_plan(goal=prompt, context=context)
        tool_result = self.tools.execute("runtime", {"prompt": prompt})
        ai_response = self.ai.run(prompt=prompt, context=context)
        execution = self.execution.execute(
            plan=plan,
            tool_result={
                "tool_result": tool_result,
                "ai_response": ai_response,
            },
        )
        self.memory.save_memory("last_prompt", prompt)
        self.tasks.complete_task(task["id"])
        return {
            "agent": "QVerseAgent",
            "status": "completed",
            "prompt": prompt,
            "task": task,
            "plan": plan,
            "execution": execution,
            "ai_response": ai_response,
            "memory": self.memory.list_memories(),
            "coordination": self.coordinator.status(),
        }
