import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    from google.adk.agents import SequentialAgent, Agent

    # This agent's output will be saved to session.state["data"]
    step1 = Agent(name="Step1_Fetch", output_key="data")

    # This agent will use the data from the previous step.
    # We instruct it on how to find and use this data.
    step2 = Agent(
        name="Step2_Process",
        instruction="Analyze the information found in state['data'] and provide a summary."
    )

    pipeline = SequentialAgent(
        name="MyPipeline",
        sub_agents=[step1, step2]
    )

    # When the pipeline is run with an initial input, Step1 will execute,
    # its response will be stored in session.state["data"], and then
    # Step2 will execute, using the information from the state as instructed.
    return


if __name__ == "__main__":
    app.run()
