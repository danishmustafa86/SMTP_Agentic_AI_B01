from agents import Agent, Runner
from dotenv import load_dotenv
import os
import sys
import logging

# --- FIX 1: DISABLE TRACING (Stops the 401 Errors) ---
# We disable the logger that prints the "tracing" errors
logging.getLogger("agents.telemetry").setLevel(logging.CRITICAL)

load_dotenv()

# --- FIX 2: USE A MORE STABLE MODEL FOR TOOLS ---
# Mixtral is often more robust with the Agents SDK than Llama 3
# If this still fails, try: "llama3-70b-8192"
FREE_MODEL = "mixtral-8x7b-32768"

print(f"Using Model: {FREE_MODEL}")
print(f"Connecting to: {os.getenv('OPENAI_BASE_URL')}")

# --- DEFINE AGENTS ---

urdu_agent = Agent(
    name="UrduAgent",
    instructions="You are a translation tool. Output only the Urdu translation.",
    model=FREE_MODEL
)

arabic_agent = Agent(
    name="ArabicAgent",
    instructions="You are a translation tool. Output only the Arabic translation.",
    model=FREE_MODEL
)

# --- ORCHESTRATOR ---

agent = Agent(
    name="Orchestrator",
    # We add explicit instructions to force correct tool usage
    instructions=(
        "You are a helpful translator. "
        "To translate text, you MUST call the provided tools. "
        "Do not try to translate it yourself. "
        "Do not use XML tags. Use standard function calling."
    ),
    model=FREE_MODEL,
    tools=[
        # We simplify the tool names to make it easier for the model
        urdu_agent.as_tool(
            tool_name="translate_to_urdu",
            tool_description="Translates English text to Urdu."
        ),
        arabic_agent.as_tool(
            tool_name="translate_to_arabic",
            tool_description="Translates English text to Arabic."
        )
    ]
)

# --- RUN ---
# We use a loop to let you try multiple times without restarting
if __name__ == "__main__":
    while True:
        try:
            user_input = input("\nEnter text (or 'q' to quit): ")
            if user_input.lower() == 'q': break
            
            # Using run_sync to execute the agent
            result = Runner.run_sync(agent, user_input)
            print(f"\nFinal Result: {result.final_output}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Tip: If you see 'MaxTurnsExceeded', the model is struggling to pick the right tool.")