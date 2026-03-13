from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatOpenAI(
    model="mistral-7b-instruct",
    api_key="AIML_API_KEY",
    base_url="https://api.aimlapi.com/v1",
    temperature=0.5,
)

# Memory stores the full chat history
memory = ConversationBufferMemory()

# ConversationChain automatically uses memory
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

# Multi-turn conversation
print(conversation.predict(input="Hi! My name is Ali."))
print(conversation.predict(input="What's my name?"))  # LLM remembers "Ali"
print(conversation.predict(input="Tell me a joke about Python."))