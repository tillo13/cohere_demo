import cohere
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("COHERE_API_KEY")

# Initialize the Cohere client with your API key
co = cohere.Client(api_key)


# generate a prediction for a prompt
prediction = co.chat(message='Howdy! 🤠', model='command')

# print the predicted text
print(f'Chatbot: {prediction.text}')