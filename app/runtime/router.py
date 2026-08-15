"""Routes an incoming message to the right skill."""

from __future__ import annotations

from app.shared import SkillResult


def route(message: str) -> SkillResult:
    # TODO: Hakim implements skill selection here.
    return SkillResult(skill_name="", response="", status="ok", duration=0.0)
