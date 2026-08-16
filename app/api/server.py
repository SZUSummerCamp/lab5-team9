"""HTTP surface for CampusBot."""

from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.governance.audit import log
from app.governance.guardrail import check, explain
from app.governance.permissions import is_allowed
from app.runtime.router import route


WEB_ROOT = Path(__file__).resolve().parents[2] / "web"


class ChatRequest(BaseModel):
    user: str = "guest"
    role: str = "guest"
    message: str = Field(min_length=1, max_length=12000)


class ChatResponse(BaseModel):
    request_id: str
    user: str
    role: str
    skill: str
    status: str
    response: str
    duration_seconds: float


app = FastAPI(title="CampusBot", version="0.2.0")
app.mount("/static", StaticFiles(directory=WEB_ROOT), name="static")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(WEB_ROOT / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    request_id = str(uuid.uuid4())

    if not check(request.message):
        log(request.user, "blocked", "blocked", 0.0)
        raise HTTPException(status_code=400, detail=explain())

    result = route(request.message)

    # An unmatched message never reached a skill, so there is nothing to authorize.
    if result.skill_name != "unknown" and not is_allowed(request.role, result.skill_name):
        log(request.user, result.skill_name, "forbidden", result.duration)
        raise HTTPException(
            status_code=403,
            detail="Your role does not have access to this skill.",
        )

    log(request.user, result.skill_name, result.status, result.duration)

    return ChatResponse(
        request_id=request_id,
        user=request.user,
        role=request.role,
        skill=result.skill_name,
        status=result.status,
        response=result.response,
        duration_seconds=round(result.duration, 3),
    )
