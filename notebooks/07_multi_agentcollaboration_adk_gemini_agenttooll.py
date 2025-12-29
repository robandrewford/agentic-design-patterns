import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    from google.adk.agents import LlmAgent
    from google.adk.tools import agent_tool
    from google.genai import types

    # 1. A simple function tool for the core capability.
    # This follows the best practice of separating actions from reasoning.
    def generate_image(prompt: str) -> dict:
        """
        Generates an image based on a textual prompt.

        Args:
            prompt: A detailed description of the image to generate.

        Returns:
            A dictionary with the status and the generated image bytes.
        """
        print(f"TOOL: Generating image for prompt: '{prompt}'")
        # In a real implementation, this would call an image generation API.
        # For this example, we return mock image data.
        mock_image_bytes = b"mock_image_data_for_a_cat_wearing_a_hat"
        return {
            "status": "success",
            # The tool returns the raw bytes, the agent will handle the Part creation.
            "image_bytes": mock_image_bytes,
            "mime_type": "image/png"
        }


    # 2. Refactor the ImageGeneratorAgent into an LlmAgent.
    # It now correctly uses the input passed to it.
    image_generator_agent = LlmAgent(
        name="ImageGen",
        model="gemini-2.0-flash",
        description="Generates an image based on a detailed text prompt.",
        instruction=(
            "You are an image generation specialist. Your task is to take the user's request "
            "and use the `generate_image` tool to create the image. "
            "The user's entire request should be used as the 'prompt' argument for the tool. "
            "After the tool returns the image bytes, you MUST output the image."
        ),
        tools=[generate_image]
    )

    # 3. Wrap the corrected agent in an AgentTool.
    # The description here is what the parent agent sees.
    image_tool = agent_tool.AgentTool(
        agent=image_generator_agent,
        description="Use this tool to generate an image. The input should be a descriptive prompt of the desired image."
    )

    # 4. The parent agent remains unchanged. Its logic was correct.
    artist_agent = LlmAgent(
        name="Artist",
        model="gemini-2.0-flash",
        instruction=(
            "You are a creative artist. First, invent a creative and descriptive prompt for an image. "
            "Then, use the `ImageGen` tool to generate the image using your prompt."
        ),
        tools=[image_tool]
    )

    # --- How it works now ---
    # 1. The `artist_agent` decides on a prompt, e.g., "A photorealistic cat wearing a tiny top hat."
    # 2. It calls the tool: `ImageGen(input="A photorealistic cat wearing a tiny top hat.")`
    #    (Note: AgentTool uses 'input' as the default parameter name for the sub-agent's query).
    # 3. The `agent_tool` invokes `image_generator_agent` with the prompt as its input.
    # 4. The `image_generator_agent` follows its instructions and calls `generate_image(prompt="...")`.
    # 5. The function returns the image bytes.
    # 6. `image_generator_agent` returns the final image as its result.
    # 7. `artist_agent` receives the image result from the tool call.
    return


if __name__ == "__main__":
    app.run()
