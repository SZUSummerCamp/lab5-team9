"""Summary skill: summarizes text supplied by the user."""

from __future__ import annotations

from app.shared import SkillResult


def handle(message: str) -> SkillResult:
    # TODO: Hakim implements summarization here.
    return SkillResult(skill_name="summary", response="", status="ok", duration=0.0)
