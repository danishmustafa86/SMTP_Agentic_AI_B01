from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AnyMessage
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import math
load_dotenv()

# LLM setup. This model will decide when to call tools.
llm = ChatOpenAI( model="gpt-4o-mini", api_key=os.getenv("AIMLAPI_API_KEY"), base_url="https://api.aimlapi.com/v1")




def add(a: int, b: int) -> int:
    """Return a + b."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Return a - b."""
    return a - b


def multiply(a: int, b: int) -> int:
    """Return a * b."""
    return a * b


def divide(a: int, b: int) -> float:
    """Return a / b. Raises if b is 0."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def power(a: int, b: int) -> int:
    """Return a raised to b."""
    return a ** b


def square_root(a: float) -> float:
    """Return sqrt(a). Raises if a is negative."""
    if a < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(a)


# Expose tool functions to the model.
tools = [add, subtract, multiply, divide, power, square_root]
llm_with_tools = llm.bind_tools(tools)



class MessagesState(TypedDict):
    # Conversation state is a running list of messages.
    # add_messages tells LangGraph how to append new messages.
    messages: Annotated[list[AnyMessage], add_messages]
    


def _normalize_messages(messages: list[AnyMessage]) -> list[AnyMessage]:
    """Ensure message content is provider-safe for chained tool calls."""
    normalized: list[AnyMessage] = []
    for msg in messages:
        content = msg.content
        if content is None:
            normalized.append(msg.model_copy(update={"content": ""}))
        elif not isinstance(content, (str, list)):
            normalized.append(msg.model_copy(update={"content": str(content)}))
        else:
            normalized.append(msg)
    return normalized


def tool_calling_llm(state: MessagesState):
    # Node 1: call the model. It may answer directly or request tools.
    safe_messages = _normalize_messages(state["messages"])
    response = llm_with_tools.invoke(safe_messages)
    if response.content is None:
        response = response.model_copy(update={"content": ""})
    return {"messages": [response]}

# Build graph
builder = StateGraph(MessagesState)


builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools))



# Flow: START -> model node.
builder.add_edge(START, "tool_calling_llm")
# Route after model response:
# - if tool call exists -> "tools"
# - otherwise -> END
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
)
# After each tool result, go back to model so it can decide:
# call another tool or produce final answer.
builder.add_edge("tools", "tool_calling_llm")
graph = builder.compile()

# Try a prompt that can use one or more calculator tools.

query = input("Enter a query: ")
messages = graph.invoke({"messages": HumanMessage(content=query)})
for m in messages['messages']:
    m.pretty_print()
