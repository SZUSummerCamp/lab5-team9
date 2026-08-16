"""Role-based access control for skills."""

from __future__ import annotations


DEFAULT_ROLE = "guest"

ROLE_SKILLS: dict[str, list[str]] = {
    "guest": ["campus"],
    "member": ["campus", "course", "library", "translation"],
    "admin": ["campus", "course", "library", "translation", "summary"],
}


def allowed_skills(role: str) -> list[str]:
    # Unknown roles fall back to the least privileged role.
    return list(ROLE_SKILLS.get(role, ROLE_SKILLS[DEFAULT_ROLE]))


def is_allowed(role: str, skill_name: str) -> bool:
    return skill_name in allowed_skills(role)
