from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from packages.config import load_env_file

if TYPE_CHECKING:
    from packages.orchestrator.model_adapter import ModelAdapter


class ModelStatus(BaseModel):
    provider: str
    configured: bool
    model: str | None = None
    base_url: str | None = None
    fallback_enabled: bool
    effective_adapter: str
    key_present: bool = False


class ModelTestResult(BaseModel):
    ok: bool
    response: str | None = None
    provider_used: str | None = None
    error: str | None = None


def get_model_status(env: dict[str, str] | None = None) -> ModelStatus:
    if env is None:
        import os

        load_env_file()
        env = dict(os.environ)

    provider = env.get("OLI_MODEL_PROVIDER", "development")
    if provider == "openai_compatible":
        return ModelStatus(
            provider=provider,
            configured=bool(
                env.get("OLI_OPENAI_COMPAT_BASE_URL")
                and env.get("OLI_OPENAI_COMPAT_MODEL")
                and env.get("OLI_OPENAI_COMPAT_API_KEY")
            ),
            model=env.get("OLI_OPENAI_COMPAT_MODEL"),
            base_url=env.get("OLI_OPENAI_COMPAT_BASE_URL"),
            fallback_enabled=True,
            effective_adapter="OpenAICompatibleModelAdapter",
            key_present=bool(env.get("OLI_OPENAI_COMPAT_API_KEY")),
        )
    if provider == "ollama":
        return ModelStatus(
            provider=provider,
            configured=True,
            model=env.get("OLI_OLLAMA_MODEL", "qwen2.5:7b"),
            base_url=env.get("OLLAMA_HOST", "http://127.0.0.1:11434"),
            fallback_enabled=True,
            effective_adapter="OllamaModelAdapter",
        )
    if provider == "webhook":
        return ModelStatus(
            provider=provider,
            configured=bool(env.get("OLI_WEBHOOK_MODEL_URL")),
            model="webhook",
            base_url=env.get("OLI_WEBHOOK_MODEL_URL"),
            fallback_enabled=True,
            effective_adapter="WebhookModelAdapter",
            key_present=bool(env.get("OLI_WEBHOOK_MODEL_BEARER_TOKEN")),
        )
    return ModelStatus(
        provider="development",
        configured=True,
        model="development_codex_authored",
        fallback_enabled=False,
        effective_adapter="DevelopmentModelAdapter",
    )


def test_model(model: "ModelAdapter | None" = None) -> ModelTestResult:
    from packages.orchestrator.model_adapter import (
        DevelopmentModelAdapter,
        FallbackModelAdapter,
        get_default_model_adapter,
    )

    adapter = model or get_default_model_adapter()
    try:
        response = adapter.complete("Responde exactamente con: oli_model_ok")
    except Exception as exc:
        return ModelTestResult(ok=False, error=str(exc))

    provider_used = None
    if isinstance(adapter, FallbackModelAdapter):
        provider_used = adapter.last_provider_used
        error = adapter.last_error
    elif isinstance(adapter, DevelopmentModelAdapter):
        provider_used = adapter.name
        error = None
    else:
        provider_used = getattr(adapter, "name", adapter.__class__.__name__)
        error = None

    return ModelTestResult(
        ok="oli_model_ok" in response,
        response=response[:1000],
        provider_used=provider_used,
        error=error,
    )
