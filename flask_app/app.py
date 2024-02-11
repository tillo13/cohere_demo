from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session  # This is the Flask-Session extension
import os
import cohere

# Initialize the Flask app and configure the session
app = Flask(__name__)
app.secret_key = 'replace_with_a_secret_key'  # Set a secret key for sessions security
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)  # Initialize the session

# Load the Cohere API key from the environment variables
api_key = os.getenv('COHERE_API_KEY')
if not api_key:
    raise ValueError("No COHERE_API_KEY set for Flask application")

# Initialize the Cohere client with the API key
co = cohere.Client(api_key)

@app.route('/')
def index():
    # Render the welcome page when the user first arrives
    return render_template('welcome.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']

    # Initialize or retrieve conversation history from the session
    if 'conversation_history' not in session:
        session['conversation_history'] = []  # List to hold the conversation history

    # Create a new 'conversation_id' if one doesn't exist in the session
    if 'conversation_id' not in session:
        # Create a new unique conversation_id
        session['conversation_id'] = f'user_defined_id_{os.urandom(4).hex()}'

    try:
        # Generate a response from Cohere using the stored 'conversation_id'
        response = co.chat(
            message=user_input,
            model="command",
            temperature=0.7,
            conversation_id=session['conversation_id'],
        )
        bot_response = response.text

        # Append the user's message and bot's response to the history
        session['conversation_history'].append(f"You: {user_input}")
        session['conversation_history'].append(f"Bot: {bot_response}")

        # Get the conversation history for display
        conversation_str = '\n'.join(session['conversation_history'])

        # Pass the conversation history and bot response to the result template
        return render_template('result.html', message=user_input, response=bot_response, conversation=conversation_str)
    except Exception as e:
        # If an error happens, print it and redirect to the index
        print(f"Error: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)  # Set `debug=False` in a production environment