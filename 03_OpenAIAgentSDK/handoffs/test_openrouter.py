# OpenRouter - https://openrouter.ai/
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv

load_dotenv()

# print(os.getenv("OPENROUTER_API_KEY"))

client = AsyncOpenAI(
    api_key=os.getenv('OPENROUTER_API_KEY'),
    base_url="https://openrouter.ai/api/v1",
)

agent = Agent(
    name="OpenRouterAgent",
    instructions="You are helpful",
    model=OpenAIChatCompletionsModel(
        model="meta-llama/llama-3.2-3b-instruct:free",  # Free model
        openai_client=client
    ),
)

query = input("Enter query: ")
result = Runner.run_sync(agent, query)
print(result.final_output)
