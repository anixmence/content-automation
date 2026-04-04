from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SETTINGS_PATH = BASE_DIR / "config" / "settings.json"
OUTPUT_DIR = BASE_DIR / "output"


class SettingsError(Exception):
    """Raised when settings are invalid."""


def load_settings(path: Path = DEFAULT_SETTINGS_PATH) -> dict:
    if not path.exists():
        raise SettingsError(f"Settings file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    required_fields = ["moments_count", "article_sections", "default_tone"]
    for field in required_fields:
        if field not in data:
            raise SettingsError(f"Missing required setting: {field}")

    return data
