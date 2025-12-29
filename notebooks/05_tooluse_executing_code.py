import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import os, getpass
    import asyncio
    import nest_asyncio
    from typing import List
    from dotenv import load_dotenv
    import logging
    from google.adk.agents import Agent as ADKAgent, LlmAgent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.tools import google_search
    from google.adk.code_executors import BuiltInCodeExecutor
    from google.genai import types

    # Define variables required for Session setup and Agent execution
    APP_NAME="calculator"
    USER_ID="user1234"
    SESSION_ID="session_code_exec_async"


    # Agent Definition
    code_agent = LlmAgent(
       name="calculator_agent",
       model="gemini-2.0-flash",
       code_executor=BuiltInCodeExecutor(),
       instruction="""You are a calculator agent.
       When given a mathematical expression, write and execute Python code to calculate the result.
       Return only the final numerical result as plain text, without markdown or code blocks.
       """,
       description="Executes Python code to perform calculations.",
    )

    # Agent Interaction (Async)
    async def call_agent_async(query):

       # Session and Runner
       session_service = InMemorySessionService()
       session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
       runner = Runner(agent=code_agent, app_name=APP_NAME, session_service=session_service)

       content = types.Content(role='user', parts=[types.Part(text=query)])
       print(f"\n--- Running Query: {query} ---")
       final_response_text = "No final text response captured."
       try:
           # Use run_async
           async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
               print(f"Event ID: {event.id}, Author: {event.author}")

               # --- Check for specific parts FIRST ---
               # has_specific_part = False
               if event.content and event.content.parts and event.is_final_response():
                   for part in event.content.parts: # Iterate through all parts
                       if part.executable_code:
                           # Access the actual code string via .code
                           print(f"  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```")
                           has_specific_part = True
                       elif part.code_execution_result:
                           # Access outcome and output correctly
                           print(f"  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}")
                           has_specific_part = True
                       # Also print any text parts found in any event for debugging
                       elif part.text and not part.text.isspace():
                           print(f"  Text: '{part.text.strip()}'")
                           # Do not set has_specific_part=True here, as we want the final response logic below

                   # --- Check for final response AFTER specific parts ---
                   text_parts = [part.text for part in event.content.parts if part.text]
                   final_result = "".join(text_parts)
                   print(f"==> Final Agent Response: {final_result}")

       except Exception as e:
           print(f"ERROR during agent run: {e}")
       print("-" * 30)

    # Main async function to run the examples
    async def main():
       await call_agent_async("Calculate the value of (5 + 7) * 3")
       await call_agent_async("What is 10 factorial?")


    # Execute the main async function
    try:
       nest_asyncio.apply()
       asyncio.run(main())
    except RuntimeError as e:
       # Handle specific error when running asyncio.run in an already running loop (like Jupyter/Colab)
       if "cannot be called from a running event loop" in str(e):
           print("\nRunning in an existing event loop (like Colab/Jupyter).")
           print("Please run `await main()` in a notebook cell instead.")
           # If in an interactive environment like a notebook, you might need to run:
           # await main()
       else:
           raise e # Re-raise other runtime errors
    return


if __name__ == "__main__":
    app.run()
