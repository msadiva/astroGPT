# Daily Astrological Insight

A small, modular Python service that infers a zodiac sign from a birth date and generates a concise daily insight using OpenAI. Includes a REST API (FastAPI) and a CLI (Typer).

## Features
- Western zodiac sign inference based on birth date
- OpenAI-backed natural language generation for the final insight
- REST API and CLI entry points

## Requirements
- Python 3.13
- An OpenAI API key available via the `OPENAI_API_KEY` environment variable

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set your OpenAI key (zsh/bash):
```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Run the REST API
From the project root:
```bash
uvicorn api:app --reload
```

Health check:
```bash
curl http://127.0.0.1:8000/
```

Create an insight:
```bash
curl -s -X POST http://127.0.0.1:8000/insight \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Ritika",
    "birth_date": "1995-08-20",
    "birth_time": "14:30",
    "birth_place": "Jaipur, India"
  }'
```
Example response:
```json
{
  "zodiac": "Leo",
  "insight": "Your innate leadership and warmth will shine today. Embrace spontaneity and avoid overthinking."
}
```

## CLI Usage
With the virtualenv active:
```bash
python cli.py insight \
  --name Ritika \
  --birth-date 1995-08-20 \
  --birth-time 14:30 \
  --birth-place "Jaipur, India"
```
This will output JSON containing the inferred `zodiac` and the generated `insight`.

## Notes
- The current orchestrator calls OpenAI directly for generation. Ensure `OPENAI_API_KEY` is set.
- In-memory caching is keyed by `(name, sign, date)` to avoid repeated calls for the same input on the same day.
- The daily theme and simple personalization help keep guidance fresh while remaining concise.
- Zodiac inference uses standard Western sun sign date ranges.

## Project Structure
```
astro_insight/
  __init__.py
  zodiac.py          # Sign inference
  rules.py           # Daily themes (hinting)
  llm.py             # OpenAI integration
  cache.py           # In-memory cache
  personalize.py     # Simple scoring
api.py               # FastAPI app
cli.py               # Typer CLI
requirements.txt
```


