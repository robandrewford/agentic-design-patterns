import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _(ADKAgent):
    from google.adk.agents import Agent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.tools import google_search
    from google.genai import types
    import nest_asyncio
    import asyncio

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


if __name__ == "__main__":
    app.run()
