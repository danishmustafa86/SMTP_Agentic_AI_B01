from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()






groq_api_key = os.getenv('GROQ_API_KEY')
groq_client = AsyncOpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)
agent = Agent(
    name="QuizAgent",
    instructions="You are a Quiz Agent. You generate quizzes",
    model=OpenAIChatCompletionsModel(
        model="llama-3.3-70b-versatile",
        openai_client=groq_client
    ),
    # output_type=Quiz
)


query = input("Enter the query: ")
result = Runner.run_sync(
    agent,
    query,
)
print(result.final_output)