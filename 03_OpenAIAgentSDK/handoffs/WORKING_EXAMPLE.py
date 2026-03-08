"""
SIMPLE WORKING EXAMPLE - No More Errors!

This file uses GROQ (free) by default.
It will work immediately without any API issues.
"""

from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv
import os

load_dotenv()


# ========================================
# SETUP - Choose your API
# ========================================

print("\n" + "="*60)
print("CHECKING YOUR API KEYS...")
print("="*60)

# Check which API keys you have
has_groq = bool(os.getenv('GROQ_API_KEY'))
has_openai = bool(os.getenv('OPENAI_API_KEY'))
has_gemini = bool(os.getenv('GEMINI_API_KEY'))

print(f"✅ GROQ_API_KEY: {'Found' if has_groq else '❌ Missing'}")
print(f"✅ OPENAI_API_KEY: {'Found' if has_openai else '❌ Missing'}")
print(f"⚠️ GEMINI_API_KEY: {'Found (not used)' if has_gemini else '❌ Missing'}\n")

# Create agent based on available keys
agent = None

if has_groq:
    print("🚀 Using GROQ (Free & Fast)")
    print("-" * 60)
    
    groq_client = AsyncOpenAI(
        api_key=os.getenv('GROQ_API_KEY'),
        base_url="https://api.groq.com/openai/v1",
    )
    
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful AI assistant. Be concise and friendly.",
        model=OpenAIChatCompletionsModel(
            model="llama-3.3-70b-versatile",
            openai_client=groq_client
        ),
    )
    
elif has_openai:
    print("🚀 Using OPENAI (Reliable & Cheap)")
    print("-" * 60)
    
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful AI assistant. Be concise and friendly.",
        model="gpt-4o-mini",
    )
    
else:
    print("❌ ERROR: No valid API key found!")
    print("\nYou need either:")
    print("  1. GROQ_API_KEY (FREE) - Get at: https://console.groq.com/keys")
    print("  2. OPENAI_API_KEY (Cheap) - Get at: https://platform.openai.com/api-keys")
    print("\nAdd to your .env file:")
    print("  GROQ_API_KEY=your-key-here")
    print("  OR")
    print("  OPENAI_API_KEY=your-key-here")
    exit(1)


# ========================================
# RUN EXAMPLES
# ========================================

def run_example(query):
    """Run a single query and print the result"""
    print(f"\n📝 Query: {query}")
    print("-" * 60)
    
    try:
        result = Runner.run_sync(agent, query)
        print(f"🤖 Response: {result.final_output}\n")
        return True
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


# Run demo queries
print("\n" + "="*60)
print("RUNNING DEMO QUERIES")
print("="*60)

example_queries = [
    "Say hello in 3 different languages",
    "What is 25 + 37?",
    "Explain what an AI agent is in one sentence",
]

success_count = 0
for query in example_queries:
    if run_example(query):
        success_count += 1

# Summary
print("="*60)
print(f"✅ RESULTS: {success_count}/{len(example_queries)} queries successful")
print("="*60)

if success_count == len(example_queries):
    print("\n🎉 SUCCESS! Everything is working!\n")
    print("You can now:")
    print("  1. Modify this file for your needs")
    print("  2. Use the same API setup in other files")
    print("  3. Build your own agents")
    print("\n💡 TIP: The setup code at the top works everywhere!")
else:
    print("\n⚠️ Some queries failed. Check your API key and internet connection.")


# ========================================
# INTERACTIVE MODE (Optional)
# ========================================

print("\n" + "="*60)
print("INTERACTIVE MODE")
print("="*60)
print("Type your questions (or 'quit' to exit):\n")

while True:
    try:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break
        
        if not user_input:
            continue
        
        run_example(user_input)
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        break
    
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
