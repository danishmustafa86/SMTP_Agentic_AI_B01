import asyncio
import os
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
)
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# GitHub MCP Agent — Claude Agent SDK style
#
# Prerequisites:
#   1. Node.js installed  (node --version to verify)
#   2. GITHUB_PERSONAL_ACCESS_TOKEN set in .env  (needs repo + read:org scope)
#   3. ANTHROPIC_API_KEY set in .env
#
# The GitHub MCP server runs as a local subprocess (via npx).
# Claude Agent SDK launches it automatically through the mcp_servers config.
# ---------------------------------------------------------------------------

GITHUB_TOKEN = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")

if not GITHUB_TOKEN:
    raise EnvironmentError(
        "GITHUB_PERSONAL_ACCESS_TOKEN is not set. "
        "Add it to your .env file."
    )

# ---------------------------------------------------------------------------
# GitHub MCP server — runs locally via npx (stdio transport)
# The SDK spawns this process and talks to it over stdin/stdout.
# Tool names exposed by this server follow the pattern:
#   mcp__github__<tool_name>
# e.g. mcp__github__list_repositories, mcp__github__create_issue, etc.
# ---------------------------------------------------------------------------

GITHUB_MCP_SERVER = {
    "command": "npx",
    "args": ["-y", "@github/mcp-server"],
    "env": {
        **os.environ,                               # pass through current env
        "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN,
    },
}

# Allow all tools from the github MCP server
GITHUB_TOOL_NAMES = ["mcp__github__*"]

# ---------------------------------------------------------------------------

user_query = input("Enter your GitHub query: ").strip()
if not user_query:
    user_query = (
        "List my GitHub repositories and tell me which one "
        "was updated most recently."
    )


async def message_generator():
    """Streaming input required by the Claude Agent SDK query() function."""
    yield {
        "type": "user",
        "message": {"role": "user", "content": user_query},
    }


async def main():
    print(f"\nUser: {user_query}\n")
    print("-" * 60)

    async for message in query(
        prompt=message_generator(),
        options=ClaudeAgentOptions(
            allowed_tools=GITHUB_TOOL_NAMES,
            mcp_servers={"github": GITHUB_MCP_SERVER},
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"\n[Tool call] {block.name}")
                    if hasattr(block, "input") and block.input:
                        print(f"  Input: {block.input}")

        elif isinstance(message, ResultMessage):
            print("-" * 60)
            print(f"Agent finished: {message.subtype}")


asyncio.run(main())
