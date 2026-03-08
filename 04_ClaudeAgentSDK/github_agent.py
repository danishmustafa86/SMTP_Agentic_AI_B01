import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions
from dotenv import dotenv_values

_env = dotenv_values()
GITHUB_TOKEN = _env.get("GITHUB_TOKEN")

SYSTEM_PROMPT = """You are a helpful GitHub assistant. You have access to GitHub tools via MCP.
You can help users:
- Search and explore repositories (code, README, files, structure)
- Summarize project documentation
- Look up GitHub user profiles and their public activity
- Find issues, pull requests, and releases
- Compare repositories or explore organizations

Always be concise, accurate, and cite specific details (repo names, usernames, links) in your answers."""


async def run_agent():
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN is not set. Add it to a .env file or your environment.")
        return

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        permission_mode="acceptEdits",
        allowed_tools=["mcp__github__*", "WebFetch", "WebSearch"],
        mcp_servers={
            "github": {
                "type": "http",
                "url": "https://api.githubcopilot.com/mcp/",
                "headers": {"Authorization": f"Bearer {GITHUB_TOKEN}"},
            }
        },
    )

    print("=" * 60)
    print("  GitHub AI Agent  —  Powered by Claude Agent SDK + GitHub MCP")
    print("=" * 60)
    print("Ask me anything about GitHub repositories, profiles,")
    print("documentation, issues, and more.")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        print("\nAssistant: ", end="", flush=True)

        async for message in query(prompt=user_input, options=options):
            if hasattr(message, "content"):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(block.text, end="", flush=True)

        print()


if __name__ == "__main__":
    asyncio.run(run_agent())
