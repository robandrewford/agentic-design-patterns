import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    # Import the necessary VertexAiRagMemoryService class from the google.adk.memory module.
    from google.adk.memory import VertexAiRagMemoryService


    RAG_CORPUS_RESOURCE_NAME = "projects/your-gcp-project-id/locations/us-central1/ragCorpora/your-corpus-id"

    # Define an optional parameter for the number of top similar results to retrieve.
    # This controls how many relevant document chunks the RAG service will return.
    SIMILARITY_TOP_K = 5

    # Define an optional parameter for the vector distance threshold.
    # This threshold determines the maximum semantic distance allowed for retrieved results;
    # results with a distance greater than this value might be filtered out.
    VECTOR_DISTANCE_THRESHOLD = 0.7

    # Initialize an instance of VertexAiRagMemoryService.
    # This sets up the connection to your Vertex AI RAG Corpus.
    # - rag_corpus: Specifies the unique identifier for your RAG Corpus.
    # - similarity_top_k: Sets the maximum number of similar results to fetch.
    # - vector_distance_threshold: Defines the similarity threshold for filtering results.
    memory_service = VertexAiRagMemoryService(
        rag_corpus=RAG_CORPUS_RESOURCE_NAME,
        similarity_top_k=SIMILARITY_TOP_K,
        vector_distance_threshold=VECTOR_DISTANCE_THRESHOLD
    )
    return


if __name__ == "__main__":
    app.run()
