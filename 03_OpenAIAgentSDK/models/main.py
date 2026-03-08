from agents import Agent, Runner , OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os

load_dotenv()


set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=os.getenv("AIML_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)



agent = Agent(
    name="AIMLAgent",
    instructions="You are a helpful assistant.",
    model=OpenAIChatCompletionsModel(
        model="gpt-4o-mini",
        openai_client=client
    )
)


query = input("Enter your query: ")
result = Runner.run_sync(agent, query)
print(result.final_output)