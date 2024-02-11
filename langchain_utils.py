from langchain_openai import OpenAI  # Updated import
import os
from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore", category=ResourceWarning)

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI with the API key
llm = OpenAI(api_key=API_KEY)

def ask_openai(question):
    """
    Asks a question to the OpenAI model and returns the response.
    """
    # Use the invoke method to ask the question
    response = llm.invoke(question, temperature=0.7) 
    return response

# Expose the ask_openai function
def get_enhanced_prompt(prompt):
    """
    Requests an enhanced prompt from LangChain OpenAI based on the input prompt.
    """
    improved_prompt = ask_openai(f"Respond back with only an enhanced version to create a better image from an AI service for this: {prompt}")
    return improved_prompt

# This condition checks if the script is run directly (not imported)
if __name__ == '__main__':
    QUESTION_TO_ASK = "When is Christmas?"
    response = ask_openai(QUESTION_TO_ASK)
    print(response)