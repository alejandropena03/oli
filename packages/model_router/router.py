from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from packages.orchestrator.model_adapter import ModelAdapter


class TaskType(StrEnum):
    INTENT_INTERPRETATION = "intent_interpretation"
    PERMISSION_CLASSIFICATION = "permission_classification"
    MEMORY_QUERY_GENERATION = "memory_query_generation"
    STEP_ROUTING = "step_routing"
    BASIC_VALIDATION = "basic_validation"
    PLAN_CREATION = "plan_creation"
    SYNTHESIS = "synthesis"
    REPORT_GENERATION = "report_generation"
    DRAFT_WRITING = "draft_writing"
    COMPLEX_ARCHITECTURE = "complex_architecture"
    DEEP_CODE_ANALYSIS = "deep_code_analysis"
    CRITICAL_DECISION_SUPPORT = "critical_decision_support"


class ModelRole(StrEnum):
    FAST_LOCAL = "fast_local"
    MAIN_LOCAL = "main_local"
    PREMIUM_REASONING = "premium_reasoning"
    PREMIUM_CODING = "premium_coding"


class PrivacyMode(StrEnum):
    LOCAL_ONLY = "local_only"
    HYBRID = "hybrid"
    CLOUD_OK = "cloud_ok"


class RoutingTier(StrEnum):
    TIER_1_FAST_LOCAL = "tier_1_fast_local"
    TIER_2_MAIN_LOCAL = "tier_2_main_local"
    TIER_3_FRONTIER_API = "tier_3_frontier_api"
    DEVELOPMENT_FALLBACK = "development_fallback"
    BLOCKED = "blocked"


class RoutingDecision(BaseModel):
    task_type: TaskType
    tier: RoutingTier
    role: ModelRole | None
    provider: str
    reason: str
    requires_gpu: bool
    external_api_allowed: bool


TIER_1_TASKS = {
    TaskType.INTENT_INTERPRETATION,
    TaskType.PERMISSION_CLASSIFICATION,
    TaskType.MEMORY_QUERY_GENERATION,
    TaskType.STEP_ROUTING,
    TaskType.BASIC_VALIDATION,
}

TIER_2_TASKS = {
    TaskType.PLAN_CREATION,
    TaskType.SYNTHESIS,
    TaskType.REPORT_GENERATION,
    TaskType.DRAFT_WRITING,
}

TIER_3_TASKS = {
    TaskType.COMPLEX_ARCHITECTURE,
    TaskType.DEEP_CODE_ANALYSIS,
    TaskType.CRITICAL_DECISION_SUPPORT,
}


class ModelRouter:
    def __init__(
        self,
        *,
        gpu_available: bool = False,
        privacy_mode: PrivacyMode = PrivacyMode.HYBRID,
        provider: str = "development",
    ) -> None:
        self.gpu_available = gpu_available
        self.privacy_mode = privacy_mode
        self.provider = provider

    def decide(self, task_type: TaskType) -> RoutingDecision:
        if task_type in TIER_1_TASKS:
            if self.gpu_available:
                return RoutingDecision(
                    task_type=task_type,
                    tier=RoutingTier.TIER_1_FAST_LOCAL,
                    role=ModelRole.FAST_LOCAL,
                    provider="ollama",
                    reason="Tier 1 task should use the fastest local model when GPU is available.",
                    requires_gpu=True,
                    external_api_allowed=False,
                )
            return self._development_or_cloud(
                task_type,
                role=ModelRole.FAST_LOCAL,
                reason="Tier 1 task has no local GPU yet; use configured development/API adapter.",
            )

        if task_type in TIER_2_TASKS:
            if self.gpu_available:
                return RoutingDecision(
                    task_type=task_type,
                    tier=RoutingTier.TIER_2_MAIN_LOCAL,
                    role=ModelRole.MAIN_LOCAL,
                    provider="ollama",
                    reason="Tier 2 task should use the main local model when GPU is available.",
                    requires_gpu=True,
                    external_api_allowed=False,
                )
            return self._development_or_cloud(
                task_type,
                role=ModelRole.MAIN_LOCAL,
                reason="Tier 2 task has no local GPU yet; use configured development/API adapter.",
            )

        if self.privacy_mode == PrivacyMode.LOCAL_ONLY:
            return RoutingDecision(
                task_type=task_type,
                tier=RoutingTier.BLOCKED,
                role=ModelRole.PREMIUM_REASONING,
                provider="none",
                reason="Tier 3 task needs frontier quality, but privacy mode is local_only and no GPU is available.",
                requires_gpu=False,
                external_api_allowed=False,
            )

        role = (
            ModelRole.PREMIUM_CODING
            if task_type == TaskType.DEEP_CODE_ANALYSIS
            else ModelRole.PREMIUM_REASONING
        )
        return RoutingDecision(
            task_type=task_type,
            tier=RoutingTier.TIER_3_FRONTIER_API,
            role=role,
            provider=self.provider,
            reason="Tier 3 task should use a frontier API until benchmarked local GPU models are available.",
            requires_gpu=False,
            external_api_allowed=True,
        )

    def get_adapter(self, task_type: TaskType) -> tuple["ModelAdapter", RoutingDecision]:
        decision = self.decide(task_type)
        if decision.tier == RoutingTier.BLOCKED:
            raise RuntimeError(decision.reason)
        from packages.orchestrator.model_adapter import get_default_model_adapter

        return get_default_model_adapter(), decision

    def _development_or_cloud(
        self,
        task_type: TaskType,
        *,
        role: ModelRole,
        reason: str,
    ) -> RoutingDecision:
        if self.privacy_mode == PrivacyMode.LOCAL_ONLY:
            return RoutingDecision(
                task_type=task_type,
                tier=RoutingTier.DEVELOPMENT_FALLBACK,
                role=role,
                provider="development",
                reason="Local-only mode without GPU uses deterministic development adapter only.",
                requires_gpu=False,
                external_api_allowed=False,
            )
        return RoutingDecision(
            task_type=task_type,
            tier=RoutingTier.DEVELOPMENT_FALLBACK,
            role=role,
            provider=self.provider,
            reason=reason,
            requires_gpu=False,
            external_api_allowed=self.provider != "development",
        )
