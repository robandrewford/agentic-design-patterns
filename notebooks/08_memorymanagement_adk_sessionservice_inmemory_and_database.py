import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    # Example: Using InMemorySessionService
    # This is suitable for local development and testing where data persistence
    # across application restarts is not required.
    from google.adk.sessions import InMemorySessionService
    _session_service = InMemorySessionService()
    return


@app.cell
def _():
    # Example: Using DatabaseSessionService
    # This is suitable for production or development requiring persistent storage.
    # You need to configure a database URL (e.g., for SQLite, PostgreSQL, etc.).
    # Requires: pip install google-adk[sqlalchemy] and a database driver (e.g., psycopg2 for PostgreSQL)
    from google.adk.sessions import DatabaseSessionService
    # Example using a local SQLite file:
    db_url = 'sqlite:///./my_agent_data.db'
    _session_service = DatabaseSessionService(db_url=db_url)
    return


@app.cell
def _():
    # Example: Using VertexAiSessionService
    # This is suitable for scalable production on Google Cloud Platform, leveraging
    # Vertex AI infrastructure for session management.
    # Requires: pip install google-adk[vertexai] and GCP setup/authentication
    from google.adk.sessions import VertexAiSessionService
    PROJECT_ID = 'your-gcp-project-id'
    LOCATION = 'us-central1'  # Replace with your GCP project ID
    REASONING_ENGINE_APP_NAME = 'projects/your-gcp-project-id/locations/us-central1/reasoningEngines/your-engine-id'  # Replace with your desired GCP location
    # The app_name used with this service should correspond to the Reasoning Engine ID or name
    # When using this service, pass REASONING_ENGINE_APP_NAME to service methods:
    # session_service.create_session(app_name=REASONING_ENGINE_APP_NAME, ...)
    # session_service.get_session(app_name=REASONING_ENGINE_APP_NAME, ...)
    # session_service.append_event(session, event, app_name=REASONING_ENGINE_APP_NAME)
    # session_service.delete_session(app_name=REASONING_ENGINE_APP_NAME, ...)
    _session_service = VertexAiSessionService(project=PROJECT_ID, location=LOCATION)  # Replace with your Reasoning Engine resource name
    return


if __name__ == "__main__":
    app.run()
