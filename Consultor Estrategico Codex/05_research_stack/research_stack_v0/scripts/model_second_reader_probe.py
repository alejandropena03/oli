from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from packages.config import load_env_file  # noqa: E402
from packages.orchestrator.model_adapter import get_default_model_adapter  # noqa: E402


OUT_DIR = Path(__file__).resolve().parents[1] / "probe_outputs"
OUT_PATH = OUT_DIR / "model_second_reader_2026-05-31.md"


PROMPT = """
Actua como segundo lector critico para Oli. No navegues: usa solo los hechos del prompt.

Contexto Oli:
- Oli propone Dedicated Runtime por usuario/equipo con app/API/CLI/Desktop Bridge, Mission Kernel, permisos, terminal/sandbox Linux, audit log, Postgres + pgvector, Model Router y Mission Black Box.
- SSH puede existir como setup/admin/power-user channel, pero no como bypass de permisos ni root shell para el LLM.
- Memoria Oli actual: user/company/mission memory; Postgres + pgvector; memory entries con confidence, source, status, reason, source missions, history, tags, expires_at; Mission Black Box; After Action Review; playbooks; user inspect/edit/delete/export.

State-of-the-art observado por research:
- Letta: core memory siempre visible + archival memory buscada on-demand + context hierarchy.
- Zep/Graphiti: temporal knowledge graph para conversaciones y business data cambiante.
- Mem0: memory layer con vector + graph memory, entity/relationship extraction.
- SOTA apunta a memoria jerarquica, temporal, con provenance, write-time reconciliation y evals.
- Remote/runtime SOTA: Claude Code Desktop/Remote, Cloudflare browser SSH, Tailscale/Zero Trust, Teleport session recording.
- Riesgos: terminal remoto y agentes de coding introducen RCE, exfiltracion de claves, approval bypass, prompt injection, SSRF y command execution risk.

Pregunta:
1. Valida si el modelo app PC + conexion terminal/SSH de Oli esta alineado con state of the art.
2. Valida si la memoria de Oli esta al nivel state of the art.
3. Da score 0-10, gaps, y decision ejecutiva.

Respuesta en español, compacta, con secciones:
Veredicto
Score runtime/SSH
Score memoria
Gaps criticos
Que construir primero
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    load_env_file(override=True)
    model = get_default_model_adapter()
    response = model.complete(PROMPT)
    OUT_PATH.write_text(
        f"# Model second reader probe\n\nFecha: {datetime.now(timezone.utc).isoformat()}\n\n{response}\n",
        encoding="utf-8",
    )
    print(response[:2000])
    print(OUT_PATH)


if __name__ == "__main__":
    main()

