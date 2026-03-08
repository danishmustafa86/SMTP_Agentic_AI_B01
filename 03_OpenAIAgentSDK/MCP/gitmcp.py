"""
GitHub MCP (gitmcp.io) – one MCP server per repo: https://gitmcp.io/owner/repo

Tasks you can do with GitHub MCP (minimal list):
- What type of repo is this? (app, library, docs, etc.)
- What language/framework is it written in?
- Summarize the README or project purpose
- List top-level files or key directories
- Find where X is implemented / where config lives
- What are the main commands (e.g. build, test, run)?
- Explain how to contribute or run locally
- Search docs (llms.txt, readme, etc.) for a topic

Minimal example: one agent, one repo, one question (configurable).
"""

import argparse
import asyncio
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from agents import Agent, HostedMCPTool, Runner


# Default repo: use gitmcp.io/owner/repo (same as github.com/owner/repo)
DEFAULT_REPO = "openai/codex"


def gitmcp_url(owner_repo: str) -> str:
    """Turn github.com/owner/repo into gitmcp.io MCP server URL."""
    return f"https://gitmcp.io/{owner_repo.strip().replace('https://github.com/', '').strip('/')}"


async def main(repo: str, question: str) -> None:
    server_url = gitmcp_url(repo)
    agent = Agent(
        name="GitHub Assistant",
        instructions=(
            "Use the MCP tools for this repository to answer the user. "
            "Base your answers on the actual repo content (README, structure, code)."
        ),
        tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "gitmcp",
                    "server_url": server_url,
                    "require_approval": "never",
                }
            )
        ],
    )

    result = await Runner.run(agent, question)
    print(result.final_output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ask questions about a GitHub repo via GitMCP (gitmcp.io)."
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=f"Repository as owner/repo (default: {DEFAULT_REPO})",
    )
    parser.add_argument(
        "--question",
        default="What type of repository is this, and what is it used for?",
        help="Question to ask about the repo",
    )
    args = parser.parse_args()

    asyncio.run(main(args.repo, args.question))
