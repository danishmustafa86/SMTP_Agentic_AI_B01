from agents import Agent, Runner
from dotenv import load_dotenv
import os

load_dotenv()


urdu_agent = Agent(
    name = "Urdu Agent",
    instructions = "You are a helpful assistant that can translate English to Urdu."
)


arabic_agent = Agent(
    name = "Arabic Agent",
    instructions = "You are a helpful assistant that can translate English to Arabic."
)

agent = Agent(
    name = "Orchestrator",
    instructions = "YOur are helpful language translator with your given translation handoff agents.",
    tools = [
        urdu_agent.as_tool(
            tool_name = "urdu_tranlator",
            tool_description = "Translate English to Urdu."
        ),
        arabic_agent.as_tool(
            tool_name = "arabic_tranlator",
            tool_description = "Translate English to Arabic."
        )
    ]
)

input = input("Enter the text to translate: ")

result = Runner.run_sync(agent, input)

print(result.final_output)