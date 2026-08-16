"""Launch entry point used by the CampusBot launcher: the app itself lives in app/api/server.py."""

from __future__ import annotations

import os
from pathlib import Path

import uvicorn

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.api.server import app


if __name__ == "__main__":
    host = os.getenv("CAMPUSBOT_HOST", "127.0.0.1")
    port = int(os.getenv("CAMPUSBOT_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
