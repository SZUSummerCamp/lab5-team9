"""Input guardrail: decides whether a message is safe to handle."""

from __future__ import annotations


BLOCKED_PHRASES = [
    "ignore previous instructions",
    "ignore all instructions",
    "disregard your instructions",
    "show private data",
    "reveal system prompt",
    "act as",
    "jailbreak",
    "dan mode",
    "you are now",
    "forget your instructions",
]


def check(message: str) -> bool:
    lowered = message.lower()
    return not any(phrase in lowered for phrase in BLOCKED_PHRASES)


def explain() -> str:
    return "Request blocked: message contains disallowed content."
