import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    def evaluate_response_accuracy(agent_output: str, expected_output: str) -> float:
        """Calculates a simple accuracy score for agent responses."""
        # This is a very basic exact match; real-world would use more sophisticated metrics
        return 1.0 if agent_output.strip().lower() == expected_output.strip().lower() else 0.0

    # Example usage
    agent_response = "The capital of France is Paris."
    ground_truth = "Paris is the capital of France."
    score = evaluate_response_accuracy(agent_response, ground_truth)
    print(f"Response accuracy: {score}")


    import time

    def timed_agent_action(agent_function, *args, **kwargs):
        """Measures the execution time of an agent's function."""
        start_time = time.perf_counter()
        result = agent_function(*args, **kwargs)
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        print(f"Action '{agent_function.__name__}' took {latency_ms:.2f} ms")
        return result, latency_ms

    # Example usage with a dummy agent function
    def simulated_tool_call(query):
        time.sleep(0.15) # Simulate some work
        return f"Result for {query}"

    result, latency = timed_agent_action(simulated_tool_call, "get weather")
    print(f"Tool call result: {result}")

    # This is conceptual as actual token counting depends on the LLM API
    class LLMInteractionMonitor:
        def __init__(self):
            self.total_input_tokens = 0
            self.total_output_tokens = 0

        def record_interaction(self, prompt: str, response: str):
            # In a real scenario, use LLM API's token counter or a tokenizer
            input_tokens = len(prompt.split()) # Placeholder
            output_tokens = len(response.split()) # Placeholder
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            print(f"Recorded interaction: Input tokens={input_tokens}, Output tokens={output_tokens}")

        def get_total_tokens(self):
            return self.total_input_tokens, self.total_output_tokens

    # Example usage
    monitor = LLMInteractionMonitor()
    monitor.record_interaction("What is the capital of France?", "The capital of France is Paris.")
    monitor.record_interaction("Tell me a joke.", "Why don't scientists trust atoms? Because they make up everything!")
    input_t, output_t = monitor.get_total_tokens()
    print(f"Total input tokens: {input_t}, Total output tokens: {output_t}")
    return


if __name__ == "__main__":
    app.run()
