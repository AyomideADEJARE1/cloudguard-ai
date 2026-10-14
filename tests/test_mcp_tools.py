from backend.app.server import explain_finding, get_cloud_findings


def test_get_cloud_findings_returns_simulated_data():
    result = get_cloud_findings()

    assert result["simulated"] is True
    assert result["environment"] == "Demo AWS environment"
    assert len(result["findings"]) == 3


def test_get_cloud_findings_contains_expected_ids():
    result = get_cloud_findings()

    finding_ids = {finding["id"] for finding in result["findings"]}

    assert finding_ids == {"CG-001", "CG-002", "CG-003"}


def test_explain_finding_returns_remediation():
    result = explain_finding("CG-001")

    assert result["id"] == "CG-001"
    assert result["severity"] == "HIGH"
    assert result["recommendation"]
    assert "SSH" in result["issue"]


def test_explain_finding_is_case_insensitive():
    result = explain_finding("cg-001")

    assert result["id"] == "CG-001"


def test_explain_unknown_finding():
    result = explain_finding("CG-999")

    assert result == {"error": "No finding found for CG-999"}
