const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const themeToggle = document.getElementById("theme-toggle");
const clearButton = document.getElementById("clear-button");

// Function to add a message bubble to the chat window
function addMessage(message, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add(
    "message",
    sender === "user" ? "user-message" : "bot-message"
  );

  let cleanMessage = message
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/•/g, "<br>•");

  messageDiv.innerHTML = cleanMessage;
  chatWindow.appendChild(messageDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Send message to backend and get reply
async function sendMessage() {
  const message = userInput.value.trim();
  if (message === "") return;

  addMessage(message, "user");
  userInput.value = "";

  try {
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    });

    if (response.ok) {
      const data = await response.json();
      addMessage(data.reply, "bot");
    } else {
      addMessage("Error: Unable to get a response from the server.", "bot");
    }
  } catch (error) {
    console.error(error);
    addMessage("Error: Unable to connect to the server.", "bot");
  }
}

// Send message on button click
sendButton.addEventListener("click", sendMessage);

// Send message on Enter key
userInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter") sendMessage();
});

// Theme toggle
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  themeToggle.textContent = document.body.classList.contains("dark")
    ? "☀️"
    : "🌙";
});

// Clear chat history
clearButton.addEventListener("click", async () => {
  if (!confirm("Are you sure you want to clear the chat history?")) return;

  try {
    const response = await fetch("http://127.0.0.1:8000/clear_history", {
      method: "POST",
    });

    if (response.ok) {
      chatWindow.innerHTML = "";
      addMessage("Chat history cleared.", "bot");
    } else {
      addMessage("Error: Unable to clear history.", "bot");
    }
  } catch (error) {
    console.error(error);
    addMessage("Error: Unable to connect to the server.", "bot");
  }
});
