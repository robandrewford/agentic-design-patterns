import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    from google.adk.agents import Agent, ParallelAgent

    # It's better to define the fetching logic as tools for the agents
    # For simplicity in this example, we'll embed the logic in the agent's instruction.
    # In a real-world scenario, you would use tools.

    # Define the individual agents that will run in parallel
    weather_fetcher = Agent(
        name="weather_fetcher",
        model="gemini-2.0-flash-exp",
        instruction="Fetch the weather for the given location and return only the weather report.",
        output_key="weather_data"  # The result will be stored in session.state["weather_data"]
    )

    news_fetcher = Agent(
        name="news_fetcher",
        model="gemini-2.0-flash-exp",
        instruction="Fetch the top news story for the given topic and return only that story.",
        output_key="news_data"      # The result will be stored in session.state["news_data"]
    )

    # Create the ParallelAgent to orchestrate the sub-agents
    data_gatherer = ParallelAgent(
        name="data_gatherer",
        sub_agents=[
            weather_fetcher,
            news_fetcher
        ]
    )

    # To run this, you would use the ADK's Runner, which manages state and execution.
    # The following is a conceptual example of how it would be invoked.

    # from google.adk.runners import Runner
    # from google.adk.sessions import InMemorySessionService

    # # Setup runner and session
    # runner = Runner(agent=data_gatherer, session_service=InMemorySessionService())

    # # Execute the agent
    # async for event in runner.run_async(
    #     new_message="Get weather for Mountain View and news on technology"
    # ):
    #     if event.is_final_response():
    #         # The results are now in the session state
    #         final_state = runner.get_session().state
    #         print("\n--- Gathered Data ---")
    #         print(f"Weather: {final_state.get('weather_data')}")
    #         print(f"News: {final_state.get('news_data')}")
    return


if __name__ == "__main__":
    app.run()
