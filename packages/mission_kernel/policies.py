from __future__ import annotations

from .mission_state import MissionPlan, MissionStep, PermissionClass


APPROVAL_THRESHOLD = PermissionClass.RESOURCE_CONSUMING


def max_permission_class(steps: list[MissionStep]) -> PermissionClass:
    if not steps:
        return PermissionClass.READ_DRAFT
    return max(step.permission_class for step in steps)


def requires_approval(permission_class: PermissionClass | int) -> bool:
    return PermissionClass(permission_class) >= APPROVAL_THRESHOLD


def plan_requires_approval(plan: MissionPlan) -> bool:
    return requires_approval(plan.total_permission_class)

