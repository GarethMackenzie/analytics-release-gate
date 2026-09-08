from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_MEASURE = re.compile(r"^\s*measure\s+(?:'([^']+)'|([^=]+?))\s*=", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class MeasureBlock:
    name: str
    path: Path
    start_line: int
    text: str


def iter_measure_blocks(path: Path) -> list[MeasureBlock]:
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = _MEASURE.match(line)
        if match:
            starts.append((index, (match.group(1) or match.group(2) or "").strip()))

    blocks: list[MeasureBlock] = []
    for position, (start, name) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        blocks.append(
            MeasureBlock(name=name, path=path, start_line=start + 1, text="\n".join(lines[start:end]))
        )
    return blocks
