import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    # Code Snippet

    import datetime

    from google.adk.agents import LlmAgent # type: ignore[import-untyped]
    from google.adk.tools.google_api_tool import CalendarToolset # type: ignore[import-untyped]


    async def create_agent(client_id, client_secret) -> LlmAgent:
        """Constructs the ADK agent."""
        toolset = CalendarToolset(client_id=client_id, client_secret=client_secret)
        return LlmAgent(
            model='gemini-2.0-flash-001',
            name='calendar_agent',
            description="An agent that can help manage a user's calendar",
            instruction=f"""
    You are an agent that can help manage a user's calendar.

    Users will request information about the state of their calendar or to make changes to
    their calendar. Use the provided tools for interacting with the calendar API.

    If not specified, assume the calendar the user wants is the 'primary' calendar.

    When using the Calendar API tools, use well-formed RFC3339 timestamps.

    Today is {datetime.datetime.now()}.
    """,
            tools=await toolset.get_tools(),
        )
    return (create_agent,)


@app.cell
def _(
    A2AStarletteApplication,
    ADKAgentExecutor,
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    DefaultRequestHandler,
    InMemoryArtifactService,
    InMemoryMemoryService,
    InMemorySessionService,
    InMemoryTaskStore,
    PlainTextResponse,
    Request,
    Route,
    Runner,
    Starlette,
    asyncio,
    create_agent,
    os,
    uvicorn,
):
    #Code Snippet

    def main(host: str, port: int):
        # Verify an API key is set.
        # Not required if using Vertex AI APIs.
        if os.getenv('GOOGLE_GENAI_USE_VERTEXAI') != 'TRUE' and not os.getenv(
            'GOOGLE_API_KEY'
        ):
            raise ValueError(
                'GOOGLE_API_KEY environment variable not set and '
                'GOOGLE_GENAI_USE_VERTEXAI is not TRUE.'
            )

        skill = AgentSkill(
            id='check_availability',
            name='Check Availability',
            description="Checks a user's availability for a time using their Google Calendar",
            tags=['calendar'],
            examples=['Am I free from 10am to 11am tomorrow?'],
        )

        agent_card = AgentCard(
            name='Calendar Agent',
            description="An agent that can manage a user's calendar",
            url=f'http://{host}:{port}/',
            version='1.0.0',
            defaultInputModes=['text'],
            defaultOutputModes=['text'],
            capabilities=AgentCapabilities(streaming=True),
            skills=[skill],
        )

        adk_agent = asyncio.run(create_agent(
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        ))
        runner = Runner(
            app_name=agent_card.name,
            agent=adk_agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
        agent_executor = ADKAgentExecutor(runner, agent_card)

        async def handle_auth(request: Request) -> PlainTextResponse:
            await agent_executor.on_auth_callback(
                str(request.query_params.get('state')), str(request.url)
            )
            return PlainTextResponse('Authentication successful.')

        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor, task_store=InMemoryTaskStore()
        )

        a2a_app = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )
        routes = a2a_app.routes()
        routes.append(
            Route(
                path='/authenticate',
                methods=['GET'],
                endpoint=handle_auth,
            )
        )
        app = Starlette(routes=routes)

        uvicorn.run(app, host=host, port=port)


    if __name__ == '__main__':
        main()
    return


if __name__ == "__main__":
    app.run()
