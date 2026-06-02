import pytest


@pytest.fixture(autouse=True)
def isolate_runtime_env(monkeypatch):
    monkeypatch.setenv("OLI_DISABLE_ENV_FILE", "1")
    monkeypatch.setenv("OLI_MODEL_PROVIDER", "development")
    monkeypatch.delenv("OLI_OPENAI_COMPAT_BASE_URL", raising=False)
    monkeypatch.delenv("OLI_OPENAI_COMPAT_API_KEY", raising=False)
    monkeypatch.delenv("OLI_OPENAI_COMPAT_MODEL", raising=False)
    monkeypatch.delenv("OLLAMA_HOST", raising=False)
    monkeypatch.delenv("OLI_OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("OLI_WEBHOOK_MODEL_URL", raising=False)
    monkeypatch.delenv("OLI_WEBHOOK_MODEL_BEARER_TOKEN", raising=False)

