# ollama_chatbot.py

from ollama import Client
import json
import os

# Constants
HISTORY_FILE = "conversation_history.json"
MAX_HISTORY_MESSAGES = 50  # Only keep the last 50 messages for space

# Initialize Ollama client
client = Client(host='http://localhost:11434')

# Load conversation history if it exists
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        conversation_history = json.load(f)
    print("[System] Previous conversation loaded.")
else:
    conversation_history = []
    print("[System] Starting a new conversation.")

# Function to save the last N messages to JSON


def save_history():
    trimmed_history = conversation_history[-MAX_HISTORY_MESSAGES:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(trimmed_history, f, indent=2)


# Main chatbot loop
while True:
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        save_history()
        break

    # Clear command
    if user_input.lower() == "/clear":
        conversation_history = []
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        print("[System] Conversation history cleared.")
        continue

    # Add user message
    conversation_history.append({"role": "user", "content": user_input})

    # Get LLM response
    response = client.chat(
        model="llama3:8b",
        messages=[
            {"role": "system", "content": "You are a helpful chatbot."},
            # send only the last N messages
            *conversation_history[-MAX_HISTORY_MESSAGES:]
        ]
    )

    bot_reply = response['message']['content']

    # Add bot reply
    conversation_history.append({"role": "assistant", "content": bot_reply})

    # Display bot reply
    print("Bot:", bot_reply)

    # Save conversation history after each message
    save_history()
