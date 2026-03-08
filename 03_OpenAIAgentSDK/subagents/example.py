"""Minimal subagents example: main agent hands off to specialized agents."""
from dotenv import load_dotenv
load_dotenv()

from agents import Agent, Runner

# Subagents (specialists)
math_agent = Agent(
    name="Math Agent",
    instructions="You only do math. Answer with the numeric result.",
)

general_agent = Agent(
    name="General Agent",
    instructions="You answer general knowledge and non-math questions.",
)

# Main agent: triages and hands off to subagents
main_agent = Agent(
    name="Triage",
    instructions="Route math questions to the math agent, everything else to the general agent.",
    handoffs=[math_agent, general_agent],
)

query = input("Ask something: ")
result = Runner.run_sync(main_agent, query)
print(result.final_output)
