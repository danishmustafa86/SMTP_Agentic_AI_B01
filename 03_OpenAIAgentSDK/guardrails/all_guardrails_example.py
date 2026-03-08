"""
Learning example: Input, Output, and Tool guardrails in one agent.
Shows run_in_parallel=True vs False and minimal patterns.
"""
import json
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    ToolGuardrailFunctionOutput,
    function_tool,
    input_guardrail,
    output_guardrail,
    tool_input_guardrail,
    tool_output_guardrail,
)

# --- Output schema for the main agent ---
class Reply(BaseModel):
    response: str


# --- 1) INPUT GUARDRAILS (run on user input) ---

# Sequential: runs before the agent (run_in_parallel=False). Use for must-pass checks.
@input_guardrail(run_in_parallel=False)
def block_empty(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """Reject empty or whitespace-only input."""
    text = input if isinstance(input, str) else ""
    triggered = not text or not text.strip()
    return GuardrailFunctionOutput(output_info=None, tripwire_triggered=triggered)


# Parallel: runs alongside the agent (run_in_parallel=True, default). Use when check is independent.
@input_guardrail(run_in_parallel=True)
def block_off_topic(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """Simple keyword check: trip if input looks like spam."""
    text = (input if isinstance(input, str) else "").lower()
    triggered = "buy crypto" in text
    return GuardrailFunctionOutput(output_info=None, tripwire_triggered=triggered)


# --- 2) OUTPUT GUARDRAIL (run on agent's final reply) ---
@output_guardrail
def no_secrets_in_reply(ctx: RunContextWrapper, agent: Agent, output: Reply) -> GuardrailFunctionOutput:
    """Trip if the agent's response contains secret-like tokens."""
    text = (output.response or "").lower()
    triggered = "sk-" in text or "password" in text
    return GuardrailFunctionOutput(output_info=None, tripwire_triggered=triggered)


# --- 3) TOOL GUARDRAILS (run on tool input/output) ---
@tool_input_guardrail
def no_secrets_in_tool_args(data) -> ToolGuardrailFunctionOutput:
    """Reject tool calls that include secret-looking args."""
    args = json.loads(data.context.tool_arguments or "{}")
    if "sk-" in json.dumps(args).lower():
        return ToolGuardrailFunctionOutput.reject_content("Secrets not allowed in tool input.")
    return ToolGuardrailFunctionOutput.allow()


@tool_output_guardrail
def no_secrets_in_tool_output(data) -> ToolGuardrailFunctionOutput:
    """Redact or reject tool output that looks like secrets."""
    text = str(data.output or "")
    if "sk-" in text:
        return ToolGuardrailFunctionOutput.reject_content("Tool output contained sensitive data.")
    return ToolGuardrailFunctionOutput.allow()


@function_tool(
    tool_input_guardrails=[no_secrets_in_tool_args],
    tool_output_guardrails=[no_secrets_in_tool_output],
)
def echo(msg: str) -> str:
    """Echo the message. Used to demonstrate tool guardrails."""
    return msg


# --- Agent: wire all guardrails and the tool ---
agent = Agent(
    name="Support",
    instructions="Answer briefly. Use the echo tool only when the user asks to repeat something.",
    input_guardrails=[block_empty, block_off_topic],
    output_guardrails=[no_secrets_in_reply],
    output_type=Reply,
    tools=[echo],
)


async def main():
    # Safe input → normal run
    try:
        r = await Runner.run(agent, "What is 2+2?")
        print("Reply:", r.final_output.response)
    except InputGuardrailTripwireTriggered:
        print("Input guardrail tripped")
    except OutputGuardrailTripwireTriggered:
        print("Output guardrail tripped")

    # Input guardrail (empty)
    try:
        await Runner.run(agent, "   ")
        print("Unexpected: no trip")
    except InputGuardrailTripwireTriggered:
        print("Input guardrail tripped (empty)")

    # Input guardrail (off-topic keyword)
    try:
        await Runner.run(agent, "buy crypto now!")
        print("Unexpected: no trip")
    except InputGuardrailTripwireTriggered:
        print("Input guardrail tripped (off-topic)")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
