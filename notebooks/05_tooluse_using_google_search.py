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

    # --- Tool Definition (Simulating Google Search) ---
    @tool
    def google_search(query: str) -> str:
        """
        Performs a Google Search to answer questions.
        """
        print(f"\n--- 🔍 Google Search (Simulated) Called: '{query}' ---")
        return f"Start of search result for '{query}': Recent AI news involves major updates from Google (Gemini 2.0), OpenAI (Sora), and Anthropic. Models are getting faster and multimodal."

    # --- Configuration ---
    try:
        llm = get_openrouter_model(model_name="google/gemini-3-flash-preview")
        print(f"Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}")
        llm = None


    async def main():
        if not llm:
            return

        tools = [google_search]
        
        # LangGraph Agent
        graph = create_react_agent(llm, tools=tools, prompt="You are a helpful assistant. Use the google_search tool to answer questions.")

        print("\n--- Running Google Search Agent (Simulated/LangGraph) ---")
        try:
            inputs = {"messages": [HumanMessage(content="what's the latest ai news?")]}
            result = await graph.ainvoke(inputs)
            print(f"\nAgent Response: {result['messages'][-1].content}")
        except Exception as e:
            print(f"Error: {e}")

    if __name__ == "__main__":
        nest_asyncio.apply()
        asyncio.run(main())
    return


if __name__ == "__main__":
    app.run()
