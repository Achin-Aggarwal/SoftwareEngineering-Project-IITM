<template>
  <div>
    <button class="chat-button" @click="toggleChat">💬</button>
    <div v-if="chatOpen" class="chat-window">
      <div class="chat-header">
        <span>AI Agent</span>
        <button class="close-btn" @click="toggleChat">✖</button>
      </div>
      <div class="chat-body">
        <div class="chat-bubble bot">Hello! How can I assist you today?</div>
      </div>
      <div class="chat-input">
        <input type="text" placeholder="Type your message..." v-model="userMessage" @keyup.enter="sendMessage"/>
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      chatOpen: false,
      userMessage: '',
    };
  },
  methods: {
    toggleChat() {
      this.chatOpen = !this.chatOpen;
    },
    sendMessage() {
      if (this.userMessage.trim()) {
        // Add user's message to the chat
        const userBubble = `<div class="chat-bubble user">${this.userMessage}</div>`;
        const botBubble = `<div class="chat-bubble bot">I'm here to assist you!</div>`;
        const chatBody = document.querySelector('.chat-body');
        chatBody.innerHTML += userBubble + botBubble;

        // Clear the input field
        this.userMessage = '';

        // Scroll to the bottom of the chat
        chatBody.scrollTop = chatBody.scrollHeight;
      }
    },
  },
};
</script>



<style scoped>
.chat-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background: #007bff;
  color: white;
  border: none;
  padding: 20px;
  cursor: pointer;
  border-radius: 50%;
  font-size: 26px;
}

.chat-window {
  position: fixed;
  bottom: 90px;
  right: 30px;
  width: 500px;
  height: 450px;
  background: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s ease;
}

.chat-header {
  background-color: #007bff;
  color: white;
  padding: 15px;
  font-size: 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: "Comic Sans MS", serif;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 22px;
  cursor: pointer;
}

.chat-body {
  flex-grow: 1;
  padding: 15px;
  overflow-y: auto;
  height: 500px;
}

.chat-bubble {
  max-width: 85%;
  margin-bottom: 15px;
  padding: 12px 20px;
  border-radius: 25px;
  display: inline-block;
  clear: both;
}

.chat-bubble.user {
  background-color: #007bff;
  color: white;
  align-self: flex-end;
  border-radius: 25px 25px 0 25px;
}

.chat-bubble.bot {
  background-color: #f1f1f1;
  color: #333;
  align-self: flex-start;
  border-radius: 25px 25px 25px 0;
}

.chat-input {
  display: flex;
  padding: 15px;
  background-color: #f1f1f1;
}

.chat-input input {
  width: 85%;
  padding: 12px;
  border: none;
  border-radius: 25px;
  margin-right: 15px;
  font-size: 16px;
}

.chat-input button {
  padding: 12px;
  border: none;
  border-radius: 50%;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  font-size: 16px;
}

.chat-input input:focus {
  outline: none;
}

.chat-window .chat-body {
  max-height: 300px;
  overflow-y: scroll;
}
</style>