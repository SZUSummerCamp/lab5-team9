"""Translation skill: translates text requested by the user."""

from __future__ import annotations

from app.shared import SkillResult


def handle(message: str) -> SkillResult:
    # TODO: Hakim implements translation here.
    return SkillResult(skill_name="translation", response="", status="ok", duration=0.0)
