from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)


# ── 1. Define tools the agent can use ────────────────────────────────────────
@tool
def calculate(expression: str) -> str:
    """Evaluate a basic math expression like '2 + 3 * 4'."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

@tool
def search(query: str) -> str:
    """Search the web for information about a topic (mock)."""
    return f"Top result for '{query}': It is a widely studied subject with many resources available."

tools = [calculate, search]


# ── 2. Agent prompt ── must include agent_scratchpad ─────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when needed."),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),   # where tool calls/results go
])


# ── 3. Build the agent ────────────────────────────────────────────────────────
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# ── 4. Run the agent ─────────────────────────────────────────────────────────
result = agent_executor.invoke({"input": "What is 456 * 789?"})
print("Answer:", result["output"])

result2 = agent_executor.invoke({"input": "Search for information about LangGraph."})
print("Answer:", result2["output"])
