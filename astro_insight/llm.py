from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
from openai import OpenAI 


_SIGN_TRAITS = {
    "Aries": ["bold", "energetic", "trailblazing"],
    "Taurus": ["grounded", "patient", "steady"],
    "Gemini": ["curious", "adaptable", "expressive"],
    "Cancer": ["intuitive", "caring", "protective"],
    "Leo": ["confident", "warm", "charismatic"],
    "Virgo": ["meticulous", "practical", "helpful"],
    "Libra": ["diplomatic", "harmonious", "fair-minded"],
    "Scorpio": ["intense", "focused", "transformative"],
    "Sagittarius": ["optimistic", "adventurous", "philosophical"],
    "Capricorn": ["disciplined", "ambitious", "resilient"],
    "Aquarius": ["innovative", "humanitarian", "independent"],
    "Pisces": ["imaginative", "compassionate", "dreamy"],
}


@dataclass
class GenerationConfig:
    temperature: float = 0.7
    max_tokens: int = 120


class LLMClient:
    """LLM client for generating daily insights.
    """

    def __init__(self, config: GenerationConfig | None = None) -> None:
        self.config = config or GenerationConfig()


    def generate_insight_openai(
        self,
        *,
        name: str,
        sign: str,
        today: date,
        extra_context: Optional[str] = None,
        model: str = "gpt-4o-mini",
    ) -> str:
        """Call OpenAI Chat Completions to generate an insight.

        Requires OPENAI_API_KEY to be set in the environment.
        """
        if OpenAI is None:
            raise RuntimeError("OpenAI client not available.")

        client = OpenAI(api_key=API_KEY)
        sys_prompt = (
            "You are an expert astrologer who writes short, warm and practical daily insights."
        )
        traits_csv = ", ".join(_SIGN_TRAITS.get(sign, []))
        user_prompt = (
            f"User: {name}\n"
            f"Zodiac: {sign}\n"
            f"Date: {today.isoformat()}\n"
            f"Sign traits: {traits_csv}\n"
            f"Extra context: {extra_context or ''}\n\n"
            "Write a single-paragraph daily guidance in 40-60 words."
            " Keep it specific, supportive, and non-deterministic. Avoid astrological jargon."
        )

        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )
        return (resp.choices[0].message.content or "").strip()

