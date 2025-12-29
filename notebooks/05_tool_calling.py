import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import asyncio
    import nest_asyncio
    from langgraph.prebuilt import create_react_agent
    from langchain_core.tools import tool as langchain_tool
    from langchain_core.messages import HumanMessage
    from crewai import Agent as CrewAgent, Task, Crew
    from crewai.tools import tool as crew_tool
    
    # Use utils
    from utils import get_openrouter_model

    # --- Common Setup ---
    try:
        llm = get_openrouter_model(model_name="google/gemini-3-flash-preview") # Shared LLM
        print(f"Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}")
        llm = None

    # --- 1. LangGraph Agent Example ---
    @langchain_tool
    def search_information(query: str) -> str:
        """
        Provides factual information on a given topic. Use this tool to find answers.
        """
        print(f"\n[LangChain Tool] Searching for: '{query}'")
        simulated_results = {
            "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
            "capital of france": "The capital of France is Paris.",
            "population of earth": "The estimated population of Earth is around 8 billion people.",
            "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
            "default": f"Simulated search result for '{query}': No specific information found."
        }
        return simulated_results.get(query.lower(), simulated_results["default"])

    async def run_langchain_example():
        if not llm: return
        print("\n=== Running LangChain/LangGraph Tool Calling Example ===")
        tools = [search_information]
        
        # Create ReAct Agent with LangGraph
        graph = create_react_agent(llm, tools=tools, prompt="You are a helpful assistant.")
        
        try:
            inputs = {"messages": [HumanMessage(content="What is the capital of France?")]}
            result = await graph.ainvoke(inputs)
            print(f"Final LangChain Response: {result['messages'][-1].content}")
        except Exception as e:
            print(f"LangChain Error: {e}")


    # --- 2. CrewAI Agent Example ---
    @crew_tool("Simulated Search Tool")
    def crew_search_tool(query: str) -> str:
        """Useful for searching information."""
        # Re-using the logic for simulation
        print(f"\n[CrewAI Tool] Searching for: '{query}'")
        simulated_results = {
             "aapl": "AAPL is trading at $178.15",
             "apple": "AAPL is trading at $178.15",
        }
        return simulated_results.get(query.lower(), "Data not found.")

    def run_crewai_example():
        if not llm: return
        print("\n=== Running CrewAI Tool Calling Example ===")
        # Use openrouter/ prefix for CrewAI to avoid native Google client
        crew_llm = f"openrouter/{llm.model_name}"
        agent = CrewAgent(
            role='Researcher',
            goal='Find financial data.',
            backstory='You look up stock prices.',
            verbose=True,
            tools=[crew_search_tool],
            llm=crew_llm
        )
        task = Task(
            description="Find the price of Apple stock.",
            expected_output="The price of AAPL.",
            agent=agent
        )
        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        print(f"Final CrewAI Response: {result}")


    # --- Main Execution ---
    async def main():
        nest_asyncio.apply()
        await run_langchain_example()
        print("\n" + "-"*30 + "\n")
        # CrewAI is synchronous (mostly)
        run_crewai_example()

    if __name__ == "__main__":
        asyncio.run(main())

    return


if __name__ == "__main__":
    app.run()
