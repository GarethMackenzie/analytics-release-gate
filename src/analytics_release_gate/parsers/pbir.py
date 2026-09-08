from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_json(path: Path) -> dict[str, Any] | list[Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if not isinstance(data, (dict, list)):
        raise ValueError("JSON root must be an object or array")
    return data
