from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)


# ── 1. Define tools with @tool decorator ─────────────────────────────────────
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny and 28°C."   # mock response


# ── 2. Bind tools to LLM ─────────────────────────────────────────────────────
tools = [add, multiply, get_weather]
llm_with_tools = llm.bind_tools(tools)


# ── 3. LLM decides which tool to call ────────────────────────────────────────
response = llm_with_tools.invoke("What is 15 + 27?")
print("Tool calls:", response.tool_calls)   # [{'name': 'add', 'args': {'a': 15, 'b': 27}}]

response2 = llm_with_tools.invoke("What is the weather in Karachi?")
print("Tool calls:", response2.tool_calls)


