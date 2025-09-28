from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import os
from typing import Any, Dict

from dateutil import parser as date_parser

from .zodiac import infer_zodiac_sign
from .llm import LLMClient, GenerationConfig
from .cache import GLOBAL_CACHE
from .personalize import score_for_day


@dataclass
class UserInput:
    name: str
    birth_date: str
    birth_time: str | None = None
    birth_place: str | None = None
    


def _parse_date(date_str: str) -> date:
    dt = date_parser.parse(date_str).date()
    return dt


def _today() -> date:
    return datetime.utcnow().date()


def generate_daily_insight(payload: Dict[str, Any]) -> Dict[str, Any]:
    user = UserInput(
        name=payload.get("name", "Friend"),
        birth_date=payload["birth_date"],
        birth_time=payload.get("birth_time"),
        birth_place=payload.get("birth_place"),
    )

    birth_dt = _parse_date(user.birth_date)
    sign = infer_zodiac_sign(birth_dt)
    today = _today()

    cache_key = (user.name, sign, today)
    cached = GLOBAL_CACHE.get(cache_key)
    if cached is None:
        llm = LLMClient(GenerationConfig())
        persona = score_for_day(user.name, sign, today)
        extra = f"Focus area: {persona.priority}."

        insight_en = llm.generate_insight_openai(
                name=user.name,
                sign=sign,
                today=today,
                extra_context=extra,)
       
    
        GLOBAL_CACHE.set(cache_key, insight_en)
    else:
        insight_en = cached

    return {
        "zodiac": sign,
        "insight": insight_en,
    }

