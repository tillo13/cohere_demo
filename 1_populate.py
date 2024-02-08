import weaviate
import json
import requests
import time
import os
from dotenv import load_dotenv
from weaviate.auth import AuthApiKey

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key and Weaviate credentials from environment variables
OPENAI_APIKEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_WCS_URL")
WEAVIATE_APIKEY = os.getenv("WEAVIATE_API_KEY")

# Time script execution
start_time = time.time()

# Create a client for the remote Weaviate instance
print(f"Connecting to {WEAVIATE_URL}...")
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=AuthApiKey(api_key=WEAVIATE_APIKEY),
    additional_headers={"X-OpenAI-Api-Key": OPENAI_APIKEY}
)

# Check if the 'Question' class exists in the Weaviate schema and delete it if it does
if client.schema.exists("Question"):
    print("The 'Question' class already exists. Deleting it...")
    client.schema.delete_class("Question")

# Define and create the 'Question' class in the schema
class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {},
        "generative-openai": {}
    }
}

print("Creating the 'Question' class in the schema...")
client.schema.create_class(class_obj)
print("The 'Question' class has been created.")

url = "https://drive.google.com/uc?export=download&id=1TdeAV1N_NgjEB3-T21FQLSu1sdg4-_qW"

print(f"Retrieving New York Stock Exchange data from {url}...")

# Load data from your JSON file
response = requests.get(url)
data = json.loads(response.text)
question_count = len(data)
print(f"Data successfully retrieved. {question_count} questions found.")

# Start importing the questions into Weaviate
print(f"Starting the import process for {question_count} New York Stock Exchange questions...")
for i, question_data in enumerate(data):
    print(f"Importing NYSE question {i + 1}: {question_data['Question']}")
    
    # Define the properties for each 'Question' object
    question_properties = {
        "answer": question_data["Answer"],
        "question": question_data["Question"],
        "category": question_data["Category"],
    }
    
    # Add the data to Weaviate
    client.data_object.create(
        data_object=question_properties,
        class_name="Question"
    )

# Calculate the total time taken to run the script
end_time = time.time()
print(f"All New York Stock Exchange questions have been imported in {end_time - start_time:.2f} seconds.")