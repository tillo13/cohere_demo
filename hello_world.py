from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# Check if we've got the keys correctly
if not (COHERE_API_KEY and STABILITY_API_KEY):
    raise ValueError("API keys not found. Please check your .env file.")

print("API keys loaded successfully.")