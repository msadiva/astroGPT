from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from astro_insight.orchestrator import generate_daily_insight


app = FastAPI(title="Daily Astrological Insight")


class InsightRequest(BaseModel):
    name: str = Field(default="Friend")
    birth_date: str
    birth_time: str | None = None
    birth_place: str | None = None


@app.post("/insight")
def create_insight(req: InsightRequest):
    return generate_daily_insight(req.model_dump())


@app.get("/")
def root():
    return {"status": "ok", "endpoints": ["/insight"]}

