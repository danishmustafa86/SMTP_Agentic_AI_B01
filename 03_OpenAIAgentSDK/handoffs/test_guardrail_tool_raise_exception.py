# Tool guardrails: allow, reject_content, and raise_exception.
# raise_exception halts the whole run and raises ToolInputGuardrailTripwireTriggered or ToolOutputGuardrailTripwireTriggered.

import json
from agents import (
    Agent,
    Runner,
    ToolGuardrailFunctionOutput,
    ToolInputGuardrailTripwireTriggered,
    ToolOutputGuardrailTripwireTriggered,
    function_tool,
    tool_input_guardrail,
    tool_output_guardrail,
)


@tool_input_guardrail
def block_forbidden_input(data) -> ToolGuardrailFunctionOutput:
    """Reject bad args with a message; for critical violations use raise_exception to stop the run."""
    args = json.loads(data.context.tool_arguments or "{}")
    if args.get("text", "").strip().lower() == "halt":
        return ToolGuardrailFunctionOutput.raise_exception(output_info="forbidden_input")
    if "reject_me" in args.get("text", "").lower():
        return ToolGuardrailFunctionOutput.reject_content("Input not allowed; try something else.")
    return ToolGuardrailFunctionOutput.allow()


@tool_output_guardrail
def block_forbidden_output(data) -> ToolGuardrailFunctionOutput:
    """If tool returns a forbidden string, halt the run with raise_exception."""
    out = str(data.output or "")
    if "secret-result" in out.lower():
        return ToolGuardrailFunctionOutput.raise_exception(output_info="sensitive_output")
    return ToolGuardrailFunctionOutput.allow()


@function_tool(
    tool_input_guardrails=[block_forbidden_input],
    tool_output_guardrails=[block_forbidden_output],
)
def echo_tool(text: str) -> str:
    """Echo the user message. Used to demonstrate tool guardrail behaviors."""
    return text


agent = Agent(
    name="EchoAgent",
    instructions="Use the echo_tool when the user asks to echo or repeat something. Otherwise answer briefly.",
    tools=[echo_tool],
)


def main():
    # Allow: normal flow
    r = Runner.run_sync(agent, "Echo: hello")
    print("Allow:", r.final_output)

    # reject_content: tool call is replaced with message; run continues
    r = Runner.run_sync(agent, "Echo: reject_me please")
    print("Reject content (run continued):", r.final_output)

    # raise_exception on input: run halts, ToolInputGuardrailTripwireTriggered
    try:
        Runner.run_sync(agent, "Echo: halt")
        print("Unexpected: no exception")
    except ToolInputGuardrailTripwireTriggered as e:
        print("Tool input raise_exception:", e.output.output_info)

    # raise_exception on output: tool returns "secret-result", output guardrail halts run
    try:
        Runner.run_sync(agent, "Echo: secret-result")
        print("Unexpected: no exception")
    except ToolOutputGuardrailTripwireTriggered as e:
        print("Tool output raise_exception:", e.output.output_info)

    print("Done.")


if __name__ == "__main__":
    main()
