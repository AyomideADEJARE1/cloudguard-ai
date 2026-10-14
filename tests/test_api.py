from fastapi.testclient import TestClient

from backend.app.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "CloudGuard AI API"


def test_findings_endpoint_returns_simulated_findings():
    response = client.get("/api/findings")

    assert response.status_code == 200
    data = response.json()

    assert data["simulated"] is True
    assert len(data["findings"]) == 3
    assert {item["id"] for item in data["findings"]} == {"CG-001", "CG-002", "CG-003"}


def test_findings_have_required_fields():
    response = client.get("/api/findings")
    findings = response.json()["findings"]
    required = {"id", "resource", "severity", "issue", "recommendation"}

    for finding in findings:
        assert required.issubset(finding)
        assert finding["severity"] in {"HIGH", "MEDIUM", "LOW"}


def test_get_finding_by_id():
    response = client.get("/api/findings/CG-001")

    assert response.status_code == 200
    assert response.json()["id"] == "CG-001"
    assert response.json()["severity"] == "HIGH"


def test_finding_lookup_is_case_insensitive():
    response = client.get("/api/findings/cg-001")

    assert response.status_code == 200
    assert response.json()["id"] == "CG-001"


def test_unknown_finding_id():
    response = client.get("/api/findings/CG-999")

    assert response.status_code == 200
    assert response.json() == {"error": "No finding found for CG-999"}
