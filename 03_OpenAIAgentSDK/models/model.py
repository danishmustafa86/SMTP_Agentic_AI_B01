import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from openai import AsyncOpenAI

from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

BASE_URL ="https://api.aimlapi.com/v1"
API_KEY = os.getenv("AIML_API_KEY")
# MODEL_NAME = "gpt-4o-mini"

if not BASE_URL or not API_KEY:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )


def _sanitize_messages(messages: list) -> list:
    """AIML API rejects messages with content=null; OpenAI allows it for assistant tool_calls."""
    out = []
    for m in messages:
        m = dict(m)
        if m.get("content") is None:
            m["content"] = ""
        out.append(m)
    return out


class AIMLCompatibleClient(AsyncOpenAI):
    """Wrapper that ensures no message has content=null for AIML API compatibility."""

    async def post(self, path, *, body=None, **kwargs):
        if isinstance(body, dict) and "messages" in body and body["messages"] is not None:
            body = {**body, "messages": _sanitize_messages(body["messages"])}
        return await super().post(path, body=body, **kwargs)


client = AIMLCompatibleClient(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

# An alternate approach that would also work:
# PROVIDER = OpenAIProvider(openai_client=client)
# agent = Agent(..., model="some-custom-model")
# Runner.run(agent, ..., run_config=RunConfig(model_provider=PROVIDER))


@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(
            model="gpt-4o-mini", openai_client=client),
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())