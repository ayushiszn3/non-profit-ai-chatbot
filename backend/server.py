import asyncio
import websockets
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from flask import Flask
from flask_cors import CORS
import threading

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Configure OpenRouter client
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Flask app setup
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Chatbot server is running"

async def query_openrouter(prompt):
    try:
        response = await client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  # or "anthropic/claude-3-haiku"
            temperature=0.5,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a multilingual assistant. Follow these rules strictly:\n"
                        "1. Respond in the SAME LANGUAGE as the user's message\n"
                        "2. For unclear inputs (code, numbers, mixed languages), use English\n"
                        "3. Never translate the user's message - only match their language\n"
                        "4. For technical terms (GitHub, API, etc.), keep them in original form\n"
                        "Examples:\n"
                        "- User: 'Bonjour' → French response\n"
                        "- User: 'Hola' → Spanish response\n"
                        "- User: 'Hello' → English response\n"
                        "- User: 'git clone' → English response (unclear)"
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

async def handle_message(websocket):
    async for message in websocket:
        print(f"User ({len(message)} chars): {message[:50]}...")
        reply = await query_openrouter(message)
        await websocket.send(reply)

async def websocket_server():
    async with websockets.serve(handle_message, "localhost", 6789):
        print("✅ WebSocket server running at ws://localhost:6789")
        await asyncio.Future()  # Run indefinitely

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Start Flask in a daemon thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start WebSocket server in main thread
    asyncio.run(websocket_server())