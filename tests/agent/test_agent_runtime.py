from agent.runtime.AgentRuntime import run_agent, runtime_status


def test_agent_runtime_status():
    status = runtime_status()
    assert status["status"] == "running"
    assert status["version"] == "V9"


def test_agent_run():
    result = run_agent("hello qverse")
    assert result["agent"] == "QVerseAgent"
    assert result["status"] == "completed"
