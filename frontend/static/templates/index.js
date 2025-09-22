const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

// Enter = send, Shift+Enter = newline
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Send button click
sendBtn.addEventListener("click", sendMessage);

// Add message bubble
function addMessage(content, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  if (sender === "bot") {
    msg.innerHTML = content;
  } else {
    msg.innerHTML = content.replace(/\n/g, "<br>");
  }
  chatContainer.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return msg;
}

// Add typing dots
function addTyping() {
  const typing = document.createElement("div");
  typing.classList.add("message", "bot");
  typing.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
  chatContainer.appendChild(typing);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return typing;
}

// Animate Markdown
function animateMarkdown(element, markdownText) {
  element.innerHTML = "";
  let index = 0;
  const speed = 15;

  const interval = setInterval(() => {
    element.innerText = markdownText.slice(0, index);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    index++;
    if (index > markdownText.length) {
      clearInterval(interval);
      element.innerHTML = marked.parse(markdownText);
    }
  }, speed);
}

// Send message
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;
  addMessage(text, "user");
  userInput.value = "";

  const typingElement = addTyping();

  try {
    const response = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_question: text })
    });

    const data = await response.json();
    const answer = data.final_answer || "No response";
    animateMarkdown(typingElement, answer);

  } catch (err) {
    typingElement.innerText = "❌ Error connecting to backend";
  }
}
