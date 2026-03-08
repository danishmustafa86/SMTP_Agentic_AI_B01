# agent="Hostel Assitant"
import asyncio
from claude_agent_sdk import ClaudeAgentOptions, query
from dotenv import dotenv_values

_env = dotenv_values()

async def main_agent():
    async for message in query(
        prompt = "You are a helpfull hostel assistant. Help me with my hostel tasks.",
        options = ClaudeAgentOptions(
            # model = "claude-3-5-sonnet-latest",
            allowed_tools= ["READ", "WRITE", "DELETE"],
            permission_mode = "acceptEdits",
        )
        ):
        if hasattr(message, "content"):
            print(message.content)

asyncio.run(main_agent())