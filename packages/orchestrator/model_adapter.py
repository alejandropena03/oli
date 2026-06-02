from __future__ import annotations

import json
import os
from typing import Protocol
from urllib import error, request

from packages.config import load_env_file


class ModelAdapter(Protocol):
    """Swappable model interface.

    V0 uses deterministic mocks. Later this can be backed by Ollama, vLLM,
    OpenAI, Anthropic, or a rented GPU endpoint without changing the kernel.
    """

    def complete(self, prompt: str) -> str:
        ...


class MockModelAdapter:
    name = "mock"

    def complete(self, prompt: str) -> str:
        return f"[mock-model] {prompt}"


class MockIntentModelAdapter:
    """Adapter para tests del orchestrator LLM-first.

    Devuelve respuestas JSON válidas para prompts de interpretación de intención,
    y texto plano para prompts de ejecución y síntesis. Permite testear el pipeline
    completo sin red ni modelo real.
    """

    name = "mock_intent"

    _INTENT_RESPONSE = """{
  "goal": "test_mission",
  "summary": "Misión de prueba generada por MockIntentModelAdapter",
  "success_criteria": [
    "el output existe y no está vacío",
    "la misión completa todos los estados del pipeline"
  ],
  "output_format": "text",
  "required_connectors": [],
  "scope_in": ["análisis y síntesis"],
  "scope_out": ["acciones externas"],
  "steps": [
    {
      "order": 1,
      "description": "Analizar la petición del usuario",
      "executor": "Orchestrator",
      "required_connector": null,
      "permission_class": 0
    },
    {
      "order": 2,
      "description": "Sintetizar respuesta",
      "executor": "Orchestrator",
      "required_connector": null,
      "permission_class": 0
    }
  ],
  "confidence": 0.9
}"""

    _VALIDATION_RESPONSE = """{
  "criteria_results": [
    {
      "criterion": "el output existe y no está vacío",
      "passed": true,
      "evidence": "output generado correctamente"
    },
    {
      "criterion": "la misión completa todos los estados del pipeline",
      "passed": true,
      "evidence": "pipeline ejecutado sin errores"
    }
  ],
  "overall_passed": true,
  "score": 1.0,
  "notes": "mock validation passed"
}"""

    def complete(self, prompt: str) -> str:
        # Detectar tipo de prompt por contenido del system prompt
        if '"goal"' in prompt and '"success_criteria"' in prompt:
            return self._INTENT_RESPONSE
        if '"criteria_results"' in prompt and '"overall_passed"' in prompt:
            return self._VALIDATION_RESPONSE
        return f"[mock-intent-model] Respuesta para: {prompt[:100]}"


class DevelopmentModelAdapter:
    """Codex-authored deterministic model for V0 development.

    While Alejandro does not have the target local machine/GPU, this adapter
    gives the orchestrator a stable model boundary. The behavior is authored
    during development and later replaced by Ollama/vLLM without changing the
    Mission Kernel.
    """

    name = "development_codex_authored"

    def complete(self, prompt: str) -> str:
        if "competitor_research_brief" in prompt:
            return (
                "Oli compite contra herramientas como Lindy, Dust y Claude Projects, pero su gap explotable "
                "esta en posicionarse como supervisor de ejecucion, no como otro agente aislado. Lindy tiene "
                "fuerza en automatizacion de workflows y experiencia simple, aunque su propuesta no enfatiza "
                "control local, mission replay ni evidencia operacional profunda. Dust es fuerte para equipos "
                "que quieren asistentes conectados a conocimiento e integraciones, pero se siente mas cercano "
                "a knowledge work empresarial que a convertir intencion en trabajo terminado. Claude Projects "
                "ofrece razonamiento y contexto excelentes, pero no es por si mismo una capa persistente de "
                "permisos, herramientas, memoria, costos y validacion. El espacio de Oli es construir confianza "
                "operacional: misiones con estado, permisos, evidencias, validacion y aprendizaje reutilizable. "
                "El wedge inicial debe probar una mision repetible y vendible antes de expandir herramientas."
            )
        return f"[development-model] {prompt}"


class FallbackModelAdapter:
    """Try a primary model, then fall back to development behavior.

    This keeps V0 usable when a free/remote provider is rate-limited or down,
    while preserving the error as metadata for evidence.
    """

    name = "fallback"

    def __init__(self, primary: ModelAdapter, fallback: ModelAdapter | None = None) -> None:
        self.primary = primary
        self.fallback = fallback or DevelopmentModelAdapter()
        self.last_provider_used: str | None = None
        self.last_error: str | None = None

    def complete(self, prompt: str) -> str:
        try:
            output = self.primary.complete(prompt)
            self.last_provider_used = getattr(self.primary, "name", self.primary.__class__.__name__)
            self.last_error = None
            return output
        except Exception as exc:
            self.last_error = str(exc)
            output = self.fallback.complete(prompt)
            self.last_provider_used = getattr(self.fallback, "name", self.fallback.__class__.__name__)
            return output


class OllamaModelAdapter:
    """Adapter for local Ollama once Alejandro has a local machine."""

    name = "ollama"

    def __init__(
        self,
        model: str = "qwen2.5:7b",
        host: str = "http://127.0.0.1:11434",
        timeout_seconds: int = 120,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def complete(self, prompt: str) -> str:
        payload = json.dumps(
            {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            }
        ).encode("utf-8")
        req = request.Request(
            f"{self.host}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=self.timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data.get("response", "")


class OpenAICompatibleModelAdapter:
    """Adapter for vLLM or rented GPU endpoints exposing chat/completions."""

    name = "openai_compatible"

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout_seconds: int = 120,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds

    def complete(self, prompt: str) -> str:
        payload = json.dumps(
            {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
        ).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                data = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"OpenAI-compatible provider returned HTTP {exc.code}: {detail}"
            ) from exc
        return data["choices"][0]["message"]["content"]


class WebhookModelAdapter:
    """Generic adapter for internal automation webhooks.

    The webhook must accept a JSON POST. Oli sends both `prompt` and `input`
    so simple n8n/automation flows can map either field. Common response
    shapes are supported: string, `response`, `text`, `output`, `content`, or
    OpenAI-like `choices[0].message.content`.
    """

    name = "webhook"

    def __init__(
        self,
        url: str,
        bearer_token: str | None = None,
        timeout_seconds: int = 120,
    ) -> None:
        self.url = url
        self.bearer_token = bearer_token
        self.timeout_seconds = timeout_seconds

    def complete(self, prompt: str) -> str:
        payload = json.dumps(
            {
                "prompt": prompt,
                "input": prompt,
                "source": "oli",
            }
        ).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"

        req = request.Request(
            self.url,
            data=payload,
            headers=headers,
            method="POST",
        )
        with request.urlopen(req, timeout=self.timeout_seconds) as response:
            raw = response.read().decode("utf-8")
        return _extract_webhook_text(raw)


def _extract_webhook_text(raw: str) -> str:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw

    if isinstance(data, str):
        return data

    if isinstance(data, list) and data:
        return _extract_webhook_text(json.dumps(data[0]))

    if not isinstance(data, dict):
        return str(data)

    for key in ("response", "text", "output", "content", "message"):
        value = data.get(key)
        if isinstance(value, str):
            return value

    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(first.get("text"), str):
                return first["text"]

    return json.dumps(data)


def get_default_model_adapter() -> ModelAdapter:
    """Select the runtime model without changing mission code.

    OLI_MODEL_PROVIDER values:
    - development: deterministic Codex-authored behavior for current V0 work
    - ollama: local Ollama, configured with OLI_OLLAMA_MODEL and OLLAMA_HOST
    - openai_compatible: vLLM/rented GPU endpoint
    - webhook: internal automation webhook that calls an LLM
    """

    if os.getenv("OLI_DISABLE_ENV_FILE") != "1":
        load_env_file()
    provider = os.getenv("OLI_MODEL_PROVIDER", "development").lower()

    if provider == "ollama":
        return FallbackModelAdapter(OllamaModelAdapter(
            model=os.getenv("OLI_OLLAMA_MODEL", "qwen2.5:7b"),
            host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"),
        ))

    if provider == "openai_compatible":
        base_url = os.getenv("OLI_OPENAI_COMPAT_BASE_URL")
        api_key = os.getenv("OLI_OPENAI_COMPAT_API_KEY")
        model = os.getenv("OLI_OPENAI_COMPAT_MODEL")
        if not base_url or not api_key or not model:
            raise RuntimeError(
                "openai_compatible provider requires "
                "OLI_OPENAI_COMPAT_BASE_URL, OLI_OPENAI_COMPAT_API_KEY and "
                "OLI_OPENAI_COMPAT_MODEL"
            )
        return FallbackModelAdapter(OpenAICompatibleModelAdapter(
            base_url=base_url,
            api_key=api_key,
            model=model,
        ))

    if provider == "webhook":
        url = os.getenv("OLI_WEBHOOK_MODEL_URL")
        if not url:
            raise RuntimeError("webhook provider requires OLI_WEBHOOK_MODEL_URL")
        return FallbackModelAdapter(WebhookModelAdapter(
            url=url,
            bearer_token=os.getenv("OLI_WEBHOOK_MODEL_BEARER_TOKEN"),
            timeout_seconds=int(os.getenv("OLI_WEBHOOK_MODEL_TIMEOUT_SECONDS", "120")),
        ))

    return DevelopmentModelAdapter()
