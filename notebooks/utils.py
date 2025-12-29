import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def get_openrouter_model(model_name: str = "google/gemini-2.5-flash-lite", temperature: float = 0.0):
    """
    Returns a LangChain ChatOpenAI instance configured for OpenRouter.
    
    Args:
        model_name: The OpenRouter model ID. Defaults to "google/gemini-2.0-flash-exp:free".
        temperature: The temperature for generation. Defaults to 0.0.
    """
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    return ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=temperature,
        default_headers={
            "HTTP-Referer": "https://github.com/robertford/agentic-design-patterns",  # Optional, for including your app on openrouter.ai rankings.
            "X-Title": "Agentic Design Patterns", # Optional. Shows in rankings on openrouter.ai.
        },
    )
