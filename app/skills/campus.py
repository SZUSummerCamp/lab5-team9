"""Campus skill: answers general questions about the university."""

from __future__ import annotations

from app.shared import SkillResult


def handle(message: str) -> SkillResult:
    # TODO: Hakim implements campus lookup here.
    return SkillResult(skill_name="campus", response="", status="ok", duration=0.0)
