import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import asyncio
    import nest_asyncio
    from typing import Optional

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
    from langchain_core.runnables import Runnable, RunnablePassthrough
    
    # Use utils for OpenRouter
    from utils import get_openrouter_model

    # --- Configuration ---
    try:
        # User requested: google/gemini-3-flash-preview
        llm = get_openrouter_model(model_name="google/gemini-3-flash-preview")
        print(f"Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}")
        llm = None

    # --- 1. Draft Writer (Generator) ---
    # Generates initial draft content on a given subject.
    draft_writer_chain = (
        ChatPromptTemplate.from_messages([
            ("system", "Write a short, informative paragraph about the user's subject."),
            ("user", "{subject}")
        ])
        | llm
        | StrOutputParser()
    )

    # --- 2. Fact Checker (Reviewer) ---
    # Reviews a given text for factual accuracy and provides a structured critique.
    reviewer_chain = (
        ChatPromptTemplate.from_messages([
            ("system", """You are a meticulous fact-checker.
            1. Read the text provided.
            2. Carefully verify the factual accuracy of all claims.
            3. Your final output must be a valid JSON dictionary containing two keys:
               - "status": A string, either "ACCURATE" or "INACCURATE".
               - "reasoning": A string providing a clear explanation for your status, citing specific issues if any are found.
            """),
            ("user", "Draft Text: {draft_text}")
        ])
        | llm
        | JsonOutputParser() 
    )

    # --- 3. Pipeline Construction ---
    # Resemblance of SequentialAgent: Generator -> Reviewer
    pipeline = (
        RunnablePassthrough.assign(draft_text=draft_writer_chain) 
        | RunnablePassthrough.assign(review_output=reviewer_chain)
    )

    # --- Execution ---
    async def run_reflection_pipeline(subject: str):
        print(f"\n--- Running Reflection Pipeline (ADK Port) for Subject: '{subject}' ---")
        try:
            result = await pipeline.ainvoke({"subject": subject})
            
            print("\n--- Initial Draft ---")
            print(result.get("draft_text"))
            
            print("\n--- Review Output ---")
            print(result.get("review_output"))
            
        except Exception as e:
            print(f"\nAn error occurred during pipeline execution: {e}")

    def main():
        nest_asyncio.apply()
        asyncio.run(run_reflection_pipeline("The history of the internet"))

    return main,


@app.cell
def _(main):
    main()
    return


if __name__ == "__main__":
    app.run()
