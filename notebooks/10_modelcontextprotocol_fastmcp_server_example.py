import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    # fastmcp_server.py
    # This script demonstrates how to create a simple MCP server using FastMCP.
    # It exposes a single tool that generates a greeting.

    # To run this server:
    # 1. Make sure you have FastMCP installed: pip install fastmcp
    # 2. Save this code as fastmcp_server.py
    # 3. Run from your terminal: python fastmcp_server.py

    from fastmcp import FastMCP, tool
    import asyncio # Required for FastMCP's async capabilities

    # Define a simple tool function.
    # The `@tool()` decorator registers this Python function as an MCP tool.
    # The docstring becomes the tool's description for the LLM.
    @tool()
    def greet(name: str) -> str:
        """
        Generates a personalized greeting.

        Args:
            name: The name of the person to greet.

        Returns:
            A greeting string.
        """
        return f"Hello, {name}! Nice to meet you."

    # Initialize the FastMCP server.
    # By default, FastMCP runs on http://localhost:8000
    # and automatically discovers functions decorated with @tool().
    mcp_server = FastMCP()

    # To run the server, you typically use `mcp_server.run()` or `mcp_server.run_async()`.
    # For a simple script, `run()` is sufficient.
    if __name__ == "__main__":
        print("Starting FastMCP server...")
        print("This server exposes a 'greet' tool.")
        print("Access the tool schema at http://localhost:8000/tools.json")
        print("Press Ctrl+C to stop the server.")
        # FastMCP's run() method is blocking and starts the server.
        # It handles the asyncio event loop internally.
        mcp_server.run()
    return


if __name__ == "__main__":
    app.run()
