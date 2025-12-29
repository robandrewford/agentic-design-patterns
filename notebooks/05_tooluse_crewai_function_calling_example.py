import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import os
    import logging
    from crewai import Agent, Task, Crew
    from crewai.tools import tool
    
    # Use utils for OpenRouter
    from utils import get_openrouter_model

    # --- Configuration ---
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize LLM via OpenRouter
    try:
        # CrewAI works well with LangChain LLM objects
        llm = get_openrouter_model(model_name="google/gemini-3-flash-preview")
        print(f"Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}")
        llm = None


    # --- Tools ---
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
            raise ValueError(f"Simulated price for ticker '{ticker.upper()}' not found.")


    # --- Agent & Task ---
    async def main():
        if not llm:
            print("LLM not initialized. Exiting.")
            return

        # Use openrouter/ prefix for CrewAI to ensure Litellm routing
        crew_llm = f"openrouter/{llm.model_name}"
        
        # 1. Financial Analyst Agent
        financial_analyst_agent = Agent(
            role='Senior Financial Analyst',
            goal='Analyze stock data using provided tools and report key prices.',
            backstory="""You're an expert in financial markets and stock analysis.
            You have a sharp eye for numbers and can identify trends.
            You summarize prices clearly.""",
            verbose=True,
            tools=[get_stock_price],
            llm=crew_llm
        )

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

        financial_crew = Crew(
            agents=[financial_analyst_agent],
            tasks=[analyze_aapl_task],
            verbose=True
        )

        print("\n## Starting the Financial Crew...")
        result = financial_crew.kickoff()
        print("\nFinal Result:\n", result)


    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())
    return


if __name__ == "__main__":
    app.run()
