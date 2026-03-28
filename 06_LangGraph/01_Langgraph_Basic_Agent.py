from langgraph.graph import StateGraph, START, END 
# from typing_extensions import TypedDict 
from pydantic import BaseModel
from typing import Literal 
import random 


class state(BaseModel):
    graph_state: str 


def node_1(state):
    return {"graph_state": state.graph_state + " I am"}


def node_2(state):
    return {"graph_state": state.graph_state + " Happy!"} 

def node_3(state): 
    return {"graph_state": state.graph_state + " Sad!"}



def decide_mood(state) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"
    return "node_3"


builder = StateGraph(state)


builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()


result = graph.invoke({"graph_state": "Hi, this is Danish."})

print(result)



