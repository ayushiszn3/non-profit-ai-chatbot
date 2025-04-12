import asyncio
import websockets
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from flask import Flask, request
from flask_cors import CORS
import threading
import uuid
import json

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

# Dictionary to track conversation state for each user
user_sessions = {}

# Query OpenRouter with conversation history
async def query_openrouter(session_id, user_message):
    try:
        # Get or create session
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                "conversation": [
                    {
                        "role": "system",
                        "content": (
                            "You are a multilingual assistant for NGOs. Automatically detect the user's language "
                            "and respond in the same language. You assist with grants, donor reporting, legal compliance, etc."
                            "Be concise and don't repeat greetings unless the conversation has been idle for a while."
                        )
                    }
                ],
                "needs_greeting": True
            }

        session = user_sessions[session_id]

        # Add user message to conversation history
        session["conversation"].append({"role": "user", "content": user_message})

        # Send greeting if this is the first interaction
        if session["needs_greeting"]:
            session["needs_greeting"] = False
            return "Hello! I'm your NGO AI assistant. How can I help you today?"

        # Get AI response
        response = await client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            temperature=0.5,
            messages=session["conversation"]
        )

        ai_message = response.choices[0].message.content
        session["conversation"].append({"role": "assistant", "content": ai_message})

        return ai_message

    except Exception as e:
        return f"Error: {str(e)}"

# WebSocket Chat Handler
async def handle_message(websocket, path):
    try:
        # Get or create session ID from cookies
        cookies = websocket.request_headers.get('Cookie', '')
        session_id = None
        
        # Try to get existing session ID from cookies
        for cookie in cookies.split(';'):
            if 'session_id=' in cookie.strip():
                session_id = cookie.strip().split('=')[1]
                break
        
        # Create new session if none exists
        if not session_id or session_id not in user_sessions:
            session_id = str(uuid.uuid4())
            await websocket.send(json.dumps({
                'type': 'set_cookie',
                'session_id': session_id
            }))
            print(f"New session created: {session_id}")

        # Process messages
        async for message in websocket:
            print(f"Message from {session_id}: {message}")
            reply = await query_openrouter(session_id, message)
            await websocket.send(reply)

    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed for session: {session_id}")
    except Exception as e:
        print(f"Error in connection: {str(e)}")
    finally:
        # Don't clean up session immediately - keep for some time
        pass

# WebSocket Server
async def websocket_server():
    async with websockets.serve(
        handle_message,
        "localhost",
        6789,
        ping_interval=20,
        ping_timeout=60
    ):
        print("✅ WebSocket server running at ws://localhost:6789")
        await asyncio.Future()  # Run forever

# Run Flask and WebSocket in parallel
def start_flask():
    app.run(host="0.0.0.0", port=5000)

def start_websocket():
    asyncio.run(websocket_server())

if __name__ == "__main__":
    threading.Thread(target=start_flask).start()  # Start Flask in a separate thread
    start_websocket()  # Start WebSocket server in the main thread