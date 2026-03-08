import asyncio
from typing import Any
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    tool,
    create_sdk_mcp_server,
)

# ---------------------------------------------------------------------------
# Custom math tools for testing agent tool calling
# ---------------------------------------------------------------------------

@tool(
    "sum_numbers",
    "Add two numbers together. Use this to sum or add numbers.",
    {"a": float, "b": float},
)
async def sum_numbers(args: dict[str, Any]) -> dict[str, Any]:
    result = args["a"] + args["b"]
    return {"content": [{"type": "text", "text": str(result)}]}


@tool(
    "subtract",
    "Subtract the second number from the first. Use for subtraction.",
    {"a": float, "b": float},
)
async def subtract(args: dict[str, Any]) -> dict[str, Any]:
    result = args["a"] - args["b"]
    return {"content": [{"type": "text", "text": str(result)}]}


@tool(
    "multiply",
    "Multiply two numbers together.",
    {"a": float, "b": float},
)
async def multiply(args: dict[str, Any]) -> dict[str, Any]:
    result = args["a"] * args["b"]
    return {"content": [{"type": "text", "text": str(result)}]}


@tool(
    "divide",
    "Divide the first number by the second. Fails if divisor is zero.",
    {"a": float, "b": float},
)
async def divide(args: dict[str, Any]) -> dict[str, Any]:
    b = args["b"]
    if b == 0:
        return {"content": [{"type": "text", "text": "Error: cannot divide by zero"}]}
    result = args["a"] / b
    return {"content": [{"type": "text", "text": str(result)}]}


# MCP server exposing the math tools (required for custom tools with query())
math_server = create_sdk_mcp_server(
    name="math",
    version="1.0.0",
    tools=[sum_numbers, subtract, multiply, divide],
)

MATH_TOOL_NAMES = [
    "mcp__math__sum_numbers",
    "mcp__math__subtract",
    "mcp__math__multiply",
    "mcp__math__divide",
]

# ---------------------------------------------------------------------------

user_query = input("What do you want to do? ")


async def message_generator():
    """Streaming input required when using MCP/custom tools."""
    yield {
        "type": "user",
        "message": {"role": "user", "content": user_query},
    }


async def main():
    # Agentic loop: streams messages as Claude works
    async for message in query(
        prompt=message_generator(),
        options=ClaudeAgentOptions(
            allowed_tools=MATH_TOOL_NAMES,  # Custom math tools
            mcp_servers={"math": math_server},
            permission_mode="acceptEdits",
        ),
    ):
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  # Claude's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")  # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")  # Final result


asyncio.run(main())