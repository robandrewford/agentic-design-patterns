import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import asyncio
    from typing import AsyncGenerator
    from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
    from google.adk.events import Event, EventActions
    from google.adk.agents.invocation_context import InvocationContext

    # Best Practice: Define custom agents as complete, self-describing classes.
    class ConditionChecker(BaseAgent):
        """A custom agent that checks for a 'completed' status in the session state."""
        name: str = "ConditionChecker"
        description: str = "Checks if a process is complete and signals the loop to stop."

        async def _run_async_impl(
            self, context: InvocationContext
        ) -> AsyncGenerator[Event, None]:
            """Checks state and yields an event to either continue or stop the loop."""
            status = context.session.state.get("status", "pending")
            is_done = (status == "completed")

            if is_done:
                # Escalate to terminate the loop when the condition is met.
                yield Event(author=self.name, actions=EventActions(escalate=True))
            else:
                # Yield a simple event to continue the loop.
                yield Event(author=self.name, content="Condition not met, continuing loop.")

    # Correction: The LlmAgent must have a model and clear instructions.
    process_step = LlmAgent(
        name="ProcessingStep",
        model="gemini-2.0-flash-exp",
        instruction="You are a step in a longer process. Perform your task. If you are the final step, update session state by setting 'status' to 'completed'."
    )

    # The LoopAgent orchestrates the workflow.
    poller = LoopAgent(
        name="StatusPoller",
        max_iterations=10,
        sub_agents=[
            process_step,
            ConditionChecker() # Instantiating the well-defined custom agent.
        ]
    )

    # This poller will now execute 'process_step' and then 'ConditionChecker'
    # repeatedly until the status is 'completed' or 10 iterations have passed.
    return


if __name__ == "__main__":
    app.run()
