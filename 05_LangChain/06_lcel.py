from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)

parser = StrOutputParser()


# ── 1. Basic LCEL chain ── prompt | llm | parser ─────────────────────────────
prompt = ChatPromptTemplate.from_template("Translate '{text}' to {language}.")
chain = prompt | llm | parser

print(chain.invoke({"text": "Good morning", "language": "French"}))


# ── 2. RunnablePassthrough ── passes input as-is to next step ─────────────────
prompt2 = ChatPromptTemplate.from_template("Tell me a joke about {topic}.")
chain2 = {"topic": RunnablePassthrough()} | prompt2 | llm | parser

print(chain2.invoke("cats"))


# ── 3. RunnableLambda ── wrap any Python function as a runnable step ──────────
shout = RunnableLambda(lambda text: text.upper() + " !!!")
chain3 = prompt | llm | parser | shout

print(chain3.invoke({"text": "hello", "language": "Spanish"}))


# ── 4. RunnableParallel ── run multiple chains at the same time ───────────────
prompt_joke = ChatPromptTemplate.from_template("Short joke about {topic}.")
prompt_fact = ChatPromptTemplate.from_template("One fun fact about {topic}.")

parallel_chain = RunnableParallel(
    joke=(prompt_joke | llm | parser),
    fact=(prompt_fact | llm | parser),
)

result = parallel_chain.invoke({"topic": "dogs"})
print("Joke:", result["joke"])
print("Fact:", result["fact"])
