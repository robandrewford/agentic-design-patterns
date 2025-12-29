import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import asyncio
    import nest_asyncio
    from typing import Optional
    
    # Import our OpenRouter utility
    # Note: We are using LangChain here instead of Google ADK because
    # the environment is configured for OpenRouter (OPENROUTER_API_KEY)
    # and Google ADK requires a native Google API Key.
    from utils import get_openrouter_model

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough

    # --- Configuration ---
    try:
        # Use a model that is available on OpenRouter
        llm = get_openrouter_model(model_name="mistralai/mistral-7b-instruct:free")
        print(f"Language model initialized via OpenRouter: {llm.model_name}")
    except Exception as e:
        print(f"Error initializing language model: {e}")
        llm = None


    # --- Define Independent Research Chains ---
    # These three chains represent the "Research Agents" from the original ADK example.

    # 1. Renewable Energy Researcher
    renewable_chain: Runnable = (
        ChatPromptTemplate.from_messages([
            ("system", "You are an AI Research Assistant specializing in energy. Research the latest advancements in 'renewable energy sources'. Summarize your key findings concisely (1-2 sentences). Output *only* the summary."),
            ("user", "Conduct research.")
        ])
        | llm
        | StrOutputParser()
    )

    # 2. Electric Vehicles Researcher
    ev_chain: Runnable = (
        ChatPromptTemplate.from_messages([
            ("system", "You are an AI Research Assistant specializing in transportation. Research the latest developments in 'electric vehicle technology'. Summarize your key findings concisely (1-2 sentences). Output *only* the summary."),
            ("user", "Conduct research.")
        ])
        | llm
        | StrOutputParser()
    )

    # 3. Carbon Capture Researcher
    carbon_chain: Runnable = (
        ChatPromptTemplate.from_messages([
            ("system", "You are an AI Research Assistant specializing in climate solutions. Research the current state of 'carbon capture methods'. Summarize your key findings concisely (1-2 sentences). Output *only* the summary."),
            ("user", "Conduct research.")
        ])
        | llm
        | StrOutputParser()
    )


    # --- Build the Parallel + Synthesis Chain ---

    # 1. Run researchers in parallel.
    # Note: Since the prompts are static, we don't strictly need input, but RunnableParallel expects one.
    # We pass a dummy input or just ignore it in the chains.
    parallel_research = RunnableParallel(
        {
            "renewable_energy_result": renewable_chain,
            "ev_technology_result": ev_chain,
            "carbon_capture_result": carbon_chain,
        }
    )

    # 2. Define the Merger Agent (Synthesis)
    merger_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI Assistant responsible for combining research findings into a structured report.
    
    Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas. Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.
    
    **Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**
    
    **Input Summaries:**
    
    *   **Renewable Energy:**
        {renewable_energy_result}
    
    *   **Electric Vehicles:**
        {ev_technology_result}
    
    *   **Carbon Capture:**
        {carbon_capture_result}
    
    **Output Format:**
    
    ## Summary of Recent Sustainable Technology Advancements
    
    ### Renewable Energy Findings
    (Based on RenewableEnergyResearcher's findings)
    [Synthesize and elaborate *only* on the renewable energy input summary provided above.]
    
    ### Electric Vehicle Findings
    (Based on EVResearcher's findings)
    [Synthesize and elaborate *only* on the EV input summary provided above.]
    
    ### Carbon Capture Findings
    (Based on CarbonCaptureResearcher's findings)
    [Synthesize and elaborate *only* on the carbon capture input summary provided above.]
    
    ### Overall Conclusion
    [Provide a brief (1-2 sentence) concluding statement that connects *only* the findings presented above.]
    """),
        ("user", "Synthesize the report.")
    ])

    # 3. Full Pipeline
    pipeline = parallel_research | merger_prompt | llm | StrOutputParser()


    # --- Execution Logic ---
    async def main_async():
        nest_asyncio.apply()
        
        if not llm:
            print("LLM not initialized. Cannot run example.")
            return

        print(f"--- Starting Parallel Research (Adapted for OpenRouter) ---")
        
        try:
            # Invoking with a dict input as ChatPromptTemplate expects a mapping
            response = await pipeline.ainvoke({"input": "Start research"})
            print("\n--- Final Report ---")
            print(response)
        except Exception as e:
            print(f"\nAn error occurred during execution: {e}")

    def main():
        asyncio.run(main_async())
        
    return main,


@app.cell
def _(main):
    main()
    return


if __name__ == "__main__":
    app.run()
