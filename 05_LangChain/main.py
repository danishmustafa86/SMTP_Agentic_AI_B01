from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()



llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    # base_url="https://api.groq.com/openai/v1"
)


query = input("Enter your query: ")

response = llm.invoke(query)

print(response.content)