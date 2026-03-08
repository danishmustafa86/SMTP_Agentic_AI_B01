"""Minimal GitHub/code MCP example using hosted MCP (no local server)."""
from dotenv import load_dotenv
load_dotenv()

from agents import Agent, HostedMCPTool, Runner

# Hosted GitHub MCP – tools run on OpenAI's side, no npx/node needed
agent = Agent(
    name="Assistant",
    instructions="Use the repo tools when the user asks about code or a repository.",
    tools=[
        HostedMCPTool(tool_config={
            "type": "mcp",
            "server_label": "gitmcp",
            "server_url": "https://gitmcp.io/openai/codex",
            "require_approval": "never",
        }),
    ],
)

query = input("Ask about a repo (e.g. 'What language is openai/cookbook? '): ")
result = Runner.run_sync(agent, query)
print(result.final_output)
