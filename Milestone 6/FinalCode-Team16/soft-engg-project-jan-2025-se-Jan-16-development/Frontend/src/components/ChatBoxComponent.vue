<template>
    <div class="chat-box">
      <div class="chat-header">
        <h3>Programming Assistant</h3>
        <button @click="$emit('close')">❌</button>
      </div>
      <div class="chat-messages">
        <div v-for="(message, index) in messages" :key="index" :class="message.sender">
          {{ message.text }}
        </div>
        <!-- Loading Indicator -->
        <div v-if="isLoading" class="bot typing-indicator">
          Typing...
        </div>
      </div>
      <div class="chat-input">
        <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Ask something..." :disabled="isLoading">
        <button @click="sendMessage" :disabled="isLoading">
          {{ isLoading ? 'Loading...' : 'Send' }}
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        newMessage: "",
        messages: [{ sender: "bot", text: "Hi! How can I assist you?", time: this.getCurrentTime() }],
        isLoading: false
      };
    },
    methods: {
      getCurrentTime() {
        const now = new Date();
        return `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`;
      },
      async sendMessage() {
        if (!this.newMessage.trim() || this.isLoading) return;
        this.messages.push({ sender: "user", text: this.newMessage, time: this.getCurrentTime() });
        const userQuery = this.newMessage;
        this.newMessage = "";
        this.isLoading = true;

        try {
            const token = localStorage.getItem("access_token");
            if (!token) {
            this.messages.push({ sender: "bot", text: "Unauthorized: No access token found.", time: this.getCurrentTime() });
            this.isLoading = false;
            return;
            }

            const response = await axios.post("http://127.0.0.1:5000/pchat", { query: userQuery }, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
            });

            console.log("API Response:", response.data);

            if (response.status === 200) {
            const fullResponse = response.data.response;

            // Debugging: Log the response received
            // console.log("Full Response:", fullResponse);

            // Extract only the Example Code block
            const match = fullResponse.match(/Example Code:\s*```python([\s\S]*?)```/);

            let formattedMessage;
            if (match) {
                formattedMessage = match[1].trim();
            } else {
                formattedMessage = "No example code found.";
            }

            // Log extracted match for debugging
            // console.log("Extracted Code:", formattedMessage);

            this.messages.push({ sender: "bot", text: formattedMessage, time: this.getCurrentTime() });
            } else {
            this.messages.push({ sender: "bot", text: response.data.error || "Error: Unable to process your request.", time: this.getCurrentTime() });
            }
        } catch (error) {
            this.messages.push({ sender: "bot", text: "Error: Unable to connect to server.", time: this.getCurrentTime() });
        } finally {
            this.isLoading = false;
            this.$nextTick(() => {
            const chatMessages = document.querySelector('.chat-messages');
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            });
        }
        }
    }
  };
  </script>
  
  <style>
  .chat-box {
    position: fixed;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    width: 350px;
    height: 450px;
    background: white;
    border-radius: 10px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    font-family: Arial, sans-serif;
  }
  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #007bff;
    color: white;
    padding: 12px;
    font-weight: bold;
  }
  .chat-header button {
    background: transparent;
    border: none;
    color: white;
    font-size: 16px;
    cursor: pointer;
  }
  .chat-messages {
    height: 350px;
    overflow-y: auto;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    scrollbar-width: thin;
  }
  .chat-input {
    display: flex;
    padding: 8px;
    border-top: 1px solid #ddd;
    background: #f9f9f9;
  }
  .chat-input input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    outline: none;
  }
  .chat-input button {
    margin-left: 8px;
    padding: 10px 15px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: 0.3s;
  }
  .chat-input button:hover {
    background: #0056b3;
  }
  .chat-input button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
  .user {
    align-self: flex-end;
    background: #e3f2fd;
    color: #007bff;
    padding: 8px 12px;
    border-radius: 10px;
    max-width: 70%;
  }
  .bot {
    align-self: flex-start;
    background: #d4edda;
    color: #155724;
    padding: 8px 12px;
    border-radius: 10px;
    max-width: 70%;
  }
  .typing-indicator {
    align-self: flex-start;
    font-style: italic;
    color: #777;
  }
  </style>
  