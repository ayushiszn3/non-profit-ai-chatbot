// DOM Elements
const themeToggle = document.getElementById('dark-toggle');
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.querySelector('.input-area button');

// WebSocket Connection
const ws = new WebSocket('ws://localhost:6789');

// Initialize
window.onload = () => {
  appendMessage('bot', "Hello! I'm your NGO AI assistant. Ask me anything!");
};

// WebSocket handlers
ws.onopen = () => {
  console.log('WebSocket connection established');
};

ws.onmessage = (event) => {
  appendMessage('bot', event.data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
  appendMessage('bot', "Connection error. Please refresh the page.");
};

ws.onclose = () => {
  console.log('WebSocket connection closed');
};

// Message Functions
function appendMessage(role, content) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;

  const contentDiv = document.createElement('div');
  contentDiv.textContent = content;

  const timeSpan = document.createElement('span');
  timeSpan.className = 'message-time';
  timeSpan.textContent = new Date().toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit'
  });

  messageDiv.appendChild(contentDiv);
  messageDiv.appendChild(timeSpan);
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sendMessage() {
  const message = userInput.value.trim();
  if (message) {
    appendMessage('user', message);
    try {
      ws.send(message);
    } catch (error) {
      console.error('WebSocket send error:', error);
      appendMessage('bot', "Message failed to send. Please refresh the page.");
    }
    userInput.value = '';
  }
}

// Event Listeners
sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Dark Mode Toggle
themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  localStorage.setItem('darkMode', document.body.classList.contains('dark'));

  // Update button icon
  const icon = themeToggle.querySelector('i');
  if (document.body.classList.contains('dark')) {
    icon?.classList.replace('fa-moon', 'fa-sun');
  } else {
    icon?.classList.replace('fa-sun', 'fa-moon');
  }
});

// Check for saved dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
  document.body.classList.add('dark');
}
