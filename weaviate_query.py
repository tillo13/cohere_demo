# query_weaviate.py
import weaviate
import os
from dotenv import load_dotenv
from weaviate.auth import AuthApiKey

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key and Weaviate credentials from environment variables
OPENAI_APIKEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_WCS_URL")
WEAVIATE_APIKEY = os.getenv("WEAVIATE_API_KEY")

# Function to perform a semantic search using Weaviate
def get_weaviate_answer(query):
    # Connect to the Weaviate instance
    client = weaviate.Client(
        url=WEAVIATE_URL,
        auth_client_secret=AuthApiKey(api_key=WEAVIATE_APIKEY),
        additional_headers={"X-OpenAI-Api-Key": OPENAI_APIKEY}
    )

    # Perform a semantic search for a question similar to the query
    search_results = (
        client.query
        .get("Question", ["question", "answer", "category"])
        .with_near_text({"concepts": [query]})
        .with_limit(1)  # Adjust the limit if you want to fetch more results
        .do()
    )

    # Return the most semantically similar question and answer
    if search_results["data"]["Get"]["Question"]:
        return search_results["data"]["Get"]["Question"][0]
    else:
        return None