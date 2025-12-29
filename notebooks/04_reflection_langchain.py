import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import os
    import sys
    import asyncio
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    
    # Use utils for OpenRouter
    from utils import get_openrouter_model

    # --- Configuration ---
    try:
        llm = get_openrouter_model(model_name="google/gemini-3-flash-preview", temperature=0.7)
        print(f"Language model initialized: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}", file=sys.stderr)
        llm = None
        
    # --- Define Chain Components ---

    # 1. Initial Generation: Creates the first draft of the product description.
    # The input to this chain will be a dictionary, so we update the prompt template.
    generation_chain = (
        ChatPromptTemplate.from_messages([
            ("system", "Write a short, simple product description for a new smart coffee mug."),
            ("user", "{product_details}")
        ])
        | llm
        | StrOutputParser()
    )

    # 2. Critique: Evaluates the generated description and provides feedback.
    critique_chain = (
        ChatPromptTemplate.from_messages([
            ("system", """Critique the following product description based on clarity, conciseness, and appeal.
            Provide specific suggestions for improvement."""),
            # This will receive 'initial_description' from the previous step.
            ("user", "Product Description to Critique:\n{initial_description}")
        ])
        | llm
        | StrOutputParser()
    )

    # 3. Refinement: Rewrites the description based on the original details and the critique.
    refinement_chain = (
        ChatPromptTemplate.from_messages([
            ("system", """Based on the original product details and the following critique,
            rewrite the product description to be more effective.

            Original Product Details: {product_details}
            Critique: {critique}

            Refined Product Description:"""),
            ("user", "") # User input is empty as the context is provided in the system message
        ])
        | llm
        | StrOutputParser()
    )


    # --- Build the Full Reflection Chain (Refactored) ---
    # This chain is structured to be more readable and linear.
    full_reflection_chain = (
        RunnablePassthrough.assign(
            initial_description=generation_chain
        )
        | RunnablePassthrough.assign(
            critique=critique_chain
        )
        | refinement_chain
    )


    # --- Run the Chain ---
    async def run_reflection_example(product_details: str):
        """Runs the LangChain reflection example with product details."""
        print(f"\n--- Running Reflection Example for Product: '{product_details}' ---")
        try:
            # The chain now expects a dictionary as input from the start.
            final_refined_description = await full_reflection_chain.ainvoke(
                {"product_details": product_details}
            )
            print("\n--- Final Refined Product Description ---")
            print(final_refined_description)
        except Exception as e:
            print(f"\nAn error occurred during chain execution: {e}")

    if __name__ == "__main__":
        test_product_details = "A mug that keeps coffee hot and can be controlled by a smartphone app."
        asyncio.run(run_reflection_example(test_product_details))
    return


if __name__ == "__main__":
    app.run()
