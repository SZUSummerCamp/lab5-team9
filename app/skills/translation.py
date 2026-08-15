"""Translation skill: translates text requested by the user."""

from __future__ import annotations

import time

from app.llm.caller import call_llm
from app.shared import SkillResult


SYSTEM_PROMPT = (
    "You are a translation assistant. "
    "Translate the text provided by the user accurately. "
    "Reply with only the translated text and nothing else."
)


def handle(message: str) -> SkillResult:
    start = time.time()

    try:
        response = call_llm(SYSTEM_PROMPT, message)
        status = "success"
    except Exception as exc:  # noqa: BLE001 - surface any failure as a skill error
        response = f"The translation skill could not answer right now: {exc}"
        status = "error"

    return SkillResult(
        skill_name="translation",
        response=response,
        status=status,
        duration=time.time() - start,
    )
