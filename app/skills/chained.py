"""Chained skill: pipes one skill's answer into the next (knowledge -> summary -> translation)."""

from __future__ import annotations

import re
import time

from app.shared import SkillResult
from app.skills.campus import handle as campus_handle
from app.skills.course import handle as course_handle
from app.skills.library import handle as library_handle
from app.skills.summary import handle as summary_handle
from app.skills.translation import handle as translation_handle


CAMPUS_KEYWORDS = (
    "motto",
    "founded",
    "campus",
    "university",
    "establish",
    "president",
    "abbreviation",
)
LIBRARY_KEYWORDS = ("library", "book", "borrow", "branch", "reading room")
COURSE_KEYWORDS = ("course", "class", "subject", "program", "academic", "study")
SUMMARY_KEYWORDS = ("summarize", "summarise", "summary", "brief", "overview", "shorten")
TRANSLATION_KEYWORDS = ("translate", "translation", "in chinese", "in english", "翻译")

# Names used to describe the chain that actually ran, e.g. "campus→summary→translation".
SKILL_NAMES = {
    campus_handle: "campus",
    course_handle: "course",
    library_handle: "library",
    summary_handle: "summary",
    translation_handle: "translation",
}


def _matches(message: str, keywords: tuple[str, ...]) -> bool:
    lowered = message.lower()
    return any(keyword in lowered for keyword in keywords)


def detect_knowledge_skill(message: str):
    # Same precedence as the router: library, then course, then campus.
    if _matches(message, LIBRARY_KEYWORDS):
        return library_handle
    if _matches(message, COURSE_KEYWORDS):
        return course_handle
    return campus_handle


def detect_chain(message: str) -> list:
    knowledge_skill = detect_knowledge_skill(message)
    has_summary = _matches(message, SUMMARY_KEYWORDS)
    has_translation = _matches(message, TRANSLATION_KEYWORDS)
    has_knowledge = (
        _matches(message, CAMPUS_KEYWORDS)
        or _matches(message, LIBRARY_KEYWORDS)
        or _matches(message, COURSE_KEYWORDS)
    )

    if has_summary and has_translation:
        return [knowledge_skill, summary_handle, translation_handle]
    if has_summary:
        return [knowledge_skill, summary_handle]
    if has_translation and has_knowledge:
        return [knowledge_skill, translation_handle]
    return []


def handle(message: str) -> SkillResult:
    start = time.time()
    names: list[str] = []

    try:
        chain = detect_chain(message)
        if not chain:
            # Nothing to chain: answer the question with the knowledge skill alone.
            chain = [detect_knowledge_skill(message)]

        current_response = message
        for skill_handle in chain:
            if skill_handle is translation_handle:
                # Carry only the language cue forward so the rest of the request
                # is not mistaken for text to translate.
                lang_match = re.search(
                    r"in\s+(chinese|english|french|korean|japanese|spanish)", message.lower()
                )
                lang_cue = (
                    f"Translate into {lang_match.group(1)}"
                    if lang_match
                    else "Translate into Chinese"
                )
                input_message = f"{lang_cue}\n\nText to translate:\n{current_response}"
            else:
                input_message = current_response
            names.append(SKILL_NAMES[skill_handle])
            step_result = skill_handle(input_message)
            if step_result.status == "error":
                return SkillResult(
                    skill_name=step_result.skill_name,
                    response=step_result.response,
                    status="error",
                    duration=time.time() - start,
                )
            current_response = step_result.response

        return SkillResult(
            skill_name="→".join(names),
            response=current_response,
            status="success",
            duration=time.time() - start,
        )
    except Exception as exc:  # noqa: BLE001 - surface any failure as a skill error
        return SkillResult(
            skill_name="→".join(names) or "chained",
            response=f"The chained skill could not answer right now: {exc}",
            status="error",
            duration=time.time() - start,
        )
