import marimo

__generated_with = "0.18.4"
app = marimo.App()


app._unparsable_cell(
    r"""
    #Synchronous Request Example

    {
      \"jsonrpc\": \"2.0\",
      \"id\": \"1\",
      \"method\": \"sendTask\",
      \"params\": {
        \"id\": \"task-001\",
        \"sessionId\": \"session-001\",
        \"message\": {
          \"role\": \"user\",
          \"parts\": [
            {
              \"type\": \"text\",
              \"text\": \"What is the exchange rate from USD to EUR?\"
            }
          ]
        },
        \"acceptedOutputModes\": [\"text/plain\"],
        \"historyLength\": 5
      }
    }

    # Streaming Request Example
     {
      \"jsonrpc\": \"2.0\",
      \"id\": \"2\",
      \"method\": \"sendTaskSubscribe\",
      \"params\": {
        \"id\": \"task-002\",
        \"sessionId\": \"session-001\",
        \"message\": {
          \"role\": \"user\",
          \"parts\": [
            {
              \"type\": \"text\",
              \"text\": \"What's the exchange rate for JPY to GBP today?\"
            }
          ]
        },
        \"acceptedOutputModes\": [\"text/plain\"],
        \"historyLength\": 5
      }
    }
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
