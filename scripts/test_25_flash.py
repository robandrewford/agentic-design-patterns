import os
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

def test_model(model_name):
    print(f"--- Testing model: {model_name} ---")
    try:
        client = Client(api_key=os.getenv('GOOGLE_API_KEY'))
        response = client.models.generate_content(
            model=model_name,
            contents="Say hello!"
        )
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Failed! Error: {e}")

if __name__ == "__main__":
    test_model("gemini-2.0-flash")
    test_model("gemini-2.5-flash")
