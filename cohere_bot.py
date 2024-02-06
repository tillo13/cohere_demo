import os
import cohere
from dotenv import load_dotenv
import datetime  # Import the datetime module
from stability_sdk import client  # Stability SDK
from stability_sdk.interfaces.gooseai.generation import generation_pb2 as generation
from PIL import Image
import io

from langchain_utils import get_enhanced_prompt


# ANSI escape codes for colors
YELLOW = '\033[93m'
GREEN = '\033[92m'
WHITE = '\033[97m'
RESET = '\033[0m'

# Separator for readability
SEPARATOR = "-" * 30

# Load environment variables from .env file
load_dotenv()

# Retrieve the Stability API key from environment variables and set safe prompt
stability_api_key = os.getenv("STABILITY_API_KEY")
SAFE_PROMPT_PREFIX = "SFW, clean and wholesome, in the style of a classic painting: "


# Initialize the Stability client
stability_api = client.StabilityInference(
    key=stability_api_key,  # The API Key
    verbose=True,  # Print debug messages
    engine="stable-diffusion-xl-beta-v2-2-2",  # The engine to use for generation (use a valid engine name here)
)

# Retrieve the API key from environment variables
api_key = os.getenv("COHERE_API_KEY")

# Initialize the Cohere client with your API key
co = cohere.Client(api_key)

# Initialize variables for conversation history
chat_history = []

# Display an opening statement before the conversation starts
print(SEPARATOR)
print(f"{GREEN}Welcome to Teradata TechStorm using Cohere's conversational AI!{RESET}")
print("Type 'quit' to end the conversation, 'image: description' to generate an image, and feel free to talk at will!")
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
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        # Add separator and current date and time before each user prompt
        print(SEPARATOR)
        print(f"{WHITE}{current_time}{RESET}")
        user_input = input(f"{WHITE}You:{RESET} ")

        # Add user message to chat history
        chat_history.append({"role": "USER", "message": user_input})

        # Handle the 'image' command
        if user_input.lower().startswith('image:'):
            # Check if the 'IMAGES' directory exists, and if not, create it
            images_dir = 'IMAGES'
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
                
            # Extract the actual description from the user input
            description = user_input[len('image:'):].strip()
            
            # Prepend the safe prompt prefix to the user's description
            safe_description = SAFE_PROMPT_PREFIX + description
            
            # Notify the user that an improved prompt is being requested
            print(f"Querying LangChain to fancy-up your initial prompt of: {description}...")
            enhanced_prompt = get_enhanced_prompt(safe_description)

            # Show the user the enhanced prompt in the console
            print(f"Received an enhanced prompt back from Langchain:{GREEN}\n{enhanced_prompt}{RESET}")

            # Notify the user before generating the image with the enhanced prompt
            print(SEPARATOR)
            print(f"Hold please, talking to Stable Diffusion to whip up an image with the enhanced version of: {description}...")
            print(SEPARATOR)

            # Changed from safe_description to enhanced_prompt here
            answers = stability_api.generate(
                prompt=enhanced_prompt,  # Use the enhanced_prom
                steps=20,  # The number of inference steps
                cfg_scale=7.5,  # Influences how strongly your generation is guided to match your prompt
                width=512,  # Generation width
                height=512,  # Generation height
                samples=1,  # Number of images to generate
                sampler=generation.SAMPLER_K_LMS,  # Sampler used for generation
            )

            for resp in answers:
                # Check if artifacts are available
                if resp.artifacts:
                    # Print selected fields from response
                    print(f"Full payload response from Stable Diffusion:")
                    print(f"answer_id: {resp.answer_id}")
                    print(f"request_id: {resp.request_id}")
                    print(f"received: {resp.received}")
                    print(f"created: {resp.created}\n")
                    for artifact in resp.artifacts:
                        if artifact.type == generation.ARTIFACT_IMAGE:
                            print(f"artifacts {{")
                            print(f"  type: ARTIFACT_IMAGE")
                            print(f"  mime: \"{artifact.mime}\"")
                            print(f"  seed: {artifact.seed}")
                            print(f"  uuid: \"{artifact.uuid}\"")
                            print(f"  size: {artifact.size}\n}}")

                            # Save and show the image
                            img = Image.open(io.BytesIO(artifact.binary))
         
                            image_filename = f"{artifact.seed}.png"

                            image_path = os.path.join(images_dir, image_filename)  # Use os.path.join to save images to 'IMAGES' directory

                            img.save(image_path)
                            print(f"Image saved to: {image_path}")
                            img.show()
                else:
                    print("No image was generated.")
            continue

        print(SEPARATOR)  # Separator after the bot's response

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