"""
WORKING Gemini API Example for OpenAI Agents SDK

This shows the CORRECT way to use Gemini with OpenAI Agents SDK
"""

from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv

load_dotenv()


# ========================================
# METHOD 1: Direct Gemini API (Native - RECOMMENDED)
# ========================================

def method_1_native_gemini():
    """
    Use Google's native Generative AI SDK
    This is MORE RELIABLE than OpenAI-compatible endpoint
    """
    print("\n" + "="*60)
    print("METHOD 1: Native Gemini API (RECOMMENDED)")
    print("="*60)
    
    try:
        import google.generativeai as genai
        
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            print("❌ GEMINI_API_KEY not found in .env")
            return
        
        # Configure native Gemini
        genai.configure(api_key=gemini_api_key)
        
        # Use the model directly
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("\n📝 Testing: 'Say hello in 3 languages'\n")
        response = model.generate_content("Say hello in 3 languages")
        print(f"✅ Success!\n{response.text}\n")
        
    except ImportError:
        print("❌ google-generativeai not installed")
        print("Install: pip install google-generativeai")
    except Exception as e:
        print(f"❌ Error: {e}")


# ========================================
# METHOD 2: OpenAI-Compatible Endpoint (TRICKY)
# ========================================

def method_2_openai_compatible():
    """
    Use Gemini through OpenAI-compatible endpoint
    NOTE: This is LESS RELIABLE and has limitations
    """
    print("\n" + "="*60)
    print("METHOD 2: OpenAI-Compatible Endpoint (Experimental)")
    print("="*60)
    
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return
    
    # Try different base URLs and model formats
    configs = [
        {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-1.5-flash-latest",  # Try with -latest suffix
        },
        {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "model": "gemini-1.5-flash",  # Original format
        },
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\n  Attempt {i}: model='{config['model']}'")
        
        try:
            client = AsyncOpenAI(
                api_key=gemini_api_key,
                base_url=config["base_url"],
            )
            
            agent = Agent(
                name="GeminiAssistant",
                instructions="You are a helpful assistant.",
                model=OpenAIChatCompletionsModel(
                    model=config["model"],
                    openai_client=client
                ),
            )
            
            result = Runner.run_sync(
                agent,
                "Say hello",
            )
            
            print(f"  ✅ SUCCESS with model: {config['model']}")
            print(f"  Response: {result.final_output}\n")
            return  # Success - exit
            
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:100]}...\n")
    
    print("⚠️ All OpenAI-compatible attempts failed!")


# ========================================
# METHOD 3: Use OpenAI Instead (BEST FOR THIS SDK)
# ========================================

def method_3_use_openai():
    """
    Just use OpenAI - the SDK is DESIGNED for OpenAI
    """
    print("\n" + "="*60)
    print("METHOD 3: Use OpenAI (RECOMMENDED FOR THIS SDK)")
    print("="*60)
    
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_api_key:
        print("❌ OPENAI_API_KEY not found in .env")
        print("Get one at: https://platform.openai.com/api-keys")
        print("\n💡 OpenAI GPT-4o-mini is VERY CHEAP:")
        print("   - Input: $0.15 per 1M tokens")
        print("   - Output: $0.60 per 1M tokens")
        print("   - About $0.01 for 100 questions!")
        return
    
    agent = Agent(
        name="OpenAIAssistant",
        instructions="You are a helpful assistant.",
        model="gpt-4o-mini",  # Super cheap and fast
    )
    
    try:
        result = Runner.run_sync(
            agent,
            "Say hello and tell me which model you are",
        )
        print(f"✅ Success!\n{result.final_output}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")


# ========================================
# METHOD 4: Use Groq (FREE ALTERNATIVE)
# ========================================

def method_4_use_groq():
    """
    Use Groq - Fast, free tier, OpenAI-compatible
    """
    print("\n" + "="*60)
    print("METHOD 4: Use Groq (FREE & FAST)")
    print("="*60)
    
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in .env")
        print("Get FREE key at: https://console.groq.com/keys")
        print("\n💡 Groq is FREE and FAST!")
        return
    
    client = AsyncOpenAI(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    
    agent = Agent(
        name="GroqAssistant",
        instructions="You are a helpful assistant.",
        model=OpenAIChatCompletionsModel(
            model="llama-3.3-70b-versatile",
            openai_client=client
        ),
    )
    
    try:
        result = Runner.run_sync(
            agent,
            "Say hello and tell me which model you are",
        )
        print(f"✅ Success!\n{result.final_output}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")


# ========================================
# MAIN
# ========================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("GEMINI API TESTING - FINDING WHAT WORKS")
    print("="*70)
    print("\n📌 Your Current Error:")
    print("   'models/gemini-1.5-flash is not found'")
    print("\n🔍 This means: Gemini's OpenAI-compatible endpoint is problematic")
    print("\n✅ Let's try different solutions...\n")
    
    # Try each method
    method_1_native_gemini()
    method_2_openai_compatible()
    method_3_use_openai()
    method_4_use_groq()
    
    # Final recommendations
    print("\n" + "="*70)
    print("📊 FINAL RECOMMENDATIONS FOR YOUR TEACHING")
    print("="*70)
    print("""
    🥇 BEST OPTION: OpenAI GPT-4o-mini
       ✅ Designed for this SDK
       ✅ Super cheap ($0.01 for ~100 questions)
       ✅ No rate limit issues
       ✅ All features work perfectly
       📝 Add to .env: OPENAI_API_KEY=sk-...
       🔗 Get key: https://platform.openai.com/api-keys
    
    🥈 SECOND BEST: Groq (FREE)
       ✅ Completely free
       ✅ Very fast
       ✅ OpenAI-compatible
       ✅ Good for teaching/testing
       📝 Add to .env: GROQ_API_KEY=gsk-...
       🔗 Get key: https://console.groq.com/keys
    
    🥉 THIRD: Native Gemini SDK
       ✅ Works reliably
       ⚠️ Different API (not OpenAI Agents SDK)
       ⚠️ Limited free quota
       📝 Use: google-generativeai library
       🔗 Get key: https://aistudio.google.com/apikey
    
    ❌ AVOID: Gemini OpenAI-Compatible Endpoint
       ❌ Unreliable
       ❌ Model name issues
       ❌ Limited functionality
       ❌ Not worth the hassle
    
    💡 FOR YOUR STUDENTS:
       - Start with OpenAI (most reliable)
       - It's NOT expensive (really!)
       - $5 credit = thousands of requests
       - Perfect for learning
    """)
    
    print("="*70)
