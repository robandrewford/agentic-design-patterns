from utils import get_openrouter_model

def main():
    print("Initializing OpenRouter model...")
    try:
        llm = get_openrouter_model()
        print(f"Model initialized: {llm.model_name}")
        
        print("Sending test prompt...")
        response = llm.invoke("Hello, are you working via OpenRouter?")
        print("\nResponse:")
        print(response.content)
        print("\nSUCCESS: OpenRouter integration verified.")
    except Exception as e:
        print(f"\nFAILURE: {e}")

if __name__ == "__main__":
    main()
