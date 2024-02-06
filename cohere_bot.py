import os
import cohere
from dotenv import load_dotenv
import datetime  # Import the datetime module

# ANSI escape codes for colors
YELLOW = '\033[93m'
GREEN = '\033[92m'
WHITE = '\033[97m'
RESET = '\033[0m'

# Separator for readability
SEPARATOR = "-" * 30

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("COHERE_API_KEY")

# Initialize the Cohere client with your API key
co = cohere.Client(api_key)

# Initialize variables for conversation history
chat_history = []

# Display an opening statement before the conversation starts
print(SEPARATOR)
print(f"{GREEN}Welcome to Terdata TechStorm using Cohere's conversational AI!{RESET}")
print("Type 'quit' to end the conversation and feel free to talk at will!")
print(SEPARATOR)

# Add a greeting message from the CohereBot
greeting_message = "Hello! I'm CohereBot. How can I assist you today?"
chat_history.append({"role": "CHATBOT", "message": greeting_message})
print(f"{YELLOW}CohereBot says:{RESET} {greeting_message}\n")


try:
    while True:
        # Get current date and time
        now = datetime.datetime.now()
        # Format the date and time
        current_time = now.strftime("%Y%b%d %H:%M:%S")

        # Add separator and current date and time before each user prompt
        print(SEPARATOR)
        print(f"{WHITE}{current_time}{RESET}")
        # Accept user input
        user_input = input(f"{WHITE}You:{RESET} ")
        user_message = f"{user_input}\n"
        print(SEPARATOR)  # Separator after the bot's response

        # Add user message to chat history
        chat_history.append({"role": "USER", "message": user_input})

        # Perform the chat request with streaming enabled
        streaming_chat = co.chat(
            chat_history=chat_history,
            message=user_input,
            stream=True
        )

        # Collect the streaming response and construct the bot's response
        bot_response = ''
        generation_id = None  # Reset generation_id for each new response
        for event in streaming_chat:
            # Check if the event has 'text' attribute first
            if hasattr(event, 'text'):
                bot_response += event.text
            # Capture the generation_id if available
            if hasattr(event, 'generation_id') and event.generation_id:
                generation_id = event.generation_id
            # Print non-text events in green
            if not hasattr(event, 'text'):
                print(f"{GREEN}Received a non-text event: {event}{RESET}")

        # Add bot's response and generation ID to chat history
        chat_history.append({"role": "CHATBOT", "message": bot_response.strip(), "generation_id": generation_id})

        # Print bot's response in yellow along with generation ID
        print(SEPARATOR)  # Separator after the bot's response
        bot_response_formatted = f"{YELLOW}CohereBot says:{RESET} {bot_response.strip()}\nGeneration ID: {generation_id}\n"
        print(bot_response_formatted)
        print(SEPARATOR)  # Separator after the bot's response

        # Break the loop if the user wants to quit
        if user_input.lower() == 'quit':
            print("Exiting the chat.")
            break

except KeyboardInterrupt:
    print("\nConversation ended.")