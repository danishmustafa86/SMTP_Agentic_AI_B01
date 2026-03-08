import os
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.tool import function_tool

# Load environment variables from .env file
load_dotenv()


# Define tools using the @function_tool decorator
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@function_tool
def subtract_numbers(a: int, b: int) -> int:
    """Subtract two numbers together"""
    return a - b






# Create agent (NO model import, NO model config)
agent = Agent(
    name="StarterAgent",
    instructions="You are a helpful AI assistant. Explain things simply.",
    tools=[add_numbers, subtract_numbers]
)

# Run agent
result = Runner.run_sync(
    agent,
    input=input("add numbers to add or subtract: ")
)

print("\nAgent Output:\n")
print(result.final_output)
