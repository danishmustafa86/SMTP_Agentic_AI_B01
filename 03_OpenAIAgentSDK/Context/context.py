


# --- Imports: Agent = the brain, Runner = runs the agent, RunContextWrapper = local context ---
from agents import Agent, Runner, RunContextWrapper, function_tool
from dataclasses import dataclass

# =============================================================================
# PART 1: What the LLM sees (agent/LLM context)
# =============================================================================
# The model only sees: instructions + conversation history (your input + past messages + tool results).
# You give context to the LLM by: instructions, input to run(), or tools that return data.

# --- Minimal run: no custom context ---
# Agent: name + instructions (system prompt). Runner.run_sync(agent, input) runs one turn.
# agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful assistant. Be brief.",
# )
# # input = what the user said; it becomes the first message the LLM sees
# result = Runner.run_sync(agent, "What is 2+2?")
# # result holds everything about the run (see Part 3)
# print(result.final_output)  # the last reply from the agent


# =============================================================================
# PART 2: Local context (for your code only — NOT sent to the LLM)
# =============================================================================
# Use RunContextWrapper when tools or hooks need extra data (user id, logger, etc.).



@dataclass
class UserInfo:
    """Your custom context object. Any type (dataclass, Pydantic, etc.) works."""
    name: str
    user_id: int
    email: str
    phone_number: str


@function_tool
def get_user_greeting(wrapper: RunContextWrapper[UserInfo]) -> str:
    """
    Tool that reads from local context. The LLM only sees this docstring and the return value.
    """
    # wrapper.context = the object you passed to Runner.run(..., context=...)
    return f"Hello, {wrapper.context.name} (id={wrapper.context.user_id})."


# Agent can be typed with your context so tools and run use the same type
user_ctx = UserInfo(name="Alice", user_id=101, email="alice@example.com", phone_number="123-456-7890")
agent_with_context = Agent[UserInfo](
    name="Greeter",
    instructions="Greet the user using the get_user_greeting tool when asked who they are.",
    tools=[get_user_greeting],
)

user_query = input("Enter your query: ")
# Pass context into the run; tools receive it via RunContextWrapper
result = Runner.run_sync(
    agent_with_context,
    input=user_query,
    context=user_ctx,
)
# print(result2.final_output)






# =============================================================================
# PART 3: What is inside the run — result and "context" of the run
# =============================================================================
# Runner.run_sync(agent, input) returns a RunResult. Key attributes:

# result.input           — original input (str or list of messages)
# print(result.final_output)     #— the last agent reply (what you usually show the user)
# print(result.new_items)        #— everything produced this run: new messages, tool calls, tool outputs
# print(result.raw_responses)     #— raw LLM responses
# print(result.context_wrapper)  #— the RunContextWrapper for this run (if you passed context)
# print(result.last_agent)        #— the agent that produced the final output
# print(result.to_input_list())   #   — input + new_items merged (useful for multi-turn / resume)

# Example: inspect what was generated
# result = Runner.run_sync(agent, "Hi")
# for item in result.new_items:
#     print(type(item).__name__, item)  # Message, ToolCall, etc.
