import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai import AuthenticationError

from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

# Load .env: first cwd, then project root (so it works from handoffs/ or project root)
load_dotenv()
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

set_tracing_disabled(True)

api_key = os.getenv("TOGETHER_API_KEY", "").strip()
if not api_key:
    print("ERROR: TOGETHER_API_KEY is not set or empty.")
    print("  1. Get a key from https://api.together.ai/settings/api-keys")
    print("  2. Add to .env: TOGETHER_API_KEY=your_key_here")
    print(f"  (Checked .env at: {env_path})")
    exit(1)

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.together.xyz/v1",
)


async def check_together_key():
    """Verify the API key works before running the agent."""
    try:
        await client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5,
        )
    except AuthenticationError:
        print("Together API rejected your key (401 Invalid API key).")
        print()
        print("Do this:")
        print("  1. Open https://api.together.ai/settings/api-keys")
        print("  2. Create a NEW API key (or copy the existing one again).")
        print("  3. In your .env file, set:  TOGETHER_API_KEY=<paste the key>")
        print("     No quotes, no extra spaces. Save the file.")
        print(f"  4. .env path: {env_path}")
        exit(1)


# Fail fast with a clear message if the key is invalid
asyncio.run(check_together_key())


agent = Agent(
    name = "AIMLAgent",
    instructions = "You are a helpful assistant",
    model = OpenAIChatCompletionsModel(
        model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        openai_client = client
    )
)

query = input("Enter you query: ")

result = Runner.run_sync(agent, query)

print(result.final_output)