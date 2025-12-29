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
    
    from utils import get_openrouter_model

    # --- Tool Definition (Simulating Vertex AI Search / RAG) ---
    @tool
    def search_q2_strategy_docs(query: str) -> str:
        """
        Searches the Q2 Strategy Documents for relevant information.
        """
        print(f"\n--- 📄 Vertex AI Search (Simulated) Called: '{query}' ---")
        # Simulate RAG retrieval
        if "safety" in query.lower():
            return "Content from Doc 'Safety_Procedures_Lab_X.pdf': All personnel must wear goggles. Emergency exits are located in the north wing."
        elif "strategy" in query.lower():
            return "Content from Doc 'Q2_Strategy.pdf': Our main goal is to increase AI adoption by 20%. Key focus areas: integration and efficiency."
        else:
            return "No relevant documents found in the datastore."

    # --- Configuration ---
    try:
        # Using a model to synthesize the "retrieved" info
        llm = get_openrouter_model(model_name="google/gemini-3-flash-preview")
        print(f"Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}")
        llm = None


    async def main():
        if not llm:
            return

        tools = [search_q2_strategy_docs]
        
        # LangGraph Agent
        graph = create_react_agent(llm, tools=tools, prompt="You are a helpful assistant. Answer questions using the available search tools for internal documents.")

        print("\n--- Running Vertex AI Search Agent (Simulated/LangGraph) ---")
        
        queries = [
            "Summarize the main points about the Q2 strategy document.",
            "What safety procedures are mentioned for lab X?"
        ]
        
        for q in queries:
            print(f"\nQuery: {q}")
            try:
                inputs = {"messages": [HumanMessage(content=q)]}
                result = await graph.ainvoke(inputs)
                print(f"Agent Response: {result['messages'][-1].content}")
            except Exception as e:
                print(f"Error: {e}")


    if __name__ == "__main__":
        nest_asyncio.apply()
        asyncio.run(main())
    return


if __name__ == "__main__":
    app.run()
