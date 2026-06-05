from ai.runtime.AIRuntime import generate_ai_response, runtime_status


def test_ai_runtime_status():
    status = runtime_status()
    assert status["status"] == "running"
    assert status["routing"] == "multi_provider_enterprise"
    assert status["transport"] == "enabled_when_env_present"


def test_ai_response_generation():
    response = generate_ai_response("hello", provider="openai")
    assert response["engine"] == "ai_response_engine"
    assert response["result"]["provider"] == "openai"
