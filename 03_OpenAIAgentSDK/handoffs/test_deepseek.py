from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv
import os

load_dotenv()


client = AsyncOpenAI(
    api_key=os.getenv("AIML_API_KEY"),
    base_url="https://api.aimlapi.com/v1"
)

agent = Agent(
    name="QuizGenerator",
    instructions = "Your are a helpful quiz generator. You will generate quizzes based of user quries.",
    model = OpenAIChatCompletionsModel(
        model="gpt-4o-mini",
        openai_client=client
    )
)

query = input("Enter your query: ")
result = Runner.run_sync(agent, query)
print(result.final_output)



















# # DeepSeek - https://platform.deepseek.com/
# from openai import AsyncOpenAI
# from agents import Agent, OpenAIChatCompletionsModel, Runner
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = AsyncOpenAI(
#     api_key=os.getenv('DEEPSEEK_API_KEY'),
#     base_url="https://api.deepseek.com/v1",
# )

# agent = Agent(
#     name="DeepSeekAgent",
#     instructions="You are helpful",
#     model=OpenAIChatCompletionsModel(
#         model="deepseek-chat",
#         openai_client=client
#     ),
# )

# query = input("Enter query: ")
# result = Runner.run_sync(agent, query)
# print(result.final_output)
