from agents import Agent, Runner, WebSearchTool
from dotenv import load_dotenv
import os

load_dotenv()

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that can search the web for information.",
    tools=[
        WebSearchTool(),
    ],
)

result = Runner.run_sync(agent, "Which coffee shop should I go to, taking into account my preferences and the weather today in SF?")
print(result.final_output)


