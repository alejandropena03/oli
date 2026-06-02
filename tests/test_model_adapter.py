import pytest

from packages.orchestrator.model_adapter import (
    DevelopmentModelAdapter,
    FallbackModelAdapter,
    OllamaModelAdapter,
    OpenAICompatibleModelAdapter,
    WebhookModelAdapter,
    _extract_webhook_text,
    get_default_model_adapter,
)


def test_development_model_adapter_produces_research_brief_text():
    model = DevelopmentModelAdapter()

    output = model.complete("competitor_research_brief")

    assert "supervisor de ejecucion" in output
    assert "Lindy" in output


def test_default_model_adapter_uses_development_when_unconfigured(monkeypatch):
    monkeypatch.delenv("OLI_MODEL_PROVIDER", raising=False)

    adapter = get_default_model_adapter()

    assert isinstance(adapter, DevelopmentModelAdapter)


def test_default_model_adapter_can_select_ollama(monkeypatch):
    monkeypatch.setenv("OLI_MODEL_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:11434")
    monkeypatch.setenv("OLI_OLLAMA_MODEL", "qwen-test")

    adapter = get_default_model_adapter()

    assert isinstance(adapter, FallbackModelAdapter)
    assert isinstance(adapter.primary, OllamaModelAdapter)
    assert adapter.primary.host == "http://localhost:11434"
    assert adapter.primary.model == "qwen-test"


def test_openai_compatible_requires_configuration(monkeypatch):
    monkeypatch.setenv("OLI_MODEL_PROVIDER", "openai_compatible")
    monkeypatch.delenv("OLI_OPENAI_COMPAT_BASE_URL", raising=False)
    monkeypatch.delenv("OLI_OPENAI_COMPAT_API_KEY", raising=False)
    monkeypatch.delenv("OLI_OPENAI_COMPAT_MODEL", raising=False)

    with pytest.raises(RuntimeError):
        get_default_model_adapter()


def test_default_model_adapter_can_select_openai_compatible(monkeypatch):
    monkeypatch.setenv("OLI_MODEL_PROVIDER", "openai_compatible")
    monkeypatch.setenv("OLI_OPENAI_COMPAT_BASE_URL", "https://gpu.example.test/v1")
    monkeypatch.setenv("OLI_OPENAI_COMPAT_API_KEY", "test-key")
    monkeypatch.setenv("OLI_OPENAI_COMPAT_MODEL", "test-model")

    adapter = get_default_model_adapter()

    assert isinstance(adapter, FallbackModelAdapter)
    assert isinstance(adapter.primary, OpenAICompatibleModelAdapter)
    assert adapter.primary.base_url == "https://gpu.example.test/v1"
    assert adapter.primary.model == "test-model"


def test_default_model_adapter_can_select_webhook(monkeypatch):
    monkeypatch.setenv("OLI_MODEL_PROVIDER", "webhook")
    monkeypatch.setenv("OLI_WEBHOOK_MODEL_URL", "https://example.test/webhook")
    monkeypatch.setenv("OLI_WEBHOOK_MODEL_BEARER_TOKEN", "test-token")

    adapter = get_default_model_adapter()

    assert isinstance(adapter, FallbackModelAdapter)
    assert isinstance(adapter.primary, WebhookModelAdapter)
    assert adapter.primary.url == "https://example.test/webhook"
    assert adapter.primary.bearer_token == "test-token"


def test_webhook_response_extractor_supports_common_shapes():
    assert _extract_webhook_text("plain text") == "plain text"
    assert _extract_webhook_text('{"response":"ok"}') == "ok"
    assert _extract_webhook_text('{"text":"ok"}') == "ok"
    assert _extract_webhook_text('{"output":"ok"}') == "ok"
    assert _extract_webhook_text('{"choices":[{"message":{"content":"ok"}}]}') == "ok"


class BrokenModel:
    name = "broken"

    def complete(self, prompt: str) -> str:
        raise RuntimeError("boom")


def test_fallback_model_adapter_uses_development_when_primary_fails():
    adapter = FallbackModelAdapter(primary=BrokenModel())

    output = adapter.complete("competitor_research_brief")

    assert "supervisor de ejecucion" in output
    assert adapter.last_provider_used == "development_codex_authored"
    assert "boom" in adapter.last_error
