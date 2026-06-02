from pathlib import Path
from uuid import uuid4

from packages.mission_kernel import create_mission
from packages.mission_store import JsonMissionStore, SqlAlchemyMissionStore, get_mission_store


def test_json_mission_store_round_trips_mission():
    test_dir = Path("runtime/test-missions")
    test_dir.mkdir(parents=True, exist_ok=True)
    store = JsonMissionStore(test_dir / f"missions-{uuid4()}.json")
    mission = create_mission("Investiga competidores de Oli")

    store.save(mission)
    loaded = store.get(mission.id)

    assert loaded is not None
    assert loaded.id == mission.id
    assert loaded.raw_input == mission.raw_input


def test_sqlalchemy_mission_store_round_trips_mission():
    test_dir = Path("runtime/test-missions")
    test_dir.mkdir(parents=True, exist_ok=True)
    store = SqlAlchemyMissionStore(f"sqlite:///{test_dir / f'missions-{uuid4()}.db'}")
    mission = create_mission("Persist this mission")

    store.save(mission)
    loaded = store.get(mission.id)

    assert loaded is not None
    assert loaded.id == mission.id
    assert loaded.raw_input == mission.raw_input
    assert store.list()[0].id == mission.id

    store.clear()
    assert store.list() == []


def test_mission_store_factory_selects_sqlalchemy():
    test_dir = Path("runtime/test-missions")
    test_dir.mkdir(parents=True, exist_ok=True)
    store = get_mission_store(
        {
            "OLI_MISSION_STORE": "sqlalchemy",
            "OLI_DATABASE_URL": f"sqlite:///{test_dir / f'factory-{uuid4()}.db'}",
        }
    )

    assert isinstance(store, SqlAlchemyMissionStore)
