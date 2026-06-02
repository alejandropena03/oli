from __future__ import annotations

from datetime import UTC, datetime
from enum import IntEnum, StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def now_utc() -> datetime:
    return datetime.now(UTC)


class PermissionClass(IntEnum):
    READ_DRAFT = 0
    INTERNAL_REVERSIBLE = 1
    RESOURCE_CONSUMING = 2
    EXTERNAL_BRAND_IMPACT = 3
    DESTRUCTIVE_SENSITIVE = 4


class MissionStatus(StrEnum):
    IDLE = "idle"
    LISTENING = "listening"
    INTAKE_RECEIVED = "intake_received"
    INTERPRETING_INTENT = "interpreting_intent"
    CLARIFYING = "clarifying"
    RETRIEVING_CONTEXT = "retrieving_context"
    CLASSIFYING_PERMISSIONS = "classifying_permissions"
    PLANNING = "planning"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    REPAIRING = "repairing"
    VALIDATING = "validating"
    DELIVERING = "delivering"
    GENERATING_REPORT = "generating_report"
    UPDATING_MEMORY = "updating_memory"
    COMPLETED = "completed"
    COMPLETED_PARTIAL = "completed_partial"  # ejecutada con conectores faltantes — no es un fallo
    BLOCKED = "blocked"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"
    QUEUED = "queued"


class MissionSource(StrEnum):
    CHAT = "chat"
    PLAYBOOK = "playbook"
    SCHEDULED = "scheduled"
    API = "api"


class StepStatus(StrEnum):
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class MissionEvent(BaseModel):
    from_status: MissionStatus | None
    to_status: MissionStatus
    trigger: str
    reason: str | None = None
    created_at: datetime = Field(default_factory=now_utc)


class InterpretedIntent(BaseModel):
    goal: str
    success_criteria: list[str]
    output_format: str
    scope: dict[str, list[str]]
    confidence: float = Field(ge=0, le=1)
    clarifications: list[dict[str, Any]] = Field(default_factory=list)


class MissionContext(BaseModel):
    user_preferences: dict[str, Any] = Field(default_factory=dict)
    company_context: dict[str, Any] = Field(default_factory=dict)
    similar_past_missions: list[dict[str, Any]] = Field(default_factory=list)
    applicable_playbooks: list[dict[str, Any]] = Field(default_factory=list)


class MissionStep(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    order: int = Field(gt=0)
    description: str
    executor: str
    required_tools: list[str] = Field(default_factory=list)
    connector_required: str | None = None  # nombre del conector externo si el paso lo necesita
    permission_class: PermissionClass = PermissionClass.READ_DRAFT
    reversible: bool = True
    estimated_duration_ms: int = Field(default=1000, gt=0)
    status: StepStatus = StepStatus.PENDING
    input: dict[str, Any] = Field(default_factory=dict)
    output: Any | None = None


class MissionPlan(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    version: int = 1
    steps: list[MissionStep]
    total_permission_class: PermissionClass
    estimates: dict[str, float]
    created_at: datetime = Field(default_factory=now_utc)


class EvidenceRef(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    kind: str
    title: str
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=now_utc)


class ValidationResult(BaseModel):
    passed: bool
    criteria_results: list[dict[str, Any]]
    score: float = Field(ge=0, le=1)
    auto_repair_possible: bool
    validated_at: datetime = Field(default_factory=now_utc)
    repair_cycle: int = 0


class CostRecord(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    model_cost_usd: float = 0
    tool_cost_usd: float = 0
    duration_ms: int = 0
    human_time_saved_hr: float = 0

    @property
    def total_cost_usd(self) -> float:
        return self.model_cost_usd + self.tool_cost_usd


class MissionReport(BaseModel):
    mission_id: UUID
    summary: str
    deliverable_description: str
    steps_completed: int
    steps_total: int
    validation_result: ValidationResult
    repair_cycles_used: int = 0
    cost: CostRecord
    playbook_candidate: bool
    playbook_candidate_reason: str | None = None
    generated_at: datetime = Field(default_factory=now_utc)


class Mission(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source: MissionSource
    status: MissionStatus
    raw_input: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=now_utc)
    interpreted_intent: InterpretedIntent | None = None
    context: MissionContext | None = None
    plan: MissionPlan | None = None
    permission_class: PermissionClass | None = None
    approval_records: list[dict[str, Any]] = Field(default_factory=list)
    current_step_index: int = 0
    validation_result: ValidationResult | None = None
    output: Any | None = None
    evidence: list[EvidenceRef] = Field(default_factory=list)
    report: MissionReport | None = None
    cost: CostRecord = Field(default_factory=CostRecord)
    block_reason: dict[str, Any] | None = None
    playbook_id: UUID | None = None
    events: list[MissionEvent] = Field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    archived_at: datetime | None = None

