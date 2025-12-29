import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import asyncio
    import nest_asyncio
    import sys
    
    # LangGraph imports (Modern LangChain Agent)
    from langgraph.prebuilt import create_react_agent
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage

    # Import utils for OpenRouter
    from utils import get_openrouter_model

    # --- Tool Definition ---
    @tool
    def execute_python_code(code: str) -> str:
        """
        Executes Python code and returns the output.
        Use this tool to perform mathematical calculations or specific data processing.
        Please print the final result so it can be captured.
        """
        print(f"\n--- 🐍 Executing Code:\n{code}\n---")
        try:
            # Capture stdout
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            with redirect_stdout(f):
                # Using a restricted scope for safety
                exec(code, {"__builtins__": __builtins__}, {})
            
            result = f.getvalue()
            print(f"--- Code Output: {result.strip()} ---")
            return result
        except Exception as e:
            return f"Error executing code: {e}"

    # --- Setup ---
    # Initialize LLM via OpenRouter
    try:
        # Using a capable model for code generation
        llm = get_openrouter_model(model_name="google/gemini-3-flash-preview", temperature=0)
        print(f"Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}", file=sys.stderr)
        llm = None


    async def main():
        if not llm:
            print("Skipping execution due to LLM initialization failure.")
            return

        tools = [execute_python_code]
        
        # Create LangGraph ReAct Agent
        # state_modifier acts as system prompt
        graph = create_react_agent(llm, tools=tools, prompt="You are a helpful assistant. When asked to perform calculations, write and execute Python code using the available tool. Always execute the code to get the answer.")
        
        # Execute Queries
        queries = [
            "Calculate the value of (5 + 7) * 3",
            "What is 10 factorial?"
        ]

        print(f"\n--- Starting Code Execution Agent (LangGraph) ---")
        
        for query in queries:
            print(f"\nQuery: {query}")
            try:
                # LangGraph expects 'messages' in input state
                inputs = {"messages": [HumanMessage(content=query)]}
                result = await graph.ainvoke(inputs)
                
                # The result is the final state. 'messages' contains the history.
                # The last message is usually the AI's final answer.
                final_msg = result["messages"][-1]
                print(f"Final Response: {final_msg.content}")
            except Exception as e:
                print(f"Error executing query: {e}")


    # --- Run ---
    if __name__ == "__main__":
        nest_asyncio.apply()
        asyncio.run(main())
    return


if __name__ == "__main__":
    app.run()
