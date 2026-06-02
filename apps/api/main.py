from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .models import router as models_router
from .missions import router as missions_router

app = FastAPI(title="Oli API", version="0.0.1")
app.include_router(missions_router)
app.include_router(models_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Oli V0</title>
        <style>
          :root {
            color-scheme: light;
            --ink: #1b1b1b;
            --muted: #626262;
            --line: #d8d8d8;
            --panel: #f7f6f3;
            --accent: #14532d;
            --accent-bg: #e6f4ea;
            --warn: #6b4e00;
          }

          * { box-sizing: border-box; }

          body {
            margin: 0;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: var(--ink);
            background: #ffffff;
            line-height: 1.45;
          }

          header {
            border-bottom: 1px solid var(--line);
            padding: 18px 28px;
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: center;
          }

          main {
            max-width: 1120px;
            margin: 0 auto;
            padding: 28px;
          }

          h1 {
            margin: 0;
            font-size: 22px;
            font-weight: 720;
            letter-spacing: 0;
          }

          h2 {
            margin: 0 0 12px;
            font-size: 16px;
            letter-spacing: 0;
          }

          p { margin: 0; color: var(--muted); }

          .status {
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
            color: var(--accent);
            background: var(--accent-bg);
            white-space: nowrap;
          }

          .layout {
            display: grid;
            grid-template-columns: minmax(280px, 360px) 1fr;
            gap: 22px;
            align-items: start;
          }

          section {
            border-top: 1px solid var(--line);
            padding-top: 18px;
          }

          .panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 16px;
          }

          label {
            display: block;
            font-size: 13px;
            font-weight: 650;
            margin-bottom: 8px;
          }

          textarea {
            width: 100%;
            min-height: 150px;
            resize: vertical;
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 11px;
            font: inherit;
            background: #fff;
          }

          button {
            width: 100%;
            min-height: 42px;
            margin-top: 12px;
            border: 0;
            border-radius: 6px;
            background: #1f1f1f;
            color: white;
            font-weight: 700;
            cursor: pointer;
          }

          button:disabled {
            cursor: wait;
            opacity: 0.65;
          }

          .result {
            display: grid;
            gap: 18px;
          }

          .empty {
            min-height: 280px;
            display: grid;
            place-items: center;
            text-align: center;
            color: var(--muted);
          }

          .meta {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
          }

          .metric {
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 10px;
            background: #fff;
          }

          .metric strong {
            display: block;
            font-size: 18px;
          }

          .metric span {
            color: var(--muted);
            font-size: 12px;
          }

          pre {
            white-space: pre-wrap;
            word-break: break-word;
            background: #fff;
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 12px;
            margin: 0;
            font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
            font-size: 13px;
          }

          ul {
            margin: 0;
            padding-left: 18px;
          }

          li { margin: 4px 0; }

          .error {
            color: #7f1d1d;
            background: #fee2e2;
            border: 1px solid #fecaca;
            border-radius: 6px;
            padding: 10px;
            margin-top: 12px;
            display: none;
          }

          @media (max-width: 820px) {
            header { align-items: flex-start; flex-direction: column; }
            main { padding: 18px; }
            .layout { grid-template-columns: 1fr; }
            .meta { grid-template-columns: 1fr; }
          }
        </style>
      </head>
      <body>
        <header>
          <div>
            <h1>Oli V0</h1>
            <p>Mission Kernel vivo: intencion -> plan -> permiso -> modelo -> ejecucion -> validacion -> reporte.</p>
          </div>
          <div class="status">research-brief-v1</div>
        </header>

        <main class="layout">
          <aside class="panel">
            <form id="mission-form">
              <label for="raw-input">Intencion clase 0: research brief</label>
              <textarea id="raw-input" name="raw_input">Investiga los 3 principales competidores de Oli y dame un brief de 1 pagina con sus fortalezas, debilidades y el gap que Oli puede explotar.</textarea>
              <button id="run-button" type="submit">Ejecutar research brief</button>
              <div id="error" class="error"></div>
            </form>
            <p style="margin-top:12px;font-size:13px;">Tambien existe una mision clase 3 en API: <code>POST /missions/draft-outreach</code>, que queda esperando aprobacion humana.</p>
            <p style="margin-top:8px;font-size:13px;">Modelo activo: <code>GET /models/status</code>. Smoke test: <code>POST /models/test</code>.</p>
          </aside>

          <section>
            <div id="empty" class="empty panel">
              <p>Ejecuta la primera mision para ver el brief, evidencia y reporte.</p>
            </div>

            <div id="result" class="result" hidden>
              <div class="meta">
                <div class="metric"><strong id="status">-</strong><span>Estado</span></div>
                <div class="metric"><strong id="steps">-</strong><span>Pasos</span></div>
                <div class="metric"><strong id="cost">-</strong><span>Costo simulado</span></div>
              </div>

              <div>
                <h2>Brief</h2>
                <pre id="brief"></pre>
              </div>

              <div>
                <h2>Reporte</h2>
                <pre id="report"></pre>
              </div>

              <div>
                <h2>Evidencia</h2>
                <ul id="evidence"></ul>
              </div>
            </div>
          </section>
        </main>

        <script>
          const form = document.getElementById("mission-form");
          const button = document.getElementById("run-button");
          const error = document.getElementById("error");
          const empty = document.getElementById("empty");
          const result = document.getElementById("result");

          form.addEventListener("submit", async (event) => {
            event.preventDefault();
            error.style.display = "none";
            button.disabled = true;
            button.textContent = "Ejecutando...";

            try {
              const rawInput = document.getElementById("raw-input").value;
              const response = await fetch("/missions/research-brief", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ raw_input: rawInput })
              });

              if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
              }

              const mission = await response.json();
              renderMission(mission);
            } catch (err) {
              error.textContent = `No se pudo ejecutar la mision: ${err.message}`;
              error.style.display = "block";
            } finally {
              button.disabled = false;
              button.textContent = "Ejecutar mision";
            }
          });

          function renderMission(mission) {
            empty.hidden = true;
            result.hidden = false;

            document.getElementById("status").textContent = mission.status;
            document.getElementById("steps").textContent = `${mission.report.steps_completed}/${mission.report.steps_total}`;
            document.getElementById("cost").textContent = `$${mission.cost.model_cost_usd.toFixed(2)}`;
            document.getElementById("brief").textContent = mission.output;
            document.getElementById("report").textContent = JSON.stringify({
              mission_id: mission.id,
              summary: mission.report.summary,
              validation_score: mission.validation_result.score,
              playbook_candidate: mission.report.playbook_candidate,
              playbook_reason: mission.report.playbook_candidate_reason
            }, null, 2);

            const evidence = document.getElementById("evidence");
            evidence.innerHTML = "";
            mission.evidence.forEach((item) => {
              const li = document.createElement("li");
              li.textContent = `${item.kind}: ${item.title}`;
              evidence.appendChild(li);
            });
          }
        </script>
      </body>
    </html>
    """
