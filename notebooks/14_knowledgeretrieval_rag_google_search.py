import marimo

__generated_with = "0.18.4"
app = marimo.App()


app._unparsable_cell(
    r"""
    from google.adk.tools import Google Search
    from google.adk.agents import Agent

    search_agent = Agent(
        name=\"research_assistant\",
        model=\"gemini-2.0-flash-exp\",
        instruction=\"You help users research topics. When asked, use the Google Search tool\",
        tools=[Google Search]
    )
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
