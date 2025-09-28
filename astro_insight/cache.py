from __future__ import annotations

from datetime import date
from typing import Dict, Tuple


class DailyCache:
    """Very simple in-memory cache keyed by (name, sign, date, lang)."""

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, str, date, str], str] = {}

    def get(self, key: Tuple[str, str, date, str]) -> str | None:
        return self._store.get(key)

    def set(self, key: Tuple[str, str, date, str], value: str) -> None:
        self._store[key] = value


GLOBAL_CACHE = DailyCache()

