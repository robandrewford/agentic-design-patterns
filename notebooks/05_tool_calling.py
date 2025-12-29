# /// script
# dependencies = ["dotenv==0.9.9", "langchain-google-genai==2.1.8", "crewai==0.150.0", "google-adk==1.8.0"]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. Install Dependencies
    """)
    return


@app.cell
def _():
    # packages added via marimo's package management: dotenv==0.9.9 langchain-google-genai==2.1.8 crewai==0.150.0 google-adk==1.8.0 !pip install -q -U "dotenv==0.9.9" "langchain-google-genai==2.1.8" "crewai==0.150.0" "google-adk==1.8.0"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. Import Packages
    """)
    return


@app.cell
def _():
    import os, getpass
    import asyncio
    import nest_asyncio
    from typing import List
    from dotenv import load_dotenv
    import logging


    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.tools import tool as langchain_tool
    from langchain.agents import create_tool_calling_agent, AgentExecutor

    from crewai import Agent as CrewAgent, Task, Crew
    from crewai.tools import tool as crew_tool

    from google.adk.agents import Agent as ADKAgent, LlmAgent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.tools import google_search
    from google.adk.code_executors import BuiltInCodeExecutor
    from google.genai import types
    return (
        ADKAgent,
        AgentExecutor,
        BuiltInCodeExecutor,
        ChatGoogleGenerativeAI,
        ChatPromptTemplate,
        Crew,
        CrewAgent,
        InMemorySessionService,
        LlmAgent,
        Runner,
        Task,
        asyncio,
        create_tool_calling_agent,
        crew_tool,
        getpass,
        google_search,
        langchain_tool,
        logging,
        nest_asyncio,
        os,
        types,
    )


@app.cell
def _(logging):
    # Basic logging setup helps in debugging and tracking to execution.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. Setup API Keys
    """)
    return


@app.cell
def _(getpass, os):
    # UNCOMMENT
    # Prompt the user securely and set API keys as an environment variables
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. LangChain
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.1 Setup LLM
    """)
    return


@app.cell
def _(ChatGoogleGenerativeAI):
    try:
       # A model with function/tool calling capabilities is required.
       llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
       print(f"✅ Language model initialized: {llm.model}")
    except Exception as e:
       print(f"🛑 Error initializing language model: {e}")
       llm = None
    return (llm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.2 Define Search Tool
    """)
    return


@app.cell
def _(langchain_tool):
    # --- Define a Tool ---
    @langchain_tool
    def search_information(query: str) -> str:
       """
       Provides factual information on a given topic. Use this tool to find answers to phrases
       like 'capital of France' or 'weather in London?'.
       """
       print(f"\n--- 🛠️ Tool Called: search_information with query: '{query}' ---")
       # Simulate a search tool with a dictionary of predefined results.
       simulated_results = {
           "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
           "capital of france": "The capital of France is Paris.",
           "population of earth": "The estimated population of Earth is around 8 billion people.",
           "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
           "default": f"Simulated search result for '{query}': No specific information found, but the topic seems interesting."
       }
       result = simulated_results.get(query.lower(), simulated_results["default"])
       print(f"--- TOOL RESULT: {result} ---")
       return result


    tools = [search_information]
    return (tools,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.3 Tool Calling Agent
    """)
    return


@app.cell
def _(
    AgentExecutor,
    ChatPromptTemplate,
    create_tool_calling_agent,
    llm,
    tools,
):
    # --- Create a Tool-Calling Agent ---
    if llm:
       # This prompt template requires an `agent_scratchpad` placeholder for the agent's internal steps.
       agent_prompt = ChatPromptTemplate.from_messages([
           ("system", "You are a helpful assistant."),
           ("human", "{input}"),
           ("placeholder", "{agent_scratchpad}"),
       ])


       # Create the agent, binding the LLM, tools, and prompt together.
       agent = create_tool_calling_agent(llm, tools, agent_prompt)


       # AgentExecutor is the runtime that invokes the agent and executes the chosen tools.
       # The 'tools' argument is not needed here as they are already bound to the agent.
       agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)
    return (agent_executor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.4 Run Agent
    """)
    return


@app.cell
def _(agent_executor, asyncio, nest_asyncio):
    async def run_agent_with_tool(query: str):
       """Invokes the agent executor with a query and prints the final response."""
       print(f"\n--- 🏃 Running Agent with Query: '{query}' ---")
       try:
           response = await agent_executor.ainvoke({"input": query})
           print("\n--- ✅ Final Agent Response ---")
           print(response["output"])
       except Exception as e:
           print(f"\n🛑 An error occurred during agent execution: {e}")


    async def main():
       """Runs all agent queries concurrently."""
       tasks = [
           run_agent_with_tool("What is the capital of France?"),
           run_agent_with_tool("What's the weather like in London?"),
           run_agent_with_tool("Tell me something about dogs.") # Should trigger the default tool response
       ]
       await asyncio.gather(*tasks)



    nest_asyncio.apply()
    asyncio.run(main())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. Crew AI
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4.1 Define Stock Price Search Tool
    """)
    return


@app.cell
def _(crew_tool, logging):
    # --- 1. Refactored Tool: Returns Clean Data ---
    # The tool now returns raw data (a float) or raises a standard Python error.
    # This makes it more reusable and forces the agent to handle outcomes properly.
    @crew_tool("Stock Price Lookup Tool")
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
    return (get_stock_price,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4.2 Setup Crew Entities
    """)
    return


@app.cell
def _(Crew, CrewAgent, Task, get_stock_price):
    # --- 2. Define the Agent ---
    # The agent definition remains the same, but it will now leverage the improved tool.
    financial_analyst_agent = CrewAgent(
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
    return (financial_crew,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4.3 Run Crew Agent
    """)
    return


@app.cell
def _(financial_crew, os):
    # --- 5. Run the Crew within a Main Execution Block ---
    # Using a __name__ == "__main__": block is a standard Python best practice.
    def main_1():
        """Main function to run the crew."""
        if not os.environ.get('OPENAI_API_KEY'):  # Check for API key before starting to avoid runtime errors.
            print('ERROR: The OPENAI_API_KEY environment variable is not set.')
            print('Please set it before running the script.')
            return
        print('\n## Starting the Financial Crew...')
        print('---------------------------------')
        result = financial_crew.kickoff()
        print('\n---------------------------------')
        print('## Crew execution finished.')
        print('\nFinal Result:\n', result)
    if __name__ == '__main__':  # The kickoff method starts the execution.
        main_1()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5. Google Agent Development Kit (ADK)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5.1 Agent with Search Tool
    """)
    return


@app.cell
def _(
    ADKAgent,
    InMemorySessionService,
    Runner,
    asyncio,
    google_search,
    nest_asyncio,
    types,
):
    # Define variables required for Session setup and Agent execution
    APP_NAME="Google Search_agent"
    USER_ID="user1234"
    SESSION_ID="1234"



    # Define Agent with access to search tool
    root_agent = ADKAgent(
       name="basic_search_agent",
       model="gemini-2.0-flash-exp",
       description="Agent to answer questions using Google Search.",
       instruction="I can answer your questions by searching the internet. Just ask me anything!",
       tools=[google_search] # Google Search is a pre-built tool to perform Google searches.
    )




    # Agent Interaction
    async def call_agent(query):
       """
       Helper function to call the agent with a query.
       """

       # Session and Runner
       session_service = InMemorySessionService()
       session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
       runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

       content = types.Content(role='user', parts=[types.Part(text=query)])
       events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)


       for event in events:
           if event.is_final_response():
               final_response = event.content.parts[0].text
               print("Agent Response: ", final_response)

    nest_asyncio.apply()

    asyncio.run(call_agent("what's the latest ai news?"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5.2 Agent with Code Tool
    """)
    return


@app.cell
def _(
    BuiltInCodeExecutor,
    InMemorySessionService,
    LlmAgent,
    Runner,
    asyncio,
    nest_asyncio,
    types,
):
    # Define variables required for Session setup and Agent execution
    APP_NAME_1 = 'calculator'
    USER_ID_1 = 'user1234'
    SESSION_ID_1 = 'session_code_exec_async'
    code_agent = LlmAgent(name='calculator_agent', model='gemini-2.0-flash', code_executor=BuiltInCodeExecutor(), instruction='You are a calculator agent.\n   When given a mathematical expression, write and execute Python code to calculate the result.\n   Return only the final numerical result as plain text, without markdown or code blocks.\n   ', description='Executes Python code to perform calculations.')

    # Agent Definition
    async def call_agent_async(query):
        session_service = InMemorySessionService()
        session = await session_service.create_session(app_name=APP_NAME_1, user_id=USER_ID_1, session_id=SESSION_ID_1)
        runner = Runner(agent=code_agent, app_name=APP_NAME_1, session_service=session_service)
        content = types.Content(role='user', parts=[types.Part(text=query)])
        print(f'\n--- Running Query: {query} ---')
        final_response_text = 'No final text response captured.'
        try:
            async for event in runner.run_async(user_id=USER_ID_1, session_id=SESSION_ID_1, new_message=content):
                print(f'Event ID: {event.id}, Author: {event.author}')
                if event.content and event.content.parts and event.is_final_response():
    # Agent Interaction (Async)
                    for part in event.content.parts:
                        if part.executable_code:
                            print(f'  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```')  # Session and Runner
                            has_specific_part = True
                        elif part.code_execution_result:
                            print(f'  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}')
                            has_specific_part = True
                        elif part.text and (not part.text.isspace()):
                            print(f"  Text: '{part.text.strip()}'")
                    text_parts = [part.text for part in event.content.parts if part.text]
                    final_result = ''.join(text_parts)
                    print(f'==> Final Agent Response: {final_result}')  # Use run_async
        except Exception as e:
            print(f'ERROR during agent run: {e}')
        print('-' * 30)
      # --- Check for specific parts FIRST ---
    async def main_2():  # has_specific_part = False
        await call_agent_async('Calculate the value of (5 + 7) * 3')
        await call_agent_async('What is 10 factorial?')  # Iterate through all parts
    try:
        nest_asyncio.apply()  # Access the actual code string via .code
        asyncio.run(main_2())
    except RuntimeError as e:
        if 'cannot be called from a running event loop' in str(e):
            print('\nRunning in an existing event loop (like Colab/Jupyter).')  # Access outcome and output correctly
            print('Please run `await main()` in a notebook cell instead.')
        else:
    # Main async function to run the examples
    # Execute the main async function
            raise e  # Also print any text parts found in any event for debugging  # Do not set has_specific_part=True here, as we want the final response logic below  # --- Check for final response AFTER specific parts ---  # Handle specific error when running asyncio.run in an already running loop (like Jupyter/Colab)  # If in an interactive environment like a notebook, you might need to run:  # await main()  # Re-raise other runtime errors
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    End of notebook!
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
