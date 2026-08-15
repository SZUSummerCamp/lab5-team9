"""Shared data structures used across skills, runtime, and governance."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SkillResult:
    skill_name: str
    response: str
    status: str
    duration: float
