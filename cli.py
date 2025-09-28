from __future__ import annotations

import json
import sys
import typer

from astro_insight.orchestrator import generate_daily_insight


app = typer.Typer(add_completion=False, help="Generate daily astrological insights")


@app.command()
def insight(
    name: str = typer.Option("Friend", help="Person's name"),
    birth_date: str = typer.Option(..., help="Birth date, e.g. 1995-08-20"),
    birth_time: str | None = typer.Option(None, help="Birth time, e.g. 14:30"),
    birth_place: str | None = typer.Option(None, help="Birth place"),
    pretty: bool = typer.Option(True, help="Pretty-print JSON output"),
):
    payload = {
        "name": name,
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_place": birth_place,
    }
    res = generate_daily_insight(payload)
    if pretty:
        typer.echo(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        typer.echo(json.dumps(res, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    try:
        app()
        return 0
    except Exception as exc:  # noqa: BLE001
        typer.echo(str(exc), err=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

