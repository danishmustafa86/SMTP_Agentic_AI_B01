
from __future__ import annotations

import os
import uuid
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from pymongo import MongoClient
from typing_extensions import TypedDict

load_dotenv()

MONGO_URI = os.getenv("DB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB", "langgraph_threads")
COLLECTION = "threads"

client = MongoClient(MONGO_URI)
threads = client[DB_NAME][COLLECTION]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("AIMLAPI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def assistant(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
graph = builder.compile()


def _rows_to_messages(rows: list[dict[str, Any]]) -> list[AnyMessage]:
    out: list[AnyMessage] = []
    for r in rows:
        role, content = r["role"], r["content"]
        if role == "user":
            out.append(HumanMessage(content=content))
        elif role == "assistant":
            out.append(AIMessage(content=content))
    return out


def _messages_to_rows(msgs: list[AnyMessage]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for m in msgs:
        if isinstance(m, HumanMessage):
            rows.append({"role": "user", "content": str(m.content)})
        elif isinstance(m, AIMessage):
            rows.append({"role": "assistant", "content": str(m.content)})
    return rows


class ChatBody(BaseModel):
    message: str
    thread_id: str | None = Field(
        default=None,
        description="Omit or null for a new thread; reuse to continue the same conversation.",
    )


class ChatOut(BaseModel):
    thread_id: str
    reply: str


app = FastAPI(title="LangGraph MongoDB threads")


@app.get("/home")
def home():
    return {"message": "Hello World"}


@app.post("/chat", response_model=ChatOut)
def chat(body: ChatBody):
    tid = body.thread_id or str(uuid.uuid4())
    doc = threads.find_one({"_id": tid})
    history_rows: list[dict[str, Any]] = doc["messages"] if doc else []
    messages = _rows_to_messages(history_rows)
    messages.append(HumanMessage(content=body.message))

    result = graph.invoke({"messages": messages})
    final = result["messages"]
    threads.update_one(
        {"_id": tid},
        {"$set": {"messages": _messages_to_rows(final)}},
        upsert=True,
    )

    last = final[-1]
    reply = str(last.content) if isinstance(last, AIMessage) else ""
    return ChatOut(thread_id=tid, reply=reply)


@app.get("/threads/{thread_id}")
def get_thread(thread_id: str):
    doc = threads.find_one({"_id": thread_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Unknown thread_id")
    return {"thread_id": thread_id, "messages": doc["messages"]}
