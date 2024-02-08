import weaviate
import os
from dotenv import load_dotenv
from weaviate.auth import AuthApiKey

# Variable to hold the query text
QUERY_TO_WCS = "what's the bell all about?"

# ANSI escape codes for colors and formatting
YELLOW = '\033[93m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'
SEPARATOR = f"{WHITE}{'-' * 60}{RESET}"

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key and Weaviate credentials from environment variables
OPENAI_APIKEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_WCS_URL")
WEAVIATE_APIKEY = os.getenv("WEAVIATE_API_KEY")

# Connect to the Weaviate instance
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=AuthApiKey(api_key=WEAVIATE_APIKEY),
    additional_headers={"X-OpenAI-Api-Key": OPENAI_APIKEY}
)

# Perform a semantic search for a question similar to the query
print(f"{BOLD}Performing a semantic search in Weaviate...")
print(f"Querying '{WEAVIATE_URL}' for data related to:\n{RESET} {YELLOW}{QUERY_TO_WCS}{RESET}")
print(SEPARATOR)

search_results = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": [QUERY_TO_WCS]})
    .with_limit(1)  # Adjust the limit if you want to fetch more results
    .do()
)

# Print the most semantically similar question and answer
if search_results["data"]["Get"]["Question"]:
    closest_match = search_results["data"]["Get"]["Question"][0]
    print(f"{BOLD}Closest WCS Question:{RESET} {YELLOW}{closest_match['question']}{RESET}")
    print(f"{BOLD}Answer:{RESET} {WHITE}{closest_match['answer']}{RESET}")
    print(f"{BOLD}Category:{RESET} {WHITE}{closest_match['category']}{RESET}")
    print(SEPARATOR)
else:
    print(f"{BOLD}No closely related questions found.{RESET}")