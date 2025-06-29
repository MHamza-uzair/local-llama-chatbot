# chatbot_api.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ollama import Client
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Client(host='http://localhost:11434')

conversation_history = []
HISTORY_FILE = "conversation_history.json"

# Load previous history if exists
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        conversation_history = json.load(f)
    print("[System] Previous conversation loaded.")


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    user_message = chat_request.message
    conversation_history.append({"role": "user", "content": user_message})

    response = client.chat(
        model="llama3:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful chatbot. "
                    "When replying, format your answers with clear headings and bullet points to improve readability. "
                    "Use short, friendly sentences."
                )
            },
            *conversation_history
        ]
    )

    bot_reply = response['message']['content']
    conversation_history.append({"role": "assistant", "content": bot_reply})

    # Save updated history
    with open(HISTORY_FILE, "w") as f:
        json.dump(conversation_history, f, indent=2)

    return JSONResponse(content={"reply": bot_reply})


@app.post("/clear_history")
async def clear_history():
    global conversation_history
    conversation_history = []

    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

    return JSONResponse(content={"message": "History cleared."}, status_code=status.HTTP_200_OK)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
