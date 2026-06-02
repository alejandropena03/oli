from __future__ import annotations

from .mission_state import Mission, MissionEvent, MissionSource, MissionStatus, now_utc


class InvalidTransition(ValueError):
    pass


TERMINAL_STATUSES = {
    MissionStatus.COMPLETED,
    MissionStatus.COMPLETED_PARTIAL,
    MissionStatus.FAILED,
    MissionStatus.CANCELLED,
    MissionStatus.ARCHIVED,
}

ACTIVE_STATUSES = {
    MissionStatus.EXECUTING,
    MissionStatus.REPAIRING,
    MissionStatus.VALIDATING,
    MissionStatus.GENERATING_REPORT,
    MissionStatus.UPDATING_MEMORY,
}

HUMAN_INPUT_STATUSES = {
    MissionStatus.CLARIFYING,
    MissionStatus.AWAITING_APPROVAL,
    MissionStatus.BLOCKED,
}

ALLOWED_TRANSITIONS: dict[MissionStatus, set[MissionStatus]] = {
    MissionStatus.IDLE: {MissionStatus.LISTENING},
    MissionStatus.LISTENING: {MissionStatus.INTAKE_RECEIVED},
    MissionStatus.INTAKE_RECEIVED: {MissionStatus.INTERPRETING_INTENT},
    MissionStatus.INTERPRETING_INTENT: {
        MissionStatus.CLARIFYING,
        MissionStatus.RETRIEVING_CONTEXT,
        MissionStatus.FAILED,
    },
    MissionStatus.CLARIFYING: {
        MissionStatus.INTERPRETING_INTENT,
        MissionStatus.RETRIEVING_CONTEXT,
        MissionStatus.CANCELLED,
    },
    MissionStatus.RETRIEVING_CONTEXT: {MissionStatus.CLASSIFYING_PERMISSIONS},
    MissionStatus.CLASSIFYING_PERMISSIONS: {MissionStatus.PLANNING},
    MissionStatus.PLANNING: {
        MissionStatus.AWAITING_APPROVAL,
        MissionStatus.EXECUTING,
        MissionStatus.FAILED,
    },
    MissionStatus.AWAITING_APPROVAL: {MissionStatus.EXECUTING, MissionStatus.CANCELLED},
    MissionStatus.EXECUTING: {
        MissionStatus.VALIDATING,
        MissionStatus.REPAIRING,
        MissionStatus.BLOCKED,
        MissionStatus.FAILED,
    },
    MissionStatus.REPAIRING: {MissionStatus.EXECUTING, MissionStatus.BLOCKED},
    MissionStatus.VALIDATING: {
        MissionStatus.DELIVERING,
        MissionStatus.REPAIRING,
        MissionStatus.FAILED,
    },
    MissionStatus.DELIVERING: {MissionStatus.GENERATING_REPORT},
    MissionStatus.GENERATING_REPORT: {MissionStatus.UPDATING_MEMORY},
    MissionStatus.UPDATING_MEMORY: {MissionStatus.COMPLETED, MissionStatus.COMPLETED_PARTIAL},
    MissionStatus.COMPLETED: {MissionStatus.ARCHIVED},
    MissionStatus.COMPLETED_PARTIAL: {MissionStatus.ARCHIVED},
    MissionStatus.BLOCKED: {MissionStatus.EXECUTING, MissionStatus.CANCELLED},
    MissionStatus.FAILED: {MissionStatus.ARCHIVED},
    MissionStatus.CANCELLED: {MissionStatus.ARCHIVED},
    MissionStatus.QUEUED: {MissionStatus.INTAKE_RECEIVED, MissionStatus.CANCELLED},
    MissionStatus.ARCHIVED: set(),
}


def create_mission(raw_input: str, source: MissionSource = MissionSource.CHAT) -> Mission:
    mission = Mission(
        raw_input=raw_input,
        source=source,
        status=MissionStatus.INTAKE_RECEIVED,
    )
    mission.events.append(
        MissionEvent(
            from_status=None,
            to_status=MissionStatus.INTAKE_RECEIVED,
            trigger="create_mission",
            reason="raw input received",
        )
    )
    return mission


def transition(
    mission: Mission,
    target_status: MissionStatus,
    *,
    trigger: str = "auto",
    reason: str | None = None,
) -> Mission:
    if target_status in {MissionStatus.BLOCKED, MissionStatus.FAILED} and not reason:
        raise InvalidTransition(f"{target_status.value} requires a documented reason")

    allowed = ALLOWED_TRANSITIONS.get(mission.status, set())
    if target_status not in allowed:
        raise InvalidTransition(
            f"Cannot transition mission {mission.id} from "
            f"{mission.status.value} to {target_status.value}"
        )

    previous = mission.status
    mission.status = target_status
    mission.events.append(
        MissionEvent(
            from_status=previous,
            to_status=target_status,
            trigger=trigger,
            reason=reason,
        )
    )

    if target_status == MissionStatus.EXECUTING and mission.started_at is None:
        mission.started_at = now_utc()
    if target_status in {MissionStatus.COMPLETED, MissionStatus.COMPLETED_PARTIAL}:
        mission.completed_at = now_utc()
    if target_status == MissionStatus.ARCHIVED:
        mission.archived_at = now_utc()

    return mission


def is_terminal(mission: Mission) -> bool:
    return mission.status in TERMINAL_STATUSES


def is_active(mission: Mission) -> bool:
    return mission.status in ACTIVE_STATUSES


def needs_human_input(mission: Mission) -> bool:
    return mission.status in HUMAN_INPUT_STATUSES

