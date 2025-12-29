import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import requests
    import json
    import os
    from dotenv import load_dotenv

    # Load API Key from .env
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in environment.")
    else:
        response = requests.post(
          url="https://openrouter.ai/api/v1/chat/completions",
          headers={
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/robandrewford/agentic-design-patterns",
            "X-Title": "Agentic Design Patterns Examples",
          },
          data=json.dumps({
            "model": "openai/gpt-4o",
            "messages": [
              {
                "role": "user",
                "content": "What is the meaning of life?"
              }
            ]
          })
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response from OpenRouter: {result['choices'][0]['message']['content']}")
        else:
            print(f"Error from OpenRouter: {response.status_code} - {response.text}")

    return


if __name__ == "__main__":
    app.run()
