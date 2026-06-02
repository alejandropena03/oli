from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime, String, create_engine, delete, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.types import JSON

from packages.mission_kernel.mission_state import Mission


class Base(DeclarativeBase):
    pass


class MissionRecord(Base):
    __tablename__ = "missions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    status: Mapped[str] = mapped_column(String(64), index=True)
    goal: Mapped[str | None] = mapped_column(String(128), index=True, nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class SqlAlchemyMissionStore:
    def __init__(self, database_url: str = "sqlite:///runtime/oli-dev.db") -> None:
        connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
        self.engine: Engine = create_engine(database_url, connect_args=connect_args)
        self.session_factory = sessionmaker(self.engine, expire_on_commit=False)
        Base.metadata.create_all(self.engine)

    def save(self, mission: Mission) -> None:
        payload = mission.model_dump(mode="json")
        now = datetime.now(UTC)
        goal = mission.interpreted_intent.goal if mission.interpreted_intent else None
        with self._session() as session:
            record = session.get(MissionRecord, str(mission.id))
            if record is None:
                record = MissionRecord(
                    id=str(mission.id),
                    status=mission.status.value,
                    goal=goal,
                    payload=payload,
                    created_at=mission.created_at,
                    updated_at=now,
                )
                session.add(record)
            else:
                record.status = mission.status.value
                record.goal = goal
                record.payload = payload
                record.updated_at = now
            session.commit()

    def get(self, mission_id: UUID) -> Mission | None:
        with self._session() as session:
            record = session.get(MissionRecord, str(mission_id))
            if record is None:
                return None
            return Mission.model_validate(record.payload)

    def list(self) -> list[Mission]:
        with self._session() as session:
            records = session.scalars(select(MissionRecord).order_by(MissionRecord.created_at.desc())).all()
            return [Mission.model_validate(record.payload) for record in records]

    def clear(self) -> None:
        with self._session() as session:
            session.execute(delete(MissionRecord))
            session.commit()

    def _session(self) -> Session:
        return self.session_factory()
