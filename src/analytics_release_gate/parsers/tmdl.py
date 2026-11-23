from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_MEASURE = re.compile(r"^\s*measure\s+(?:'((?:[^']|'')+)'|([^=]+?))\s*=", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class MeasureBlock:
    name: str
    path: Path
    start_line: int
    text: str
    description: str = ""


def iter_measure_blocks(path: Path) -> list[MeasureBlock]:
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = _MEASURE.match(line)
        if match:
            starts.append((index, (match.group(1) or match.group(2) or "").strip()))

    blocks: list[MeasureBlock] = []
    for start, name in starts:
        indent = len(lines[start]) - len(lines[start].lstrip())
        end = start + 1
        while end < len(lines):
            current = lines[end]
            if current.strip() and len(current) - len(current.lstrip()) <= indent:
                break
            end += 1
        comments: list[str] = []
        preceding = start - 1
        while preceding >= 0:
            current = lines[preceding]
            if (len(current) - len(current.lstrip()) != indent
                    or not current.lstrip().startswith("///")):
                break
            comments.append(current.lstrip()[3:].strip())
            preceding -= 1
        blocks.append(MeasureBlock(name=name.replace("''", "'"), path=path,
            start_line=start + 1, text="\n".join(lines[start:end]),
            description="\n".join(reversed(comments))))
    return blocks
