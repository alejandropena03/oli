import pytest

from packages.mission_kernel import InvalidTransition, create_mission, transition
from packages.mission_kernel.mission_state import MissionStatus, PermissionClass
from packages.mission_kernel.policies import requires_approval
from packages.mission_kernel.state_machine import is_active, is_terminal, needs_human_input


def test_create_mission_starts_at_intake_received():
    mission = create_mission("Investiga competidores de Oli")

    assert mission.status == MissionStatus.INTAKE_RECEIVED
    assert mission.raw_input == "Investiga competidores de Oli"
    assert mission.events[0].to_status == MissionStatus.INTAKE_RECEIVED


def test_valid_transition_is_recorded():
    mission = create_mission("Investiga competidores de Oli")

    transition(mission, MissionStatus.INTERPRETING_INTENT, trigger="auto")

    assert mission.status == MissionStatus.INTERPRETING_INTENT
    assert mission.events[-1].from_status == MissionStatus.INTAKE_RECEIVED
    assert mission.events[-1].to_status == MissionStatus.INTERPRETING_INTENT


def test_invalid_transition_is_rejected():
    mission = create_mission("Investiga competidores de Oli")

    with pytest.raises(InvalidTransition):
        transition(mission, MissionStatus.COMPLETED)


def test_failed_and_blocked_require_reason():
    mission = create_mission("Investiga competidores de Oli")
    transition(mission, MissionStatus.INTERPRETING_INTENT)

    with pytest.raises(InvalidTransition):
        transition(mission, MissionStatus.FAILED)


def test_status_helpers_and_permission_policy():
    mission = create_mission("Investiga competidores de Oli")
    transition(mission, MissionStatus.INTERPRETING_INTENT)
    transition(mission, MissionStatus.RETRIEVING_CONTEXT)
    transition(mission, MissionStatus.CLASSIFYING_PERMISSIONS)
    transition(mission, MissionStatus.PLANNING)
    transition(mission, MissionStatus.EXECUTING)

    assert is_active(mission)
    assert not is_terminal(mission)
    assert not needs_human_input(mission)
    assert not requires_approval(PermissionClass.READ_DRAFT)
    assert requires_approval(PermissionClass.RESOURCE_CONSUMING)

