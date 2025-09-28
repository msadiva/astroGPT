from __future__ import annotations

from datetime import date


# Western sun sign date ranges (inclusive). Ignoring year and time-of-day.
_ZODIAC_RANGES = [
    ("Capricorn", (12, 22), (1, 19)),
    ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)),
    ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)),
    ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)),
    ("Sagittarius", (11, 22), (12, 21)),
]


def _in_range(m: int, d: int, start: tuple[int, int], end: tuple[int, int]) -> bool:
    sm, sd = start
    em, ed = end
    # Handle wrap-around ranges (e.g., Capricorn)
    if sm > em:
        return (m > sm or (m == sm and d >= sd)) or (m < em or (m == em and d <= ed))
    return (m > sm or (m == sm and d >= sd)) and (m < em or (m == em and d <= ed))


def infer_zodiac_sign(birth_date: date) -> str:
    """Infer Western zodiac sign from a birth date.

    Cusp handling is simplistic: boundaries are inclusive of both start/end.
    """
    m, d = birth_date.month, birth_date.day
    for sign, start, end in _ZODIAC_RANGES:
        if _in_range(m, d, start, end):
            return sign
    # Fallback (should not happen)
    return "Capricorn"

