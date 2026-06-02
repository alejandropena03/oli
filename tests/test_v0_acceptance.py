from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.missions import clear_missions_for_tests


def test_v0_acceptance_contract():
    """V0 acceptance contract from tdd/README.md.

    V0 is accepted only if Oli can:
    - expose the FastAPI app,
    - execute slice-001 end-to-end in mock/development mode,
    - persist and retrieve the mission,
    - expose events/evidence/report,
    - stop external-impact work at an approval gate,
    - resume and complete that work after human approval.
    """

    clear_missions_for_tests()
    client = TestClient(app)

    assert client.get("/health").json() == {"status": "ok"}

    research = client.post(
        "/missions/research-brief",
        json={"raw_input": "Investiga los 3 principales competidores de Oli"},
    ).json()
    assert research["status"] == "completed"
    assert research["interpreted_intent"]["goal"] == "competitor_research_brief"
    assert research["validation_result"]["passed"] is True
    assert research["report"]["playbook_candidate"] is True

    research_id = research["id"]
    assert client.get(f"/missions/{research_id}").json()["id"] == research_id
    assert client.get(f"/missions/{research_id}/events").json()[-1]["to_status"] == "completed"
    assert len(client.get(f"/missions/{research_id}/evidence").json()) >= 5
    assert client.get(f"/missions/{research_id}/report").json()["mission_id"] == research_id

    weekly_report = client.post(
        "/missions/weekly-client-report",
        json={"raw_input": "Prepara reporte semanal para cliente de agencia"},
    ).json()
    assert weekly_report["status"] == "completed"
    assert weekly_report["interpreted_intent"]["goal"] == "weekly_client_report"
    assert weekly_report["report"]["playbook_candidate"] is True
    assert any(item["kind"] == "computed_metrics" for item in weekly_report["evidence"])

    outreach = client.post(
        "/missions/draft-outreach",
        json={"raw_input": "Prepara outreach para una agencia"},
    ).json()
    assert outreach["status"] == "awaiting_approval"
    assert outreach["permission_class"] == 3

    approved = client.post(
        f"/missions/{outreach['id']}/approve",
        json={"actor": "alejandro", "notes": "approved by V0 acceptance test"},
    ).json()
    assert approved["status"] == "completed"
    assert approved["approval_records"][0]["decision"] == "approved"
    assert any(item["kind"] == "approval" for item in approved["evidence"])
    assert any(item["kind"] == "simulated_external_action" for item in approved["evidence"])
