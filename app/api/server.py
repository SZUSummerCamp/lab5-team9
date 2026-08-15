"""HTTP surface for CampusBot."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CampusBot", version="0.1.0")


class ChatRequest(BaseModel):
    message: str
    user: str


@app.post("/chat")
def chat(request: ChatRequest) -> dict:
    # TODO: Hakim checks the guardrail (app.governance.guardrail.check).
    # TODO: Hakim routes the message (app.runtime.router.route).
    # TODO: Hakim checks permissions for the chosen skill (app.governance.permissions.is_allowed).
    # TODO: Hakim writes the audit entry (app.governance.audit.log).
    # TODO: Hakim returns the skill response.
    return {}
