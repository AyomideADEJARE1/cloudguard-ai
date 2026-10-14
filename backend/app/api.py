from botocore.exceptions import BotoCoreError, ClientError
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.aws_scanner import scan_security_groups
from backend.app.server import sample_findings

app = FastAPI(title="CloudGuard AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "CloudGuard AI API"}


@app.get("/api/findings")
def findings() -> dict:
    return {
        "environment": "Demo AWS environment",
        "simulated": True,
        "findings": sample_findings(),
    }


@app.get("/api/findings/{finding_id}")
def finding_detail(finding_id: str) -> dict:
    for finding in sample_findings():
        if finding["id"] == finding_id.upper():
            return finding

    return {"error": f"No finding found for {finding_id}"}


@app.get("/api/aws/findings")
def aws_findings() -> dict:
    try:
        findings = scan_security_groups()
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "AWS scan unavailable. Check AWS credentials, region, "
                "and read-only IAM permissions."
            ),
        ) from exc

    return {
        "environment": "AWS EC2 security groups",
        "simulated": False,
        "scan_type": "public_ssh_access",
        "count": len(findings),
        "findings": findings,
    }
