from botocore.exceptions import NoCredentialsError
from fastapi.testclient import TestClient

from backend.app import api

client = TestClient(api.app)


def test_aws_findings_endpoint_returns_real_scan_format(monkeypatch):
    sample = [
        {
            "id": "AWS-SSH-sg-demo123",
            "resource": "demo-web (sg-demo123)",
            "severity": "HIGH",
            "issue": "SSH may be publicly accessible over IPv4",
            "recommendation": "Restrict SSH access to trusted IP addresses.",
        }
    ]

    monkeypatch.setattr(api, "scan_security_groups", lambda: sample)

    response = client.get("/api/aws/findings")

    assert response.status_code == 200
    data = response.json()
    assert data["simulated"] is False
    assert data["count"] == 1
    assert data["findings"][0]["id"] == "AWS-SSH-sg-demo123"


def test_aws_findings_endpoint_handles_missing_credentials(monkeypatch):
    def fail_scan():
        raise NoCredentialsError()

    monkeypatch.setattr(api, "scan_security_groups", fail_scan)

    response = client.get("/api/aws/findings")

    assert response.status_code == 503
    assert "AWS scan unavailable" in response.json()["detail"]


def test_simulated_findings_endpoint_remains_available():
    response = client.get("/api/findings")

    assert response.status_code == 200
    assert response.json()["simulated"] is True
    assert len(response.json()["findings"]) == 3
