import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import time
    from google.adk.tools.tool_context import ToolContext
    from google.adk.sessions import InMemorySessionService

    # --- Define the Recommended Tool-Based Approach ---
    def log_user_login(tool_context: ToolContext) -> dict:
        """
        Updates the session state upon a user login event.
        This tool encapsulates all state changes related to a user login.
        Args:
            tool_context: Automatically provided by ADK, gives access to session state.
        Returns:
            A dictionary confirming the action was successful.
        """
        # Access the state directly through the provided context.
        state = tool_context.state

        # Get current values or defaults, then update the state.
        # This is much cleaner and co-locates the logic.
        login_count = state.get("user:login_count", 0) + 1
        state["user:login_count"] = login_count
        state["task_status"] = "active"
        state["user:last_login_ts"] = time.time()
        state["temp:validation_needed"] = True

        print("State updated from within the `log_user_login` tool.")

        return {
            "status": "success",
            "message": f"User login tracked. Total logins: {login_count}."
        }

    # --- Demonstration of Usage ---
    # In a real application, an LLM Agent would decide to call this tool.
    # Here, we simulate a direct call for demonstration purposes.

    # 1. Setup
    session_service = InMemorySessionService()
    app_name, user_id, session_id = "state_app_tool", "user3", "session3"
    session = session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state={"user:login_count": 0, "task_status": "idle"}
    )
    print(f"Initial state: {session.state}")

    # 2. Simulate a tool call (in a real app, the ADK Runner does this)
    # We create a ToolContext manually just for this standalone example.
    from google.adk.tools.tool_context import InvocationContext
    mock_context = ToolContext(
        invocation_context=InvocationContext(
            app_name=app_name, user_id=user_id, session_id=session_id,
            session=session, session_service=session_service
        )
    )

    # 3. Execute the tool
    log_user_login(mock_context)

    # 4. Check the updated state
    updated_session = session_service.get_session(app_name, user_id, session_id)
    print(f"State after tool execution: {updated_session.state}")

    # Expected output will show the same state change as the "Before" case,
    # but the code organization is significantly cleaner and more robust.
    return


if __name__ == "__main__":
    app.run()
