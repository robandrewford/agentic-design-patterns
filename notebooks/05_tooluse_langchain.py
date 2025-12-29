# /// script
# dependencies = ["dotenv==0.9.9", "langchain-google-genai==2.1.8", "crewai==0.150.0", "google-adk==1.8.0"]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import os
    import asyncio
    from typing import List

    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.tools import tool
    from langchain.agents import create_tool_calling_agent, AgentExecutor

    # --- Configuration ---
    # Ensure your GOOGLE_API_KEY environment variable is set.
    try:
        # A model with function/tool calling capabilities is required.
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
        print(f"✅ Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"🛑 Error initializing language model: {e}")
        llm = None


    # --- Define a Tool ---
    @tool
    def search_information(query: str) -> str:
        """
        Provides factual information on a given topic. Use this tool to find answers to questions
        like 'What is the capital of France?' or 'What is the weather in London?'.
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
        agent_executor = AgentExecutor(agent=agent, verbose=True)


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

        if __name__ == "__main__":
            # Run all async tasks in a single event loop.
            asyncio.run(main())

    else:
        print("\nSkipping agent execution due to LLM initialization failure.")
    return (
        AgentExecutor,
        ChatGoogleGenerativeAI,
        ChatPromptTemplate,
        asyncio,
        create_tool_calling_agent,
        os,
    )


@app.cell
def _():
    # packages added via marimo's package management: dotenv==0.9.9 langchain-google-genai==2.1.8 crewai==0.150.0 google-adk==1.8.0 !pip install -q -U "dotenv==0.9.9" "langchain-google-genai==2.1.8" "crewai==0.150.0" "google-adk==1.8.0"
    return


@app.cell
def _(
    AgentExecutor,
    ChatGoogleGenerativeAI,
    ChatPromptTemplate,
    asyncio,
    create_tool_calling_agent,
    os,
):
    import getpass
    import nest_asyncio
    from dotenv import load_dotenv
    import logging
    from langchain_core.tools import tool as langchain_tool
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Enter your Google API key: ')
    os.environ['OPENAI_API_KEY'] = getpass.getpass('Enter your OpenAI API key: ')
    try:
        llm_1 = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0)
        print(f'✅ Language model initialized: {llm_1.model}')
    except Exception as e:
        print(f'🛑 Error initializing language model: {e}')
    # UNCOMMENT
    # Prompt the user securely and set API keys as an environment variables
        llm_1 = None

    @langchain_tool
    def search_information_1(query: str) -> str:
        """  # A model with function/tool calling capabilities is required.
       Provides factual information on a given topic. Use this tool to find answers to phrases
       like 'capital of France' or 'weather in London?'.
       """
        print(f"\n--- 🛠️ Tool Called: search_information with query: '{query}' ---")
        simulated_results = {'weather in london': 'The weather in London is currently cloudy with a temperature of 15°C.', 'capital of france': 'The capital of France is Paris.', 'population of earth': 'The estimated population of Earth is around 8 billion people.', 'tallest mountain': 'Mount Everest is the tallest mountain above sea level.', 'default': f"Simulated search result for '{query}': No specific information found, but the topic seems interesting."}
        result = simulated_results.get(query.lower(), simulated_results['default'])
    # --- Define a Tool ---
        print(f'--- TOOL RESULT: {result} ---')
        return result
    tools_1 = [search_information_1]
    if llm_1:
        agent_prompt_1 = ChatPromptTemplate.from_messages([('system', 'You are a helpful assistant.'), ('human', '{input}'), ('placeholder', '{agent_scratchpad}')])
        agent_1 = create_tool_calling_agent(llm_1, tools_1, agent_prompt_1)
        agent_executor_1 = AgentExecutor(agent=agent_1, verbose=True, tools=tools_1)
      # Simulate a search tool with a dictionary of predefined results.
    async def run_agent_with_tool_1(query: str):
        """Invokes the agent executor with a query and prints the final response."""
        print(f"\n--- 🏃 Running Agent with Query: '{query}' ---")
        try:
            response = await agent_executor_1.ainvoke({'input': query})
            print('\n--- ✅ Final Agent Response ---')
            print(response['output'])
        except Exception as e:
            print(f'\n🛑 An error occurred during agent execution: {e}')

    async def main_1():
        """Runs all agent queries concurrently."""
        tasks = [run_agent_with_tool_1('What is the capital of France?'), run_agent_with_tool_1("What's the weather like in London?"), run_agent_with_tool_1('Tell me something about dogs.')]
    # --- Create a Tool-Calling Agent ---
        await asyncio.gather(*tasks)
    nest_asyncio.apply()  # This prompt template requires an `agent_scratchpad` placeholder for the agent's internal steps.
    asyncio.run(main_1())  # Create the agent, binding the LLM, tools, and prompt together.  # AgentExecutor is the runtime that invokes the agent and executes the chosen tools.  # The 'tools' argument is not needed here as they are already bound to the agent.  # Should trigger the default tool response
    return


if __name__ == "__main__":
    app.run()
