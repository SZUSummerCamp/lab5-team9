"""Single entry point for talking to the local model."""

from __future__ import annotations

import os

import httpx
from fastapi import HTTPException


def call_llm(system_prompt: str, user_message: str) -> str:
    ollama_url = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
    ollama_model = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")

    payload = {
        "model": ollama_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0.0,
            "num_ctx": 4096,
            "seed": 42,
        },
    }

    try:
        response = httpx.post(ollama_url, json=payload, timeout=90)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"The local model is unavailable. Start Ollama and check {ollama_model}.",
        ) from exc

    answer = response.json().get("message", {}).get("content", "").strip()
    if not answer:
        raise HTTPException(status_code=502, detail="The model returned an empty response.")
    return answer
