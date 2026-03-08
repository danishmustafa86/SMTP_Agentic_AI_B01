"""
Google Calendar: create one new event (random by default, 2 days from now).
Uses the Google Calendar REST API directly so creation works (connector_googlecalendar is read-only).
Does not list existing events.
"""

import argparse
import asyncio
import os
import random
import re
from pathlib import Path
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env")

# Default timezone for event start/end (Google API expects dateTime + timeZone)
DEFAULT_TZ = "UTC"


def _random_event() -> tuple[str, str, int, int]:
    """Return (title, date_yyyy_mm_dd, hour, minute) for an event 2 days from now."""
    titles = [
        "Quick sync",
        "Focus time",
        "Review meeting",
        "Check-in",
        "Planning session",
        "Code review",
        "Team catch-up",
        "Deep work block",
    ]
    day_offset = 2
    event_date = datetime.now() + timedelta(days=day_offset)
    date_str = event_date.strftime("%Y-%m-%d")
    hour = random.randint(9, 17)
    minute = random.choice([0, 15, 30, 45])
    return (random.choice(titles), date_str, hour, minute)


def _parse_create_arg(create_arg: str) -> tuple[str, str, int, int] | None:
    """Parse 'Title on YYYY-MM-DD at H:MM' or 'Title on YYYY-MM-DD at HH:MM'. Returns (title, date_str, hour, minute) or None."""
    # Match: something " on " date " at " time
    m = re.match(r"^(.+?)\s+on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{1,2}):(\d{2})\s*$", create_arg.strip(), re.IGNORECASE)
    if not m:
        return None
    title, date_str, hour_str, min_str = m.groups()
    return (title.strip(), date_str, int(hour_str), int(min_str))


def create_event_via_api(
    access_token: str,
    title: str,
    date_ymd: str,
    hour: int,
    minute: int,
    duration_minutes: int = 60,
    timezone: str = DEFAULT_TZ,
) -> tuple[bool, str]:
    """
    Create a single all-day or timed event via Google Calendar API v3.
    Returns (success, message).
    """
    # Build start datetime in ISO format for the given timezone (Google expects local time with zone)
    start_dt = f"{date_ymd}T{hour:02d}:{minute:02d}:00"
    end_h = hour + (minute + duration_minutes) // 60
    end_m = (minute + duration_minutes) % 60
    end_dt = f"{date_ymd}T{end_h:02d}:{end_m:02d}:00"

    body = {
        "summary": title,
        "start": {"dateTime": start_dt, "timeZone": timezone},
        "end": {"dateTime": end_dt, "timeZone": timezone},
    }
    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    try:
        r = requests.post(url, headers=headers, json=body, timeout=15)
    except requests.RequestException as e:
        return (False, f"Request failed: {e}")

    if r.status_code == 401:
        return (False, "Invalid or expired token. Refresh GOOGLE_CALENDAR_AUTHORIZATION in .env (OAuth Playground, scope: calendar or calendar.events).")
    if r.status_code == 403:
        return (False, "Calendar API access denied. Use OAuth scope https://www.googleapis.com/auth/calendar (or calendar.events with write).")
    if r.status_code != 200:
        try:
            err = r.json()
            msg = err.get("error", {}).get("message", r.text)
        except Exception:
            msg = r.text
        return (False, f"API error {r.status_code}: {msg}")

    data = r.json()
    event_id = data.get("id", "")
    html_link = data.get("htmlLink", "")
    return (True, f"Created: {title} on {date_ymd} at {hour:02d}:{minute:02d}. {html_link or ''}")


async def main(verbose: bool, _stream: bool, create_event: str | None) -> None:
    authorization = os.environ.get("GOOGLE_CALENDAR_AUTHORIZATION")
    if not authorization:
        raise SystemExit(
            "GOOGLE_CALENDAR_AUTHORIZATION is not set. Add it to .env (OAuth access_token from https://developers.google.com/oauthplayground/, scope: calendar or calendar.events)."
        )

    if create_event:
        parsed = _parse_create_arg(create_event)
        if not parsed:
            print('Custom event must match: "Title on YYYY-MM-DD at HH:MM"')
            print('Example: --create "Team standup on 2026-02-20 at 9:00"')
            raise SystemExit(1)
        title, date_str, hour, minute = parsed
        print(f"Creating event: {title} on {date_str} at {hour:02d}:{minute:02d}\n")
    else:
        title, date_str, hour, minute = _random_event()
        print(f"Creating random event: {title} on {date_str} ({datetime.now() + timedelta(days=2):%A}) at {hour:02d}:{minute:02d}\n")

    success, message = create_event_via_api(authorization, title, date_str, hour, minute)
    print(message)
    if success:
        print("\nCheck your Google Calendar to verify.")
    if verbose and not success:
        print("(Use OAuth scope https://www.googleapis.com/auth/calendar for write access.)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Google Calendar: create one new event (random by default, 2 days from now). Does not list events."
    )
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument("--stream", action="store_true", default=False, help="(Ignored; kept for CLI compatibility.)")
    parser.add_argument(
        "--create",
        metavar="DESCRIPTION",
        default=None,
        help='Create a specific event. Format: "Title on YYYY-MM-DD at HH:MM"',
    )
    args = parser.parse_args()

    asyncio.run(main(args.verbose, args.stream, args.create))
