from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

from analytics_release_gate.models import Finding


class Check(Protocol):
    def __call__(self, root: Path) -> Iterable[Finding]: ...
