from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.missions import clear_missions_for_tests


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_status_endpoint():
    client = TestClient(app)

    response = client.get("/models/status")

    assert response.status_code == 200
    assert response.json()["provider"] == "development"


def test_root_endpoint_explains_v0():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "Oli V0" in response.text
    assert "Ejecutar mision" in response.text
    assert "/missions/research-brief" in response.text


def test_create_and_get_research_brief_mission():
    clear_missions_for_tests()
    client = TestClient(app)

    create_response = client.post(
        "/missions/research-brief",
        json={"raw_input": "Investiga competidores de Oli"},
    )

    assert create_response.status_code == 200
    created = create_response.json()
    assert created["status"] in {"completed", "failed"}  # LLM-first: resultado depende del modelo
    assert created["interpreted_intent"] is not None
    assert created["interpreted_intent"]["goal"] != ""
    assert created["plan"] is not None

    get_response = client.get(f"/missions/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]

    list_response = client.get("/missions")
    assert list_response.status_code == 200
    assert list_response.json()[0]["id"] == created["id"]

    events_response = client.get(f"/missions/{created['id']}/events")
    assert events_response.status_code == 200
    assert events_response.json()[-1]["to_status"] in {"completed", "failed"}

    evidence_response = client.get(f"/missions/{created['id']}/evidence")
    assert evidence_response.status_code == 200
    assert any(item["kind"] == "validation" for item in evidence_response.json())

    # El reporte solo existe si completó — si falló, el endpoint devuelve null
    if created["status"] == "completed":
        report_response = client.get(f"/missions/{created['id']}/report")
        assert report_response.status_code == 200
        assert report_response.json()["mission_id"] == created["id"]


def test_draft_outreach_requires_approval_before_external_impact():
    clear_missions_for_tests()
    client = TestClient(app)

    create_response = client.post(
        "/missions/draft-outreach",
        json={"raw_input": "Prepara outreach para una agencia"},
    )

    assert create_response.status_code == 200
    mission = create_response.json()
    assert mission["status"] == "awaiting_approval"
    assert mission["permission_class"] == 3
    assert mission["approval_records"] == []

    approve_response = client.post(
        f"/missions/{mission['id']}/approve",
        json={"actor": "alejandro", "notes": "ok para ejecutar"},
    )

    assert approve_response.status_code == 200
    approved = approve_response.json()
    assert approved["status"] == "completed"
    assert approved["approval_records"][0]["decision"] == "approved"
    assert approved["report"]["playbook_candidate"] is True


def test_create_weekly_client_report_for_agency_team():
    clear_missions_for_tests()
    client = TestClient(app)

    response = client.post(
        "/missions/weekly-client-report",
        json={"raw_input": "Prepara reporte semanal para cliente de agencia"},
    )

    assert response.status_code == 200
    mission = response.json()
    assert mission["status"] == "completed"
    assert mission["interpreted_intent"]["goal"] == "weekly_client_report"
    assert mission["validation_result"]["passed"] is True
    assert mission["report"]["playbook_candidate"] is True
    assert "Reporte semanal" in mission["output"]


def test_approval_rejected_when_mission_is_not_waiting_for_approval():
    clear_missions_for_tests()
    client = TestClient(app)
    mission = client.post("/missions/research-brief", json={"raw_input": "Investiga Oli"}).json()

    response = client.post(
        f"/missions/{mission['id']}/approve",
        json={"actor": "alejandro"},
    )

    assert response.status_code == 409
