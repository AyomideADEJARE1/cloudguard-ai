from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "CloudGuard AI",
    stateless_http=True,
    json_response=True,
)


def sample_findings() -> list[dict]:
    """Return simulated security findings for the demo."""
    return [
        {
            "id": "CG-001",
            "resource": "demo-web-server",
            "severity": "HIGH",
            "issue": "SSH access is open to all IPv4 addresses",
            "recommendation": (
                "Restrict SSH access to trusted IP addresses "
                "or use AWS Systems Manager Session Manager."
            ),
        },
        {
            "id": "CG-002",
            "resource": "demo-storage",
            "severity": "MEDIUM",
            "issue": "Storage access settings need review",
            "recommendation": (
                "Review access policies and enable public-access "
                "blocking where appropriate."
            ),
        },
        {
            "id": "CG-003",
            "resource": "demo-database",
            "severity": "LOW",
            "issue": "Database monitoring needs review",
            "recommendation": ("Verify database logging and monitoring settings."),
        },
    ]


@mcp.tool()
def get_cloud_findings() -> dict:
    """Return simulated AWS cloud security findings for the demo."""
    return {
        "environment": "Demo AWS environment",
        "simulated": True,
        "findings": sample_findings(),
    }


@mcp.tool()
def explain_finding(finding_id: str) -> dict:
    """Explain a finding and recommend a remediation."""
    for finding in sample_findings():
        if finding["id"] == finding_id.upper():
            return finding

    return {"error": f"No finding found for {finding_id}"}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
