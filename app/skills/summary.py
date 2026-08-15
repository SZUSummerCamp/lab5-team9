"""Summary skill: summarizes text supplied by the user."""

from __future__ import annotations

import time

from app.llm.caller import call_llm
from app.shared import SkillResult


SYSTEM_PROMPT = (
    "You are a summarization assistant. "
    "Summarize the text provided by the user into a concise, clear response. "
    "Reply with only the summary and nothing else."
)


def handle(message: str) -> SkillResult:
    start = time.time()

    try:
        response = call_llm(SYSTEM_PROMPT, message)
        status = "success"
    except Exception as exc:  # noqa: BLE001 - surface any failure as a skill error
        response = f"The summary skill could not answer right now: {exc}"
        status = "error"

    return SkillResult(
        skill_name="summary",
        response=response,
        status=status,
        duration=time.time() - start,
    )
