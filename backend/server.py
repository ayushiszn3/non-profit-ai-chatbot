import asyncio
import websockets
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from flask import Flask
from flask_cors import CORS
import threading

# Load .env variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Configure OpenRouter Client
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Flask App (CORS enabled)
app = Flask(__name__)
CORS(app)

# Query OpenRouter with multilingual support
async def query_openrouter(prompt):
    try:
        response = await client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            temperature=0.5,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a multilingual assistant for NGOs. Automatically detect the user's language "
                        "and respond in the same language. You assist with grants, donor reporting, legal compliance, etc."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# WebSocket Chat Handler
async def handle_message(websocket):
    async for message in websocket:
        print(f"User: {message}")
        reply = await query_openrouter(message)
        await websocket.send(reply)

# WebSocket Server
async def websocket_server():
    async with websockets.serve(handle_message, "localhost", 6789):
        print("✅ WebSocket server running at ws://localhost:6789")
        await asyncio.Future()  # Run forever

# Run Flask and WebSocket in parallel
def start_flask():
    app.run(host="0.0.0.0", port=5000)

def start_websocket():
    asyncio.run(websocket_server())

if __name__ == "__main__":
    threading.Thread(target=start_flask).start()
    start_websocket()