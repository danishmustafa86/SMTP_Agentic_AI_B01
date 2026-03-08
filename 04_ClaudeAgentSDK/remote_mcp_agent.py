import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Remote MCP Agent
# Uses Anthropic's beta "mcp-client-2025-11-20" feature.
# Anthropic's servers connect to the remote MCP URL — your code never
# touches the MCP server directly.
# ---------------------------------------------------------------------------

# --- Configuration ---------------------------------------------------------
# Swap these values for any real remote MCP server you want to connect to.
MCP_SERVER_URL   = "https://example-server.modelcontextprotocol.io/sse"
MCP_SERVER_NAME  = "example-mcp"
MCP_AUTH_TOKEN   = "YOUR_TOKEN"        # leave as-is if the server is public
# ---------------------------------------------------------------------------

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

user_query = input("Enter your query: ").strip()
if not user_query:
    user_query = "What tools do you have available?"

print(f"\nUser: {user_query}\n")
print("-" * 60)

# Agentic loop — keeps running until Claude stops calling tools
messages = [{"role": "user", "content": user_query}]

while True:
    response = client.beta.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        betas=["mcp-client-2025-11-20"],        # enables the remote MCP feature
        messages=messages,

        # Tell Anthropic which remote MCP server to connect to
        mcp_servers=[
            {
                "type": "url",
                "url": MCP_SERVER_URL,
                "name": MCP_SERVER_NAME,
                "authorization_token": MCP_AUTH_TOKEN,
            }
        ],

        # Expose all tools from that MCP server to Claude
        tools=[
            {
                "type": "mcp_toolset",
                "mcp_server_name": MCP_SERVER_NAME,
            }
        ],
    )

    # Process each content block in the response
    tool_uses = []

    for block in response.content:
        block_type = getattr(block, "type", None)

        if block_type == "text":
            print(f"Claude: {block.text}")

        elif block_type == "tool_use":
            print(f"\n[Tool call] {block.name}")
            if hasattr(block, "input") and block.input:
                print(f"  Input : {block.input}")
            tool_uses.append(block)

        elif block_type == "tool_result":
            print(f"\n[Tool result] {block}")

    # If Claude made tool calls, feed the results back and loop again
    if tool_uses:
        messages.append({"role": "assistant", "content": response.content})

        tool_results = [
            {
                "type": "tool_result",
                "tool_use_id": tu.id,
                "content": "",          # remote MCP results are handled by Anthropic
            }
            for tu in tool_uses
        ]
        messages.append({"role": "user", "content": tool_results})
        continue

    # No tool calls left — Claude has produced its final answer
    if response.stop_reason == "end_turn":
        break

print("-" * 60)
print("Agent finished.")
