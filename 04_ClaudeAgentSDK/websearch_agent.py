import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
)

# ---------------------------------------------------------------------------
# Web Search Agent using Claude Agent SDK
# The web_search tool is a built-in Anthropic-hosted tool — no MCP server
# or @tool decorator needed, just add it to allowed_tools.
# ---------------------------------------------------------------------------

user_query = input("Enter your search query: ").strip()
if not user_query:
    user_query = (
        "Search for the current prices of AAPL and GOOGL, "
        "then calculate which has a better P/E ratio."
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
            # web_search is a built-in Claude tool — no MCP server required
            allowed_tools=["web_search"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    # A tool is being called (e.g. web_search)
                    print(f"\n[Tool call] {block.name}")
                    if hasattr(block, "input") and block.input:
                        print(f"  Input: {block.input}")

        elif isinstance(message, ResultMessage):
            print("-" * 60)
            print(f"Agent finished: {message.subtype}")


asyncio.run(main())
