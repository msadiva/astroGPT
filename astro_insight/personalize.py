from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from random import Random


@dataclass
class Personalization:
    consistency_score: float
    novelty_score: float
    priority: str


def score_for_day(name: str, sign: str, today: date) -> Personalization:
    seed = int(today.strftime("%Y%m%d")) * 17 + hash((name, sign)) % 100000
    rng = Random(seed)
    consistency = round(0.5 + rng.random() * 0.5, 2)
    novelty = round(rng.random(), 2)
    priority = ["career", "relationships", "health", "learning"][rng.randrange(4)]
    return Personalization(consistency, novelty, priority)

