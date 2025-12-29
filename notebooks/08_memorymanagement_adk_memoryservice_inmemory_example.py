import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    # Example: Using InMemoryMemoryService
    # This is suitable for local development and testing where data persistence
    # across application restarts is not required. Memory content is lost when the app stops.
    from google.adk.memory import InMemoryMemoryService
    _memory_service = InMemoryMemoryService()
    return


@app.cell
def _():
    # Example: Using VertexAiRagMemoryService
    # This is suitable for scalable production on Google Cloud Platform, leveraging
    # Vertex AI RAG (Retrieval Augmented Generation) for persistent, searchable memory.
    # Requires: pip install google-adk[vertexai], GCP setup/authentication, and a Vertex AI RAG Corpus.
    from google.adk.memory import VertexAiRagMemoryService
    RAG_CORPUS_RESOURCE_NAME = 'projects/your-gcp-project-id/locations/us-central1/ragCorpora/your-corpus-id'
    # The resource name of your Vertex AI RAG Corpus
    SIMILARITY_TOP_K = 5  # Replace with your Corpus resource name
    VECTOR_DISTANCE_THRESHOLD = 0.7
    # Optional configuration for retrieval behavior
    # When using this service, methods like add_session_to_memory and search_memory
    # will interact with the specified Vertex AI RAG Corpus.
    _memory_service = VertexAiRagMemoryService(rag_corpus=RAG_CORPUS_RESOURCE_NAME, similarity_top_k=SIMILARITY_TOP_K, vector_distance_threshold=VECTOR_DISTANCE_THRESHOLD)  # Number of top results to retrieve  # Threshold for vector similarity
    return


if __name__ == "__main__":
    app.run()
