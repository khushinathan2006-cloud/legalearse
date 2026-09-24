from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "LegalEase"


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def ensure_output_dir() -> Path:
    output_dir = Path("generated")
    output_dir.mkdir(exist_ok=True)
    return output_dir
