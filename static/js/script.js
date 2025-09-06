const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");



// Add message to chat
function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender === "user" ? "user-msg" : "krishna-msg");
  msg.textContent = text;
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Handle send
async function handleSend() {
  const text = userInput.value.trim();
  if (!text) return;
  addMessage(text, "user");
  userInput.value = "";

  // Show typing/loading indicator (optional)
  const loadingMsg = document.createElement("div");
  loadingMsg.classList.add("message", "krishna-msg");
  loadingMsg.textContent = "Krishna is thinking...";
  chatWindow.appendChild(loadingMsg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
    try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: text }),
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();

    // Remove loading message
    chatWindow.removeChild(loadingMsg);

    if (data.reply) {
      addMessage(data.reply, "krishna");
    } else {
      addMessage("Something went wrong. No reply received.", "krishna");
    }
  } catch (error) {
    console.error("Error:", error);

    // Remove loading message
    chatWindow.removeChild(loadingMsg);

    addMessage("An error occurred while contacting Krishna.", "krishna");
  }

}

sendBtn.addEventListener("click", handleSend);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") handleSend();
});
