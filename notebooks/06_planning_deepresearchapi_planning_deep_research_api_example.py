import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import os
    from openai import OpenAI
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if api_key:
        # Initialize the client with OpenRouter configuration
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        # Restore the original research-focused query
        system_message = """You are a professional researcher preparing a structured, data-driven report.
        Focus on data-rich insights, use reliable sources, and include inline citations."""
        user_query = "Research the economic impact of semaglutide on global healthcare systems."

        # Create the Deep Research API call using OpenRouter's model identifier
        try:
            print(f"## Requesting Deep Research from OpenRouter (model: openai/o4-mini-deep-research) ##", flush=True)
            print("Note: Deep Research models can take multiple minutes as they perform real-time web searches...", flush=True)
            
            # This is a beta API on OpenRouter
            response = client.responses.create(
              model="openai/o4-mini-deep-research",
              input=[
                {
                  "role": "developer",
                  "content": [{"type": "input_text", "text": system_message}]
                },
                {
                  "role": "user",
                  "content": [{"type": "input_text", "text": user_query}]
                }
              ],
              reasoning={"summary": "auto"},
              tools=[{"type": "web_search_preview"}]
            )

            print("## Response received from OpenRouter ##", flush=True)
            if response.output:
                final_report = response.output[-1].content[0].text
                print("\n--- FINAL REPORT ---\n")
                print(final_report)

                # --- ACCESS INLINE CITATIONS AND METADATA ---
                print("\n--- CITATIONS ---")
                annotations = response.output[-1].content[0].annotations

                if not annotations:
                    print("No annotations found in the report.")
                else:
                    for i, citation in enumerate(annotations):
                        cited_text = final_report[citation.start_index:citation.end_index]
                        print(f"Citation {i+1}:")
                        print(f"  Cited Text: {cited_text}")
                        print(f"  Title: {citation.title}")
                        print(f"  URL: {citation.url}")
                        print(f"  Location: chars {citation.start_index}–{citation.end_index}")
                
                print("\n" + "="*50 + "\n")

                # --- INSPECT INTERMEDIATE STEPS ---
                print("--- INTERMEDIATE STEPS ---")
                reasoning_steps = [item for item in response.output if item.type == "reasoning"]
                if reasoning_steps:
                    print(f"\n[Found reasoning steps]")
                    for rs in reasoning_steps:
                        for summary_part in rs.summary:
                            print(f"  - {summary_part.text}")
                
                search_steps = [item for item in response.output if item.type == "web_search_call"]
                if search_steps:
                    print(f"\n[Found search calls]")
                    for ss in search_steps:
                        print(f"  Query: '{ss.action['query']}' | Status: {ss.status}")

            else:
                print("No output received from the model.")
        except Exception as e:
            print(f"Error during Deep Research API call: {e}")
    else:
        print("OPENROUTER_API_KEY not found in .env file.")
    return


if __name__ == "__main__":
    app.run()
