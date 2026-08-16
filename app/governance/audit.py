"""Audit trail: records which user ran which skill, and how it went."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "audit.log"


def log(user: str, skill_name: str, status: str, duration: float) -> None:
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "skill": skill_name,
        "status": status,
        "duration_seconds": round(duration, 3),
    }

    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001 - auditing must never break a request
        pass
