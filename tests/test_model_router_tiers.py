import pytest

from packages.model_router import ModelRouter, ModelRole, PrivacyMode, RoutingTier, TaskType


def test_model_router_selects_fast_local_role_for_tier_1_when_gpu_available():
    decision = ModelRouter(gpu_available=True).decide(TaskType.INTENT_INTERPRETATION)

    assert decision.tier == RoutingTier.TIER_1_FAST_LOCAL
    assert decision.role == ModelRole.FAST_LOCAL
    assert decision.provider == "ollama"
    assert decision.requires_gpu is True
    assert decision.external_api_allowed is False


def test_model_router_selects_main_local_role_for_tier_2_when_gpu_available():
    decision = ModelRouter(gpu_available=True).decide(TaskType.REPORT_GENERATION)

    assert decision.tier == RoutingTier.TIER_2_MAIN_LOCAL
    assert decision.role == ModelRole.MAIN_LOCAL
    assert decision.provider == "ollama"


def test_model_router_uses_frontier_api_for_tier_3_in_hybrid_mode():
    decision = ModelRouter(provider="openai_compatible").decide(TaskType.CRITICAL_DECISION_SUPPORT)

    assert decision.tier == RoutingTier.TIER_3_FRONTIER_API
    assert decision.role == ModelRole.PREMIUM_REASONING
    assert decision.provider == "openai_compatible"
    assert decision.external_api_allowed is True


def test_model_router_blocks_tier_3_when_privacy_is_local_only_without_gpu():
    router = ModelRouter(privacy_mode=PrivacyMode.LOCAL_ONLY)

    decision = router.decide(TaskType.COMPLEX_ARCHITECTURE)

    assert decision.tier == RoutingTier.BLOCKED
    assert decision.external_api_allowed is False
    with pytest.raises(RuntimeError):
        router.get_adapter(TaskType.COMPLEX_ARCHITECTURE)
