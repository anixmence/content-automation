from __future__ import annotations

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SETTINGS_PATH = BASE_DIR / "config" / "settings.json"
OUTPUT_DIR = BASE_DIR / "output"


class SettingsError(Exception):
    """Raised when settings are invalid."""


class MissingAPIKeyError(Exception):
    """Raised when OPENAI_API_KEY is missing."""


def load_settings(path: Path = DEFAULT_SETTINGS_PATH) -> dict:
    if not path.exists():
        raise SettingsError(f"Settings file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    required_fields = ["moments_count", "article_sections", "default_tone", "model"]
    for field in required_fields:
        if field not in data:
            raise SettingsError(f"Missing required setting: {field}")

    return data


def load_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise MissingAPIKeyError(
            "OPENAI_API_KEY 未設定。請先在環境變數設定 API key，例如：\n"
            "export OPENAI_API_KEY='your_api_key'"
        )
    return api_key


def load_model_name(settings: dict) -> str:
    return os.getenv("OPENAI_MODEL", str(settings["model"]))
