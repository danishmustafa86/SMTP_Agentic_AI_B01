from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()


# Hi danish
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("http://api.aimlapi.com")
    )

response = llm.invoke("Explain what is AI in simple words")

print(response.content)