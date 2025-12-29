import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import os
    import asyncio
    from crewai import Agent, Task, Crew, Process
    
    # Use utils for OpenRouter
    from utils import get_openrouter_model

    # --- Configuration ---
    try:
        # Initialize LLM via OpenRouter
        llm = get_openrouter_model(model_name="google/gemini-3-flash-preview")
        print(f"Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}")
        llm = None

    async def main():
        if not llm:
            return

        # Use openrouter/ prefix for CrewAI to ensure Litellm routing
        crew_llm = f"openrouter/{llm.model_name}"

        # 2. Define a clear and focused agent
        planner_writer_agent = Agent(
            role='Article Planner and Writer',
            goal='Plan and then write a concise, engaging summary on a specified topic.',
            backstory=(
                'You are an expert technical writer and content strategist. '
                'Your strength lies in creating a clear, actionable plan before writing, '
                'ensuring the final summary is both informative and easy to digest.'
            ),
            verbose=True,
            allow_delegation=False,
            llm=crew_llm # Assign the specific LLM to the agent
        )

        # 3. Define a task with a more structured and specific expected output
        topic = "The importance of Reinforcement Learning in AI"
        high_level_task = Task(
            description=(
                f"1. Create a bullet-point plan for a summary on the topic: '{topic}'.\n"
                f"2. Write the summary based on your plan, keeping it around 200 words."
            ),
            expected_output=(
                "A final report containing two distinct sections:\n\n"
                "### Plan\n"
                "- A bulleted list outlining the main points of the summary.\n\n"
                "### Summary\n"
                "- A concise and well-structured summary of the topic."
            ),
            agent=planner_writer_agent,
        )

        # Create the crew with a clear process
        crew = Crew(
            agents=[planner_writer_agent],
            tasks=[high_level_task],
            process=Process.sequential,
        )

        # Execute the task
        print("## Running the planning and writing task ##")
        result = crew.kickoff()

        print("\n\n---\n## Task Result ##\n---")
        print(result)

    if __name__ == "__main__":
        asyncio.run(main())
    return


if __name__ == "__main__":
    app.run()
