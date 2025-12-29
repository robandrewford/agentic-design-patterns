import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import os
    import logging
    import time
    import json
    import re
    from functools import wraps
    from typing import Tuple, Any

    from crewai import Agent, Task, Crew, Process
    from crewai_tools import SerperDevTool
    from pydantic import BaseModel, Field, ValidationError

    # --- 0. Setup ---
    # Set up logging for observability
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # For demonstration, we'll assume these are set in your environment
    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
    # os.environ["SERPER_API_KEY"] = "YOUR_SERPER_API_KEY"


    # --- 1. Input Validation (Improved) ---
    def moderate_input(text: str) -> Tuple[bool, str]:
        """
        Simulates content moderation using whole-word matching to avoid false positives.
        """
        # REFACTORED: Use regex for whole-word matching to prevent flagging words
        # like "non-violent".
        forbidden_keywords = ["violence", "hate", "illegal"]
        pattern = r'\b(' + '|'.join(re.escape(k) for k in forbidden_keywords) + r')\b'

        if re.search(pattern, text, re.IGNORECASE):
            return False, f"Input contains forbidden content based on keyword matching."
        return True, "Input is clean."


    # --- 2. Structured Output Definition ---
    class ResearchSummary(BaseModel):
        """Pydantic model for structured research output."""
        title: str = Field(description="A concise title for the research summary.")
        key_findings: list[str] = Field(description="A list of 3-5 key findings.")
        confidence_score: float = Field(description="A score from 0.0 to 1.0 indicating confidence in the findings.")


    # --- 3. Output Validation Guardrail (Corrected) ---
    def validate_research_summary(output: str) -> Tuple[bool, Any]:
        """
        Validates the raw string output from the LLM.
        The guardrail receives a string, which must be parsed and validated against the Pydantic model.
        """
        try:
            # Attempt to parse the LLM's string output into a JSON object.
            data = json.loads(output)
            # Validate the data against the ResearchSummary model.
            summary = ResearchSummary.model_validate(data)

            # Perform logical checks on the validated data.
            if not summary.title or len(summary.title.strip()) < 5:
                return False, "Research summary title is too short or empty."
            if len(summary.key_findings) < 3:
                return False, "Research summary must have at least 3 key findings."
            if not (0.0 <= summary.confidence_score <= 1.0):
                return False, "Confidence score must be between 0.0 and 1.0."

            logging.info(f"Guardrail PASSED for: {summary.title}")
            # IMPORTANT: If valid, return True and the original, approved string.
            return True, output

        except (json.JSONDecodeError, ValidationError) as e:
            # If the output is not valid JSON or doesn't match the model, reject it.
            logging.error(f"Guardrail FAILED: {e}")
            return False, f"Output failed validation: {e}"


    # --- 4. Error Handling and Resilience ---
    def retry_with_exponential_backoff(max_retries: int = 3, initial_delay: float = 1.0):
        """
        A decorator to retry a function with exponential backoff.
        NOTE: For production, consider a robust library like `tenacity`.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                delay = initial_delay
                for i in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        logging.warning(f"Attempt {i+1}/{max_retries} failed: {e}. Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                        delay *= 2
                raise Exception(f"Function {func.__name__} failed after {max_retries} attempts.")
            return wrapper
        return decorator


    # --- 5. Agent and Task Setup ---
    search_tool = SerperDevTool()

    # Agent 1: Researcher
    researcher = Agent(
        role='Senior Research Analyst',
        goal='Provide concise and accurate research summaries based on web searches.',
        backstory='An expert in extracting key insights from vast amounts of information.',
        tools=[search_tool],
        verbose=True,
        allow_delegation=False,
    )

    # Agent 2: Data Analyst (with restricted tools)
    data_analyst = Agent(
        role='Data Analyst',
        goal='Process and clean structured data.',
        backstory='Meticulous in handling datasets and ensuring data integrity.',
        tools=[], # This agent has NO tools that could access external systems.
        verbose=True
    )

    # Task 1: Research Task with validation
    research_task = Task(
        description=(
            "Conduct thorough research on 'climate change impacts on coastal cities'. "
            "Synthesize the findings into a JSON object containing a title, a list of "
            "3-5 key findings, and a confidence score."
        ),
        # REFACTORED: Provide a clear, human-readable instruction for the LLM.
        expected_output="A JSON object conforming to the ResearchSummary schema, including a title, key_findings, and confidence_score.",
        agent=researcher,
        # The corrected guardrail function is applied here.
        guardrail=validate_research_summary,
        # REFACTORED: Use `output_pydantic` for automatic parsing into the specified model.
        # This replaces the old `output_json` parameter.
        output_pydantic=ResearchSummary,
        output_file='climate_research_summary.json'
    )

    # Task 2: Data Processing Task
    data_processing_task = Task(
        description=(
            "Analyze the research summary from the previous task and report on its structure. "
            "Your input will be the JSON from the researcher. "
            "Confirm that it contains a title, at least three findings, and a confidence score."
        ),
        expected_output="A brief confirmation report on the data's quality.",
        agent=data_analyst,
        context=[research_task] # This task uses the output of the research task as context.
    )

    # --- 6. Crew Setup ---
    crew = Crew(
        agents=[researcher, data_analyst],
        tasks=[research_task, data_processing_task],
        process=Process.sequential,
        verbose=True,
    )

    # --- 7. Execution ---
    if __name__ == "__main__":
        user_query = "Please research climate change impacts on coastal cities."
        is_clean, message = moderate_input(user_query)

        if is_clean:
            logging.info("Input is clean. Starting crew execution...")

            # The `kickoff` method will now return the output of the final task.
            # Since the final task's agent (data_analyst) doesn't have a Pydantic
            # output defined, this will likely be a string.
            result = crew.kickoff()

            print("\n--- Crew Execution Finished ---")

            # The final result is the output of the last task in the sequence.
            print("\nFinal Result from Crew:")
            print(result)

            # The structured output from the first task is saved to the file.
            print(f"\nStructured output from the research task has been saved to: {research_task.output_file}")
            # You can also access the structured output directly from the task object after execution:
            if research_task.output:
                 print("\nAccessing structured output from the research task object:")
                 # The .output attribute holds the Pydantic object
                 print(research_task.output.model_dump_json(indent=2))

        else:
            logging.error(f"Input rejected by moderation: {message}")
            print(f"\nCannot proceed: {message}")
    return


if __name__ == "__main__":
    app.run()
