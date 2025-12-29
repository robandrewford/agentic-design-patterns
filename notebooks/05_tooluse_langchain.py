import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import asyncio
    import nest_asyncio
    from langgraph.prebuilt import create_react_agent
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage
    
    # Use utils
    from utils import get_openrouter_model

    # --- Tool Definition ---
    @tool
    def search_information(query: str) -> str:
        """
        Provides factual information on a given topic.
        """
        print(f"\n--- 🛠️ Tool Called: search_information with query: '{query}' ---")
        simulated_results = {
            "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
            "capital of france": "The capital of France is Paris.",
            "tell me something about dogs": "Dogs are domesticated mammals, not natural wild animals.",
            "default": f"Simulated search result for '{query}': No specific information found."
        }
        # Simple fuzzy match or fallback
        key = query.lower()
        if "weather" in key and "london" in key:
            result = simulated_results["weather in london"]
        elif "capital" in key and "france" in key:
            result = simulated_results["capital of france"]
        elif "dogs" in key:
            result = simulated_results["tell me something about dogs"]
        else:
            result = simulated_results["default"]
            
        print(f"--- TOOL RESULT: {result} ---")
        return result

    # --- Setup ---
    try:
        llm = get_openrouter_model(model_name="google/gemini-3-flash-preview") 
        print(f"Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}")
        llm = None


    async def main():
        if not llm:
            return

        tools = [search_information]
        
        # New LangGraph Agent
        graph = create_react_agent(llm, tools=tools, prompt="You are a helpful assistant.")

        async def run_query(q):
            print(f"\nQuery: {q}")
            try:
                inputs = {"messages": [HumanMessage(content=q)]}
                result = await graph.ainvoke(inputs)
                print(f"Result: {result['messages'][-1].content}")
            except Exception as e:
                print(f"Error: {e}")

        nest_asyncio.apply()
        await asyncio.gather(
            run_query("What is the capital of France?"),
            run_query("What's the weather like in London?"),
            run_query("Tell me something about dogs.")
        )


    if __name__ == "__main__":
        asyncio.run(main())
    return


if __name__ == "__main__":
    app.run()
