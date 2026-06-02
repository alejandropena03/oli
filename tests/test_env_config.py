import os
from pathlib import Path
from uuid import uuid4

from packages.config import load_env_file


def test_load_env_file_sets_missing_values(monkeypatch):
    env_dir = Path("runtime/test-env")
    env_dir.mkdir(parents=True, exist_ok=True)
    env_file = env_dir / f".env.{uuid4()}.local"
    env_file.write_text('OLI_TEST_VALUE="ok"\n', encoding="utf-8")
    monkeypatch.delenv("OLI_TEST_VALUE", raising=False)

    load_env_file(env_file)

    assert os.environ["OLI_TEST_VALUE"] == "ok"


def test_load_env_file_does_not_override_by_default(monkeypatch):
    env_dir = Path("runtime/test-env")
    env_dir.mkdir(parents=True, exist_ok=True)
    env_file = env_dir / f".env.{uuid4()}.local"
    env_file.write_text('OLI_TEST_VALUE="from_file"\n', encoding="utf-8")
    monkeypatch.setenv("OLI_TEST_VALUE", "from_env")

    load_env_file(env_file)

    assert os.environ["OLI_TEST_VALUE"] == "from_env"
