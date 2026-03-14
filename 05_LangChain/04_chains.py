from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)


# ── 1. Prompt with a slot for chat history ────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("chat_history"),   # past messages injected here
    ("human", "{input}"),
])

# ── 2. Base LCEL chain (no memory yet) ───────────────────────────────────────
chain = prompt | llm | StrOutputParser()


# ── 3. Per-session history store (replaces ConversationBufferMemory) ──────────
store = {}

def get_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# ── 4. Wrap chain with memory (replaces ConversationChain) ────────────────────
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


# ── 5. Multi-turn conversation ────────────────────────────────────────────────
config = {"configurable": {"session_id": "user_1"}}

print(chain_with_memory.invoke({"input": "Hi! My name is Ali."}, config=config))
print(chain_with_memory.invoke({"input": "What's my name?"}, config=config))   # remembers "Ali"
print(chain_with_memory.invoke({"input": "Tell me a joke about Python."}, config=config))



























# from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
# import os

# load_dotenv()

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     api_key=os.getenv("AIMLAPI_API_KEY"),
#     base_url="http://api.aimlapi.com/v1"
# )

# prompt = ChatPromptTemplate.from_template(
#     "Explain {topic} in simple words."
# )

# parser = StrOutputParser()

# chain = prompt | llm | parser

# result = chain.invoke({"topic": "Machine Learning"})
# print(result)
