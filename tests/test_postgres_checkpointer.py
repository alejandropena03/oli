"""Tests for PostgresSaver checkpointer integration.

Split into two groups:
- Unit tests (no Postgres needed): run always, verify factory logic.
- Integration tests (Postgres required): skipped unless OLI_DATABASE_URL points
  to a live Postgres instance and OLI_MISSION_STORE=sqlalchemy.

Run integration tests on Mac personal with Docker Postgres:
    OLI_MISSION_STORE=sqlalchemy \\
    OLI_DATABASE_URL=postgresql+psycopg2://oli:oli@localhost:5432/oli \\
    python -m pytest tests/test_postgres_checkpointer.py -v
"""

from __future__ import annotations

import os
import uuid

import pytest

from packages.config.env import load_env_file

load_env_file()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _postgres_available() -> bool:
    return (
        os.environ.get("OLI_MISSION_STORE") == "sqlalchemy"
        and os.environ.get("OLI_DATABASE_URL", "").startswith("postgresql")
    )


requires_postgres = pytest.mark.skipif(
    not _postgres_available(),
    reason="Postgres not configured — set OLI_MISSION_STORE=sqlalchemy and OLI_DATABASE_URL",
)


# ---------------------------------------------------------------------------
# Unit tests — always run
# ---------------------------------------------------------------------------

class TestCheckpointerFactory:
    def test_returns_memory_saver_by_default(self, monkeypatch):
        monkeypatch.delenv("OLI_DATABASE_URL", raising=False)
        monkeypatch.setenv("OLI_MISSION_STORE", "json")

        from langgraph.checkpoint.memory import MemorySaver
        from packages.orchestrator.checkpointer import get_checkpointer

        checkpointer = get_checkpointer()
        assert isinstance(checkpointer, MemorySaver)

    def test_returns_memory_saver_when_store_is_json(self, monkeypatch):
        monkeypatch.setenv("OLI_MISSION_STORE", "json")
        monkeypatch.setenv("OLI_DATABASE_URL", "postgresql+psycopg2://oli:oli@localhost:5432/oli")

        from langgraph.checkpoint.memory import MemorySaver
        from packages.orchestrator.checkpointer import get_checkpointer

        checkpointer = get_checkpointer()
        assert isinstance(checkpointer, MemorySaver)

    def test_psycopg3_url_conversion(self):
        from packages.orchestrator.checkpointer import _to_psycopg3_url

        result = _to_psycopg3_url("postgresql+psycopg2://oli:oli@localhost:5432/oli")
        assert result == "postgresql://oli:oli@localhost:5432/oli"

    def test_psycopg3_url_conversion_passthrough(self):
        from packages.orchestrator.checkpointer import _to_psycopg3_url

        raw = "postgresql://oli:oli@localhost:5432/oli"
        assert _to_psycopg3_url(raw) == raw

    def test_graph_builds_without_postgres(self):
        """Graph topology must compile cleanly regardless of Postgres availability."""
        from packages.orchestrator.mission_graph import build_weekly_report_graph

        graph = build_weekly_report_graph(use_memory_checkpointer=False)
        assert graph is not None

    def test_graph_builds_with_memory_saver(self, monkeypatch):
        monkeypatch.setenv("OLI_MISSION_STORE", "json")
        monkeypatch.delenv("OLI_DATABASE_URL", raising=False)

        from packages.orchestrator.mission_graph import build_weekly_report_graph

        graph = build_weekly_report_graph(use_memory_checkpointer=True)
        assert graph is not None


# ---------------------------------------------------------------------------
# Integration tests — require live Postgres
# ---------------------------------------------------------------------------

@requires_postgres
class TestPostgresSaverIntegration:
    def test_checkpointer_returns_postgres_saver(self):
        from packages.orchestrator.checkpointer import get_checkpointer

        checkpointer = get_checkpointer()
        # PostgresSaver is not importable in envs without the package,
        # so we verify by duck-typing (has .put and .get methods)
        assert hasattr(checkpointer, "put")
        assert hasattr(checkpointer, "get")
        assert not isinstance(checkpointer, __import__("langgraph.checkpoint.memory", fromlist=["MemorySaver"]).MemorySaver)

    def test_mission_checkpoint_survives_graph_reinvocation(self):
        """A mission state saved by graph run 1 is retrievable in graph run 2.

        This proves durable checkpointing: missions survive server restarts.
        """
        from packages.orchestrator.mission_graph import build_weekly_report_graph
        from packages.orchestrator.checkpointer import get_checkpointer
        from packages.mission_kernel.mission_state import MissionStatus, MissionSource
        from packages.mission_kernel.state_machine import create_mission
        from packages.orchestrator.weekly_client_report import (
            DEFAULT_WEEKLY_REPORT_DATA,
            DEFAULT_WEEKLY_REPORT_INPUT,
        )

        thread_id = str(uuid.uuid4())
        checkpointer = get_checkpointer()

        # Run 1 — execute the mission to completion
        graph = build_weekly_report_graph(use_memory_checkpointer=True)
        mission = create_mission(raw_input=DEFAULT_WEEKLY_REPORT_INPUT, source=MissionSource.CHAT)
        initial_state = {
            "mission": mission,
            "performance_data": DEFAULT_WEEKLY_REPORT_DATA,
        }
        config = {"configurable": {"thread_id": thread_id}}
        result = graph.invoke(initial_state, config=config)

        assert result["mission"].status == MissionStatus.COMPLETED

        # Run 2 — retrieve the checkpoint from Postgres (simulates server restart)
        checkpoint = checkpointer.get(config)
        assert checkpoint is not None, "Checkpoint not found in Postgres after graph run"

        channel_values = checkpoint.get("channel_values", {})
        # PostgresSaver wraps bare dict state under __root__ key
        saved_state = channel_values.get("__root__", channel_values)
        assert "mission" in saved_state, "Mission not persisted in checkpoint"
        assert saved_state["mission"].status == MissionStatus.COMPLETED

    def test_different_threads_have_isolated_checkpoints(self):
        """Two missions with different thread_ids don't share state."""
        from packages.orchestrator.mission_graph import build_weekly_report_graph
        from packages.orchestrator.checkpointer import get_checkpointer
        from packages.mission_kernel.mission_state import MissionSource
        from packages.mission_kernel.state_machine import create_mission
        from packages.orchestrator.weekly_client_report import (
            DEFAULT_WEEKLY_REPORT_DATA,
            DEFAULT_WEEKLY_REPORT_INPUT,
        )

        thread_a = str(uuid.uuid4())
        thread_b = str(uuid.uuid4())
        checkpointer = get_checkpointer()

        graph = build_weekly_report_graph(use_memory_checkpointer=True)

        for thread_id in (thread_a, thread_b):
            mission = create_mission(raw_input=DEFAULT_WEEKLY_REPORT_INPUT, source=MissionSource.CHAT)
            graph.invoke(
                {"mission": mission, "performance_data": DEFAULT_WEEKLY_REPORT_DATA},
                config={"configurable": {"thread_id": thread_id}},
            )

        cp_a = checkpointer.get({"configurable": {"thread_id": thread_a}})
        cp_b = checkpointer.get({"configurable": {"thread_id": thread_b}})

        assert cp_a is not None
        assert cp_b is not None

        cv_a = cp_a["channel_values"]
        cv_b = cp_b["channel_values"]
        state_a = cv_a.get("__root__", cv_a)
        state_b = cv_b.get("__root__", cv_b)
        mission_a_id = state_a["mission"].id
        mission_b_id = state_b["mission"].id
        assert mission_a_id != mission_b_id, "Thread isolation broken — missions share state"

    def test_graph_builds_with_postgres_checkpointer(self):
        """Graph compilation succeeds with PostgresSaver injected."""
        from packages.orchestrator.mission_graph import build_weekly_report_graph

        # With Postgres env set, get_checkpointer() returns PostgresSaver
        graph = build_weekly_report_graph(use_memory_checkpointer=True)
        assert graph is not None
