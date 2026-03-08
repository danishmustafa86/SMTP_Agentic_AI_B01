from agents import Agent, Runner, WebSearchTool, function_tool
from dotenv import load_dotenv
import os

load_dotenv()


@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@function_tool
def subtract_numbers(a: int, b: int) -> int:
    """Subtract two numbers together"""
    return a - b


agent = Agent(
    name="orchestrator ",
    instructions="You are a helpful assistant that can add and subtract numbers and can also call websearch tool. If use is asking math questions out of given tools then simply say sorry.",
    tools=[ add_numbers, subtract_numbers, WebSearchTool() ]
)

input = input("Enter two numbers to add or subtract or ask anything from the web: ")


result = Runner.run_sync(agent, input)


print(result.final_output)
