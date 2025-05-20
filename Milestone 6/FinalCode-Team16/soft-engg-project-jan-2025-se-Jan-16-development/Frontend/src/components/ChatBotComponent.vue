<template>
  <div>
    <button class="chat-button" @click="toggleChat">
      <span class="chat-icon">💬</span>
    </button>
    <div v-if="chatOpen" class="chat-window">
      <div class="chat-header">
        <div class="header-content">
          <div class="avatar">AI</div>
          <span class="title">Support Assistant</span>
        </div>
        <button class="close-btn" @click="toggleChat">✖</button>
      </div>
      <div class="chat-body">
        <div v-for="(message, index) in chatMessages" :key="index" class="chat-bubble" :class="message.sender">
          <template v-if="message.sender === 'bot'">
            <div v-for="(line, i) in message.text.split('\n')" :key="i">{{ line }}</div>
          </template>
          <template v-else>
            {{ message.text }}
          </template>
          <span class="message-time">{{ message.time }}</span>
        </div>
        <div v-if="isLoading" class="loading-indicator">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
      </div>
      <div class="chat-input">
        <input v-model="userMessage" type="text" placeholder="Type your message..." @keyup.enter="sendMessage" :disabled="isLoading" />
        <button @click="sendMessage" :disabled="isLoading">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      chatOpen: false,
      userMessage: '',
      chatMessages: [{ sender: 'bot', text: 'Hello! How can I assist you today?', time: this.getCurrentTime() }],
      isLoading: false
    };
  },
  methods: {
    toggleChat() {
      this.chatOpen = !this.chatOpen;
    },
    getCurrentTime() {
      const now = new Date();
      return `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`;
    },
    async sendMessage() {
      if (!this.userMessage.trim() || this.isLoading) return;
      this.chatMessages.push({ sender: 'user', text: this.userMessage, time: this.getCurrentTime() });
      const userQuery = this.userMessage;
      this.userMessage = '';
      this.isLoading = true;

      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          this.chatMessages.push({ sender: 'bot', text: 'Unauthorized: No access token found.', time: this.getCurrentTime() });
          this.isLoading = false;
          return;
        }

        const response = await axios.post("http://127.0.0.1:5000/chat", { query: userQuery }, {
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          }
        });

        console.log("API Response:", response.data);

        if (response.status === 200) {
          const formattedMessage = response.data.response ? response.data.response.replace(/\. /g, '.\n') : "I'm here to assist you!";
          this.chatMessages.push({ sender: 'bot', text: formattedMessage, time: this.getCurrentTime() });
        } else {
          this.chatMessages.push({ sender: 'bot', text: response.data.error || "Error: Unable to process your request.", time: this.getCurrentTime() });
        }
      } catch (error) {
        this.chatMessages.push({ sender: 'bot', text: "Error: Unable to connect to server.", time: this.getCurrentTime() });
      } finally {
        this.isLoading = false;
        this.$nextTick(() => {
          const chatBody = document.querySelector('.chat-body');
          if (chatBody) {
            chatBody.scrollTop = chatBody.scrollHeight;
          }
        });
      }
    }
  }
};
</script>

<style scoped>
/* Base styling */
* {
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Chat button styling */
.chat-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background: linear-gradient(135deg, #2563eb, #1e40af);
  color: white;
  border: none;
  width: 60px;
  height: 60px;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.chat-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.chat-icon {
  font-size: 24px;
}

/* Chat window styling */
.chat-window {
  position: fixed;
  bottom: 100px;
  right: 30px;
  width: 380px;
  height: 500px;
  background: #fff;
  border: none;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s ease;
  z-index: 1000;
}

/* Header styling */
.chat-header {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  color: white;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content {
  display: flex;
  align-items: center;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: white;
  color: #1e40af;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 12px;
  font-size: 14px;
}

.title {
  font-size: 16px;
  font-weight: 600;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Chat body styling */
.chat-body {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f8fafc;
}

.chat-bubble {
  max-width: 85%;
  margin-bottom: 16px;
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  clear: both;
  line-height: 1.5;
  font-size: 14px;
}

.chat-bubble.user {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  color: white;
  float: right;
  border-bottom-right-radius: 4px;
}

.chat-bubble.bot {
  background-color: white;
  color: #334155;
  float: left;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.message-time {
  font-size: 10px;
  opacity: 0.7;
  display: block;
  margin-top: 6px;
  text-align: right;
}

/* Loading indicator */
.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  clear: both;
  margin: 10px auto;
  width: 70px;
}

.dot {
  width: 8px;
  height: 8px;
  margin: 0 4px;
  background-color: #2563eb;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  } 40% {
      transform: scale(1.0);
    }
}

/* Input area styling */
.chat-input {
  display: flex;
  padding: 16px;
  background-color: white;
  border-top: 1px solid #e2e8f0;
}

.chat-input input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  font-size: 14px;
  transition: border 0.2s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.chat-input input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}

.chat-input input:disabled {
  background-color: #f1f5f9;
  cursor: not-allowed;
}

.chat-input button {
  width: 40px;
  height: 40px;
  margin-left: 12px;
  background: linear-gradient(135deg, #2563eb, #1e40af);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.chat-input button:hover {
  transform: scale(1.05);
}

.button-disabled {
  opacity: 0.6;
  cursor: not-allowed !important;
  transform: scale(1) !important;
}

.chat-input button:disabled {
  cursor: not-allowed;
}

/* Scrollbar styling */
.chat-body::-webkit-scrollbar {
  width: 6px;
}

.chat-body::-webkit-scrollbar-track {
  background: #f8fafc;
}

.chat-body::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 6px;
}
</style>