from agents import Agent, Runner



agent = Agent(
    name="Assistant",
    instructions="You are helpfull assistant",
)


query = input("Enter your query: ")
result = Runner.run_sync(agent, query)
print(result.final_output)