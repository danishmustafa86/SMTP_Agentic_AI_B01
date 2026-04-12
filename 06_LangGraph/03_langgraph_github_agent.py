import warnings
warnings.filterwarnings("ignore", category = UserWarning)


from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessagesState, StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
# from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage,HumanMessage, AnyMessage 
from typing import Annotated
from dotenv import load_dotenv
import os
from pprint import pprint 
import requests
load_dotenv()




class State(MessagesState):
    user: str
    followers: list
    repos: list
    messages: Annotated[list[AnyMessage], add_messages]





def get_github_user_followers(state: State) -> State:
    
    """
    Tool to get the followers of a GitHub user. 

    Args:
        user (str): The GitHub username.

    Returns:
        List: The followers of the GitHub user.
    """
    # pprint(state)
    userName: str = "Ali7-cell"
    response = requests.get(
        f"https://api.github.com/users/{userName}/followers")
    followers = response.json()
    # print(followers)
    return {"followers": followers}



def get_github_user_repos(state: State) -> State:
    """
    Tool to get the repositories of a GitHub user. 

    Args:
        user (str): The GitHub username.

    Returns:
        List: The repositories of the GitHub user.
    """
    # print(state)
    userName: str = "Ali7-cell"
    response = requests.get(f"https://api.github.com/users/{userName}/repos")
    repos = response.json()
    # print(repos)
    return {"repos": repos}


def get_github_user_info(state: State) -> State:
    """
    Tool to get the information of a GitHub user. 

    Args:
        user (str): The GitHub username.

    Returns:
        Dict: The information of the GitHub user.
    """
    # print(state)
    userName: str = "Ali7-cell"
    response = requests.get(f"https://api.github.com/users/{userName}")
    user_info = response.json()
    # pprint(user_info)
    # pprint(user_info)
    return {"user": user_info}


builder =  StateGraph(State)
builder.add_node("get_github_user_followers", get_github_user_followers)
builder.add_node("get_github_user_repos", get_github_user_repos)
builder.add_node("get_github_user_info", get_github_user_info)

builder.add_edge(START, "get_github_user_info")
builder.add_edge("get_github_user_info", "get_github_user_followers")
builder.add_edge("get_github_user_followers", "get_github_user_repos")
builder.add_edge("get_github_user_repos", END)


# memory = MemorySaver()
graph = builder.compile()



result =graph.invoke({"messages": [HumanMessage(content="what is my followers and repos")]
})

pprint(result.get("repos"))