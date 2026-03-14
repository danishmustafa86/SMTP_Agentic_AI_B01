from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("AIMLAPI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)


# # ── 1. StrOutputParser ── returns plain text string ──────────────────────────
prompt = ChatPromptTemplate.from_template("Tell me one fact about {topic}.")
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"topic": "Python"}))


# ── 2. JsonOutputParser ── returns a Python dict ─────────────────────────────
# json_parser = JsonOutputParser()
# prompt2 = ChatPromptTemplate.from_template(
#     "Return a JSON with 'name' and 'capital' for {country}. Return ONLY valid JSON."
# )
# chain2 = prompt2 | llm | json_parser

# print(chain2.invoke({"country": "France"}))


# ── 3. PydanticOutputParser ── structured + validated output ─────────────────
# class Country(BaseModel):
#     name: str = Field(description="Country name")
#     capital: str = Field(description="Capital city")
#     population: int = Field(description="Approximate population")

# pydantic_parser = JsonOutputParser(pydantic_object=Country)

# prompt3 = ChatPromptTemplate.from_template(
#     "Give info about {country}.\n{format_instructions}"
# )
# chain3 = prompt3 | llm | pydantic_parser

# result = chain3.invoke({
#     "country": "Japan",
#     "format_instructions": pydantic_parser.get_format_instructions(),
# })
# print(result)
