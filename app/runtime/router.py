"""Routes an incoming message to the right skill."""

from __future__ import annotations

from app.shared import SkillResult
from app.skills.campus import handle as campus_handle
from app.skills.chained import handle as chained_handle
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
TRANSLATION_KEYWORDS = ("translate", "translation", "in chinese", "in english", "翻译")
SUMMARY_KEYWORDS = ("summarize", "summary", "brief", "overview", "shorten")

# Checked in order: the first skill with a keyword hit wins.
ROUTES = (
    (TRANSLATION_KEYWORDS, translation_handle),
    (SUMMARY_KEYWORDS, summary_handle),
    (LIBRARY_KEYWORDS, library_handle),
    (COURSE_KEYWORDS, course_handle),
    (CAMPUS_KEYWORDS, campus_handle),
)

KNOWLEDGE_KEYWORDS = CAMPUS_KEYWORDS + LIBRARY_KEYWORDS + COURSE_KEYWORDS
CHAIN_KEYWORDS = SUMMARY_KEYWORDS + TRANSLATION_KEYWORDS

UNMATCHED_RESPONSE = (
    "I'm sorry, I can't help with that. Please ask about Shenzhen University "
    "campus, courses, library, or request a translation."
)


def route(message: str) -> SkillResult:
    lowered = message.lower()

    # A knowledge question that also asks for a summary or a translation needs
    # more than one skill, so hand the whole message to the chain.
    has_knowledge = any(keyword in lowered for keyword in KNOWLEDGE_KEYWORDS)
    has_chain = any(keyword in lowered for keyword in CHAIN_KEYWORDS)
    if has_knowledge and has_chain:
        return chained_handle(message)

    for keywords, handle in ROUTES:
        if any(keyword in lowered for keyword in keywords):
            return handle(message)

    return SkillResult(
        skill_name="unknown",
        response=UNMATCHED_RESPONSE,
        status="unmatched",
        duration=0.0,
    )
