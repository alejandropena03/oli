from __future__ import annotations

import os
from typing import Union

from langgraph.checkpoint.memory import MemorySaver


def get_checkpointer() -> Union[MemorySaver, object]:
    """Return PostgresSaver if OLI_DATABASE_URL is set, MemorySaver otherwise.

    PostgresSaver is imported lazily so the module loads without psycopg installed
    in environments that only use MemorySaver (e.g. CI without Postgres).
    """
    db_url = os.environ.get("OLI_DATABASE_URL", "")
    store = os.environ.get("OLI_MISSION_STORE", "json")

    if store == "sqlalchemy" and db_url.startswith("postgresql"):
        return _build_postgres_saver(db_url)

    return MemorySaver()


def _build_postgres_saver(db_url: str) -> object:
    try:
        from langgraph.checkpoint.postgres import PostgresSaver  # type: ignore
        import psycopg  # type: ignore

        # PostgresSaver requires a psycopg3 connection string (postgresql://)
        # SQLAlchemy uses postgresql+psycopg2:// — normalize for psycopg3
        conn_string = _to_psycopg3_url(db_url)
        conn = psycopg.connect(conn_string, autocommit=True)
        saver = PostgresSaver(conn)
        saver.setup()
        return saver
    except ImportError as e:
        raise RuntimeError(
            "PostgresSaver requires 'langgraph-checkpoint-postgres' and 'psycopg'. "
            "Install with: pip install langgraph-checkpoint-postgres psycopg[binary]\n"
            f"Original error: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"Failed to connect PostgresSaver to '{db_url}': {e}\n"
            "Check that Postgres is running and OLI_DATABASE_URL is correct."
        ) from e


def _to_psycopg3_url(db_url: str) -> str:
    """Convert SQLAlchemy-style URL to psycopg3-compatible URL.

    postgresql+psycopg2://user:pass@host:port/db
    → postgresql://user:pass@host:port/db
    """
    return db_url.replace("postgresql+psycopg2://", "postgresql://").replace(
        "postgresql+psycopg://", "postgresql://"
    )
