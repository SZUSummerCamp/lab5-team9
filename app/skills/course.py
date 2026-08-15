"""Course skill: answers questions about courses and schedules."""

from __future__ import annotations

import json
import time
from pathlib import Path

from app.llm.caller import call_llm
from app.shared import SkillResult


KNOWLEDGE_PATH = Path(__file__).resolve().parents[2] / "knowledge.json"

SYSTEM_PROMPT = (
    "You are the course assistant for Shenzhen University. "
    "Answer questions about university courses, subjects, and academic programs. "
    "Use only the knowledge context provided in the user message. "
    "Never invent, guess, or add facts that are not in that context. "
    'If the answer is not in the context, reply exactly: "That information is not available." '
    "Keep answers short and factual."
)


def handle(message: str) -> SkillResult:
    start = time.time()

    knowledge = json.loads(KNOWLEDGE_PATH.read_text(encoding="utf-8"))
    user_message = (
        f"Knowledge context:\n{json.dumps(knowledge, ensure_ascii=False, indent=2)}\n\n"
        f"User question:\n{message}"
    )

    try:
        response = call_llm(SYSTEM_PROMPT, user_message)
        status = "success"
    except Exception as exc:  # noqa: BLE001 - surface any failure as a skill error
        response = f"The course skill could not answer right now: {exc}"
        status = "error"

    return SkillResult(
        skill_name="course",
        response=response,
        status=status,
        duration=time.time() - start,
    )
