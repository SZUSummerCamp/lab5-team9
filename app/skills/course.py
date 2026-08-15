"""Course skill: answers questions about courses and schedules."""

from __future__ import annotations

from app.shared import SkillResult


def handle(message: str) -> SkillResult:
    # TODO: Hakim implements course lookup here.
    return SkillResult(skill_name="course", response="", status="ok", duration=0.0)
