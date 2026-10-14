from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
