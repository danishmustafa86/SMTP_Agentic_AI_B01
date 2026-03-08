# AI/ML API - https://aimlapi.com/
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
import os
from dotenv import load_dotenv

load_dotenv()

# Avoid tracing errors when using non-OpenAI providers (AIML API)
set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=os.getenv('AIML_API_KEY'),
    base_url="https://api.aimlapi.com/v1",
)

agent = Agent(
    name="AIMLAgent",
    instructions="You are helpful",
    model=OpenAIChatCompletionsModel(
        model="gpt-4o-mini",
        openai_client=client
    ),
)

query = input("Enter query: ")
result = Runner.run_sync(agent, query)
print(result.final_output)
