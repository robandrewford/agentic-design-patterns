import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    # pip install crewai langchain-openai

    import os
    from crewai import Agent, Task, Crew
    from crewai.tools import tool
    import logging

    # --- Best Practice: Configure Logging ---
    # A basic logging setup helps in debugging and tracking the crew's execution.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # --- Set up your API Key ---
    # For production, it's recommended to use a more secure method for key management
    # like environment variables loaded at runtime or a secret manager.
    #
    # Set the environment variable for your chosen LLM provider (e.g., OPENAI_API_KEY)
    # os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
    # os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"


    # --- 1. Refactored Tool: Returns Clean Data ---
    # The tool now returns raw data (a float) or raises a standard Python error.
    # This makes it more reusable and forces the agent to handle outcomes properly.
    @tool("Stock Price Lookup Tool")
    def get_stock_price(ticker: str) -> float:
        """
        Fetches the latest simulated stock price for a given stock ticker symbol.
        Returns the price as a float. Raises a ValueError if the ticker is not found.
        """
        logging.info(f"Tool Call: get_stock_price for ticker '{ticker}'")
        simulated_prices = {
            "AAPL": 178.15,
            "GOOGL": 1750.30,
            "MSFT": 425.50,
        }
        price = simulated_prices.get(ticker.upper())

        if price is not None:
            return price
        else:
            # Raising a specific error is better than returning a string.
            # The agent is equipped to handle exceptions and can decide on the next action.
            raise ValueError(f"Simulated price for ticker '{ticker.upper()}' not found.")


    # --- 2. Define the Agent ---
    # The agent definition remains the same, but it will now leverage the improved tool.
    financial_analyst_agent = Agent(
      role='Senior Financial Analyst',
      goal='Analyze stock data using provided tools and report key prices.',
      backstory="You are an experienced financial analyst adept at using data sources to find stock information. You provide clear, direct answers.",
      verbose=True,
      tools=[get_stock_price],
      # Allowing delegation can be useful, but is not necessary for this simple task.
      allow_delegation=False,
    )

    # --- 3. Refined Task: Clearer Instructions and Error Handling ---
    # The task description is more specific and guides the agent on how to react
    # to both successful data retrieval and potential errors.
    analyze_aapl_task = Task(
      description=(
          "What is the current simulated stock price for Apple (ticker: AAPL)? "
          "Use the 'Stock Price Lookup Tool' to find it. "
          "If the ticker is not found, you must report that you were unable to retrieve the price."
      ),
      expected_output=(
          "A single, clear sentence stating the simulated stock price for AAPL. "
          "For example: 'The simulated stock price for AAPL is $178.15.' "
          "If the price cannot be found, state that clearly."
      ),
      agent=financial_analyst_agent,
    )

    # --- 4. Formulate the Crew ---
    # The crew orchestrates how the agent and task work together.
    financial_crew = Crew(
      agents=[financial_analyst_agent],
      tasks=[analyze_aapl_task],
      verbose=True # Set to False for less detailed logs in production
    )

    # --- 5. Run the Crew within a Main Execution Block ---
    # Using a __name__ == "__main__": block is a standard Python best practice.
    def main():
        """Main function to run the crew."""
        # Check for API key before starting to avoid runtime errors.
        if not os.environ.get("OPENAI_API_KEY"):
            print("ERROR: The OPENAI_API_KEY environment variable is not set.")
            print("Please set it before running the script.")
            return

        print("\n## Starting the Financial Crew...")
        print("---------------------------------")

        # The kickoff method starts the execution.
        result = financial_crew.kickoff()

        print("\n---------------------------------")
        print("## Crew execution finished.")
        print("\nFinal Result:\n", result)

    if __name__ == "__main__":
        main()
    return


if __name__ == "__main__":
    app.run()
