from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID

from packages.mission_kernel.mission_state import Mission


class JsonMissionStore:
    """Tiny durable store for V0.

    This is intentionally boring: one JSON file, no database server, enough to
    keep API-created missions available across process restarts while V0 is
    still proving the mission lifecycle.
    """

    def __init__(self, path: Path | str = "runtime/missions.json") -> None:
        self.path = Path(path)

    def save(self, mission: Mission) -> None:
        missions = self._read_all()
        missions[str(mission.id)] = mission.model_dump(mode="json")
        self._write_all(missions)

    def get(self, mission_id: UUID) -> Mission | None:
        raw = self._read_all().get(str(mission_id))
        if raw is None:
            return None
        return Mission.model_validate(raw)

    def list(self) -> list[Mission]:
        return [
            Mission.model_validate(raw)
            for raw in self._read_all().values()
        ]

    def clear(self) -> None:
        self._write_all({})

    def _read_all(self) -> dict[str, dict]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write_all(self, missions: dict[str, dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(missions, indent=2), encoding="utf-8")
