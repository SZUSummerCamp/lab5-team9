"""Library skill: answers questions about library branches and services."""

from __future__ import annotations

from app.shared import SkillResult


def handle(message: str) -> SkillResult:
    # TODO: Hakim implements library lookup here.
    return SkillResult(skill_name="library", response="", status="ok", duration=0.0)
