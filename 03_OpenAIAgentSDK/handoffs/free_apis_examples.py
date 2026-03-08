"""
Free API Examples - Quick Reference
Get keys from the URLs in each example
"""

from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# 1. GROQ (FREE) - https://console.groq.com/keys
# ============================================
def example_groq():
    client = AsyncOpenAI(
        api_key=os.getenv('GROQ_API_KEY'),
        base_url="https://api.groq.com/openai/v1",
    )
    
    agent = Agent(
        name="GroqAgent",
        instructions="You are helpful",
        model=OpenAIChatCompletionsModel(
            model="llama-3.3-70b-versatile",
            openai_client=client
        ),
    )
    
    result = Runner.run_sync(agent, "Say hi")
    print(result.final_output)


# ============================================
# 2. AI/ML API (FREE) - https://aimlapi.com/
# ============================================
def example_aiml():
    client = AsyncOpenAI(
        api_key=os.getenv('AIML_API_KEY'),
        base_url="https://api.aimlapi.com/v1",
    )
    
    agent = Agent(
        name="AIMLAgent",
        instructions="You are helpful",
        model=OpenAIChatCompletionsModel(
            model="gpt-4o-mini",  # or other models from their list
            openai_client=client
        ),
    )
    
    result = Runner.run_sync(agent, "Say hi")
    print(result.final_output)


# ============================================
# 3. TOGETHER AI (FREE) - https://api.together.xyz/
# ============================================
def example_together():
    client = AsyncOpenAI(
        api_key=os.getenv('TOGETHER_API_KEY'),
        base_url="https://api.together.xyz/v1",
    )
    
    agent = Agent(
        name="TogetherAgent",
        instructions="You are helpful",
        model=OpenAIChatCompletionsModel(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            openai_client=client
        ),
    )
    
    result = Runner.run_sync(agent, "Say hi")
    print(result.final_output)


# ============================================
# 4. DEEPSEEK (CHEAP) - https://platform.deepseek.com/
# ============================================
def example_deepseek():
    client = AsyncOpenAI(
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com/v1",
    )
    
    agent = Agent(
        name="DeepSeekAgent",
        instructions="You are helpful",
        model=OpenAIChatCompletionsModel(
            model="deepseek-chat",
            openai_client=client
        ),
    )
    
    result = Runner.run_sync(agent, "Say hi")
    print(result.final_output)


# ============================================
# 5. OPENROUTER (FREE TIER) - https://openrouter.ai/
# ============================================
def example_openrouter():
    client = AsyncOpenAI(
        api_key=os.getenv('OPENROUTER_API_KEY'),
        base_url="https://openrouter.ai/api/v1",
    )
    
    agent = Agent(
        name="OpenRouterAgent",
        instructions="You are helpful",
        model=OpenAIChatCompletionsModel(
            model="meta-llama/llama-3.2-3b-instruct:free",  # Free models
            openai_client=client
        ),
    )
    
    result = Runner.run_sync(agent, "Say hi")
    print(result.final_output)


# ============================================
# 6. ANTHROPIC (PAID) - https://console.anthropic.com/
# ============================================
# Note: Anthropic doesn't have OpenAI-compatible endpoint
# Use their native SDK instead:
def example_anthropic_native():
    # pip install anthropic
    import anthropic
    
    client = anthropic.Anthropic(
        api_key=os.getenv('ANTHROPIC_API_KEY')
    )
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Say hi"}]
    )
    
    print(message.content[0].text)


# ============================================
# 7. GEMINI (FREE LIMITED) - Native SDK
# ============================================
def example_gemini_native():
    # pip install google-generativeai
    import google.generativeai as genai
    
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content("Say hi")
    print(response.text)


# ============================================
# .env FILE FORMAT
# ============================================
"""
GROQ_API_KEY=gsk-...
AIML_API_KEY=...
TOGETHER_API_KEY=...
DEEPSEEK_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-v1-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
"""


# RUN EXAMPLE
if __name__ == "__main__":
    print("Testing free APIs...\n")
    
    # Uncomment the one you want to test:
    example_groq()
    # example_aiml()
    # example_together()
    # example_deepseek()
    # example_openrouter()
    # example_anthropic_native()
    # example_gemini_native()
