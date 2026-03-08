# Input guardrails: blocking vs parallel execution.
# Blocking (run_in_parallel=False): guardrail runs first; if it trips, the agent never runs (no token spend).
# Parallel (run_in_parallel=True, default): guardrail runs alongside the agent; lower latency but agent may run before trip.

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)


@input_guardrail(run_in_parallel=False)
def blocking_guardrail(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """Runs before the agent. Tripping here means the main agent is never invoked."""
    text = input if isinstance(input, str) else ""
    triggered = "blocked_keyword" in (text or "").lower()
    return GuardrailFunctionOutput(output_info=None, tripwire_triggered=triggered)


@input_guardrail(run_in_parallel=True)
def parallel_guardrail(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """Runs concurrently with the agent. Good for non-critical checks; agent may already be running when this trips."""
    text = input if isinstance(input, str) else ""
    triggered = "parallel_block" in (text or "").lower()
    return GuardrailFunctionOutput(output_info=None, tripwire_triggered=triggered)


agent = Agent(
    name="InputModesAgent",
    instructions="Reply in one short sentence.",
    input_guardrails=[blocking_guardrail, parallel_guardrail],
)


async def main():
    # Normal input: both guardrails pass
    r = await Runner.run(agent, "What is the capital of France?")
    print("Normal:", r.final_output)

    # Blocking guardrail trips: agent never runs
    try:
        await Runner.run(agent, "Tell me about blocked_keyword please")
        print("Unexpected: no trip")
    except InputGuardrailTripwireTriggered:
        print("Blocking guardrail tripped (agent did not run)")

    # Parallel guardrail trips
    try:
        await Runner.run(agent, "Explain parallel_block to me")
        print("Unexpected: no trip")
    except InputGuardrailTripwireTriggered:
        print("Parallel guardrail tripped")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
