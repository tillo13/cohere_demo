# Teradata-Techstorm-AI-Assistant

## Introduction

This repository contains the Python code for a conversational AI assistant, CohereBot, built with the Cohere conversational AI platform and additional functionalities. CohereBot can engage in conversations with users, provide stock market information, generate images, and more. 

## What's Included

- **cohere_bot.py:** This file contains the main program logic interacting with the Cohere API.  It also includes the stability_api calls for image creation. It initializes the Stability client, loads the API key from the environment variables, and sets the safe prompt prefix.  

- **langchain_utils.py:**  It has functions to enhance user prompts and generate more accurate and interesting responses using LangChain. 

- **weaviate_query.py:** This file contains the code to perform a semantic search using Weaviate. It connects to the Weaviate instance, performs a semantic search for a question similar to the query, and returns the most semantically similar question and answer with additional information.

- **nyse_lookup.py:** This file contains the get_stock_info function, which retrieves stock market information for a given ticker symbol using the yfinance library.

- **connect_to_weaviate.py:** This file contains the code to connect to the Weaviate instance. It also contains the get_environmental_variables function to retrieve the environmental variables and the pretty_json function to format JSON output.

## Installation and Usage

To install the necessary dependencies, create a virtual environment and run the following command:

pip install -r requirements.txt

To run the program, clone the repository and run the command:

python cohere_bot.py

This will start the program, and the bot will be ready to receive user input. The bot will display an opening statement and will prompt the user to enter a command. The user can enter 'quit' to end the conversation, 'image: description' to generate an image, and anything else to continue the conversation. 

## Features

- **Conversational AI:** The bot can engage in natural language conversations with users, responding to their input with human-like messages.
- **Stock Market Information:** Provide real-time data for a given ticker symbol.
- **Image Generation:** Generate images based on user-provided descriptions, using the Stability.ai API.
- **Language Model Integration:** Uses OpenAI's LangChain to enhance user prompts.

## Examples

The following examples demonstrate how to use the program:

- ** conversing with the bot:**

user: nyse:AAPL
CohereBot says: Ticker: AAPL
Market Price: 171.09
Previous Close Price: 172.13
CohereBot says: Let's ask LangChain for something fun about this ticker symbol: AAPL...

- **Generating an image:**
user: image: cat playing piano
CohereBot says: Ok, pinging Stable Diffusion, hold please...
CohereBot says: Image saved to: IMAGES/220609213947.png
CohereBot says: Generation ID: 220609213947

- **Quitting the conversation:**

user: quit
Exiting the chat.

## Conclusion

This project demonstrates how to build a conversational AI assistant using the Cohere platform and additional libraries. The following sections provide detailed information on the functionality and code. It provides a basic framework for integrating multiple AI services like LangChain and Weaviate for enhanced functionality. The bot can be further improved and customized based on specific use cases and requirements.


## License

This project is licensed under the MIT License.
