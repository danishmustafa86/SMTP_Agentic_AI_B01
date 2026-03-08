import argparse
import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (when run from MCP/ or project root)
_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env")

from agents import Agent, HostedMCPTool, Runner, RunResult, RunResultStreaming

# import logging
# logging.basicConfig(level=logging.DEBUG)


async def main(verbose: bool, stream: bool):
    # 1. Visit https://developers.google.com/oauthplayground/
    # 2. Input https://www.googleapis.com/auth/calendar.events as the required scope
    # 3. Grab the access_token from the response and set GOOGLE_CALENDAR_AUTHORIZATION in .env
    authorization = os.environ.get("GOOGLE_CALENDAR_AUTHORIZATION")
    if not authorization:
        raise SystemExit(
            "GOOGLE_CALENDAR_AUTHORIZATION is not set. Add it to .env with the OAuth access_token (starts with ya29.)."
        )
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant that can help a user with their calendar.",
        tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "google_calendar",
                    # see https://platform.openai.com/docs/guides/tools-connectors-mcp#connectors
                    "connector_id": "connector_googlecalendar",
                    "authorization": authorization,
                    "require_approval": "never",
                }
            )
        ],
    )

    today = datetime.now().date()
    week_end = today + timedelta(days=7)
    date_range = f"{today:%Y-%m-%d} to {week_end:%Y-%m-%d}"
    run_result: RunResult | RunResultStreaming
    if stream:
        run_result = Runner.run_streamed(
            agent, f"What is my schedule from {date_range}? (that's the next week from today)"
        )
        async for event in run_result.stream_events():
            if event.type == "raw_response_event":
                if event.data.type.startswith("response.output_item"):
                    print(json.dumps(event.data.to_dict(), indent=2))
                if event.data.type.startswith("response.mcp"):
                    print(json.dumps(event.data.to_dict(), indent=2))
                if event.data.type == "response.output_text.delta":
                    print(event.data.delta, end="", flush=True)
        print()
    else:
        run_result = await Runner.run(
            agent, f"What is my schedule from {date_range}? (that's the next week from today)"
        )
        print(run_result.final_output)

    if verbose:
        for item in run_result.new_items:
            print(item)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument("--stream", action="store_true", default=False)
    args = parser.parse_args()

    asyncio.run(main(args.verbose, args.stream))