from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_pbip(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("PBIP root must be a JSON object")
    return data
