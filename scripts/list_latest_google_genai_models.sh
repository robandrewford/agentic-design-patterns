
uv run python3 -c "import os; from google.genai import Client;
from dotenv import load_dotenv; load_dotenv();
client = Client(api_key=os.getenv('GOOGLE_API_KEY'));
[print(f'{m.name}: {m.display_name}') for m in client.models.list() if 'gemini' in m.name]"

# Run the script
# ./list_latest_google_genai_models.sh