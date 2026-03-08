import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    # Define what the agent is allowed to do
    options = ClaudeAgentOptions(
        # model="claude-3-5-sonnet",  # Use 3.5 Sonnet (claude-3-5-haiku is retired)
        system_prompt="You are a helpful assistant that can write files, and search the web.",
        allowed_tools=["Write", "web_search"],  # Give it permission to write to disk
        permission_mode="acceptEdits" # Auto-approve changes (careful!)
    )

    print("--- Starting Hello World Agent ---")
    
    # The 'query' function starts the agentic loop
    async for message in query(
        prompt=input("What do you want to do?"),
        options=options
    ):
        # The SDK streams updates. We can print the text blocks as they arrive.
        if hasattr(message, 'content'):
            for block in message.content:
                if hasattr(block, 'text'):
                    print(block.text, end="", flush=True)

    print("\n--- Task Complete! Check your folder for hello.txt ---")

if __name__ == "__main__":
    asyncio.run(main())