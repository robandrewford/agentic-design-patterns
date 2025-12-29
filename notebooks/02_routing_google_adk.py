import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    # Copyright (c) 2025 Marco Fago
    #
    # This code is licensed under the MIT License.
    # See the LICENSE file in the repository for the full license text.

    import uuid
    from typing import Dict, Any, Optional

    from google.adk.agents import Agent
    from google.adk.runners import InMemoryRunner
    from google.adk.tools import FunctionTool
    from google.genai import types
    from google.adk.events import Event

    # --- Define Tool Functions ---
    # These functions simulate the actions of the specialist agents.

    def booking_handler(request: str) -> str:
        """
        Handles booking requests for flights and hotels.
        Args:
            request: The user's request for a booking.
        Returns:
            A confirmation message that the booking was handled.
        """
        print("-------------------------- Booking Handler Called ----------------------------")
        return f"Booking action for '{request}' has been simulated."

    def info_handler(request: str) -> str:
        """
        Handles general information requests.
        Args:
            request: The user's question.
        Returns:
            A message indicating the information request was handled.
        """
        print("-------------------------- Info Handler Called ----------------------------")
        return f"Information request for '{request}'. Result: Simulated information retrieval."

    def unclear_handler(request: str) -> str:
        """Handles requests that couldn't be delegated."""
        return f"Coordinator could not delegate request: '{request}'. Please clarify."

    # --- Create Tools from Functions ---
    booking_tool = FunctionTool(booking_handler)
    info_tool = FunctionTool(info_handler)

    # Define specialized sub-agents equipped with their respective tools
    booking_agent = Agent(
        name="Booker",
        model="gemini-2.0-flash",
        description="A specialized agent that handles all flight and hotel booking requests by calling the booking tool.",
        tools=[booking_tool]
    )

    info_agent = Agent(
        name="Info",
        model="gemini-2.0-flash",
        description="A specialized agent that provides general information and answers user questions by calling the info tool.",
        tools=[info_tool]
    )

    # Define the parent agent with explicit delegation instructions
    coordinator = Agent(
        name="Coordinator",
        model="gemini-2.0-flash",
        instruction=(
            "You are the main coordinator. Your only task is to analyze incoming user requests "
            "and delegate them to the appropriate specialist agent. Do not try to answer the user directly.\n"
            "- For any requests related to booking flights or hotels, delegate to the 'Booker' agent.\n"
            "- For all other general information questions, delegate to the 'Info' agent."
        ),
        description="A coordinator that routes user requests to the correct specialist agent.",
        # The presence of sub_agents enables LLM-driven delegation (Auto-Flow) by default.
        sub_agents=[booking_agent, info_agent]
    )

    # --- Execution Logic ---

    def run_coordinator(runner: InMemoryRunner, request: str):
        """Runs the coordinator agent with a given request and delegates."""
        print(f"\n--- Running Coordinator with request: '{request}' ---")
        final_result = ""
        try:
            user_id = "user_123"
            session_id = str(uuid.uuid4())
            runner.session_service.create_session(
                app_name=runner.app_name, user_id=user_id, session_id=session_id
            )

            for event in runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=types.Content(
                    role='user',
                    parts=[types.Part(text=request)]
                ),
            ):
                if event.is_final_response() and event.content:
                    # Try to get text directly from event.content to avoid iterating parts
                    if hasattr(event.content, 'text') and event.content.text:
                         final_result = event.content.text
                    elif event.content.parts:
                        # Fallback: Iterate through parts and extract text (might trigger warning)
                        text_parts = [part.text for part in event.content.parts if part.text]
                        final_result = "".join(text_parts)
                    # Assuming the loop should break after the final response
                    break

            print(f"Coordinator Final Response: {final_result}")
            return final_result
        except Exception as e:
            print(f"An error occurred while processing your request: {e}")
            return f"An error occurred while processing your request: {e}"

    def main():
        """Main function to run the ADK example."""
        print("--- Google ADK Routing Example (ADK Auto-Flow Style) ---")
        print("Note: This requires Google ADK installed and authenticated.")

        runner = InMemoryRunner(coordinator)
        # Example Usage
        result_a = run_coordinator(runner, "Book me a hotel in Paris.")
        print(f"Final Output A: {result_a}")
        result_b = run_coordinator(runner, "What is the highest mountain in the world?")
        print(f"Final Output B: {result_b}")
        result_c = run_coordinator(runner, "Tell me a random fact.") # Should go to Info
        print(f"Final Output C: {result_c}")
        result_d = run_coordinator(runner, "Find flights to Tokyo next month.") # Should go to Booker
        print(f"Final Output D: {result_d}")


    if __name__ == "__main__":
        main()
    return


if __name__ == "__main__":
    app.run()
