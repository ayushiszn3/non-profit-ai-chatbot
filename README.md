# 🌐 NGO AI Chatbot

A real-time, multilingual chatbot designed to assist NGOs with tasks like grant writing, donor reporting, and legal compliance — powered by OpenRouter (OpenAI-compatible), Flask, and WebSockets.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Built with](https://img.shields.io/badge/Built%20with-Python%20%7C%20Flask%20%7C%20WebSockets%20%7C%20HTML%20%7C%20JS-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## ✨ Features

- ⚡ Real-time chat using WebSockets
- 🌍 Multilingual support (auto-detect and respond in user’s language)
- 🎯 Focused on NGO use-cases (grants, donors, compliance)
- 🌓 Light/Dark mode toggle in UI
- 💻 Clean and responsive browser-based frontend

---

## 🗂️ Folder Structure

ngo-ai-chatbot/ ├── backend/ │ ├── server.py │ ├── requirements.txt │ └── .env ├── frontend/ │ ├── index.html │ ├── script.js │ └── styles.css └── assets/ ├── chatbotimg1.png └── chatbotimg2.png
yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ngo-ai-chatbot.git
cd ngo-ai-chatbot
2. Setup Python Backend
bash
Copy
Edit
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Add Environment Variable
Create a .env file inside the backend/ folder:
env
Copy
Edit
OPENROUTER_API_KEY=your_openrouter_api_key
4. Start the Server
bash
Copy
Edit
python server.py
This will:
Start the Flask backend on http://localhost:5000
Start WebSocket server on ws://localhost:6789
💡 Usage

Open frontend/index.html in your browser.
Type a question (NGO-related) in the chat box.
Toggle Light/Dark mode using the button in the corner.
Get real-time responses powered by GPT.
📸 Chat Interface Preview

Here’s how the chat interface looks in action:
🧠 Example Questions

How do I apply for international donor grants in India?
🧰 Tech Stack

Backend: Python, Flask, WebSockets, asyncio
Frontend: HTML, CSS (custom theming), JavaScript
AI Engine: OpenRouter GPT (GPT-3.5-Turbo or compatible)
🔒 License

This project is licensed under the MIT License.
🙌 Contributing

Feel free to fork and contribute! Open a pull request for major changes.


