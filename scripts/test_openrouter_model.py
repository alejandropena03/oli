from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from packages.config import load_env_file
from packages.orchestrator.model_adapter import get_default_model_adapter


def main() -> None:
    load_env_file(override=True)
    model = get_default_model_adapter()
    try:
        response = model.complete("Responde exactamente con: oli_openrouter_ok")
    except Exception as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1) from exc
    print(response[:1000])


if __name__ == "__main__":
    main()
