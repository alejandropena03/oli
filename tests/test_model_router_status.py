from packages.model_router import get_model_status, test_model as run_model_test
from packages.model_router.status import ModelTestResult


def test_model_status_defaults_to_development():
    status = get_model_status({})

    assert status.provider == "development"
    assert status.configured
    assert status.effective_adapter == "DevelopmentModelAdapter"


def test_model_status_reports_openai_compatible_configuration():
    status = get_model_status(
        {
            "OLI_MODEL_PROVIDER": "openai_compatible",
            "OLI_OPENAI_COMPAT_BASE_URL": "https://openrouter.ai/api/v1",
            "OLI_OPENAI_COMPAT_MODEL": "openrouter/owl-alpha",
            "OLI_OPENAI_COMPAT_API_KEY": "secret",
        }
    )

    assert status.provider == "openai_compatible"
    assert status.configured
    assert status.key_present
    assert status.model == "openrouter/owl-alpha"


class GoodModel:
    name = "good"

    def complete(self, prompt: str) -> str:
        return "oli_model_ok"


def test_model_test_result_for_good_model():
    result = run_model_test(GoodModel())

    assert isinstance(result, ModelTestResult)
    assert result.ok
    assert result.provider_used == "good"
