from __future__ import annotations

import os

from packages.config import load_env_file

from .json_store import JsonMissionStore
from .sqlalchemy_store import SqlAlchemyMissionStore


def get_mission_store(env: dict[str, str] | None = None):
    if env is None:
        load_env_file()
        env = dict(os.environ)

    store_kind = env.get("OLI_MISSION_STORE", "json").lower()
    if store_kind == "sqlalchemy":
        return SqlAlchemyMissionStore(env.get("OLI_DATABASE_URL", "sqlite:///runtime/oli-dev.db"))
    if store_kind == "json":
        return JsonMissionStore(env.get("OLI_MISSION_STORE_PATH", "runtime/missions.json"))
    raise ValueError(f"Unsupported OLI_MISSION_STORE: {store_kind}")
