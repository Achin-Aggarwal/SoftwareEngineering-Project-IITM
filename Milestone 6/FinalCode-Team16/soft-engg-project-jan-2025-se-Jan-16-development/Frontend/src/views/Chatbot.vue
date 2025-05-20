<template>
  <div class="chatbot-container">
    <div class="chatbot-card">
      <div class="chat-header">
        <h2>Chatbot Assistant</h2>
        <p>Use the chatbot to get responses or answers of technical questions.</p>
      </div>
      <div class="chat-messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
          <div class="message-content">
            <p v-html="formatMessage(message.text)"></p>
          </div>
          <div v-if="message.sender === 'chatbot'" class="message-actions">
            <button @click="copyToResponse(message.text)" class="copy-button">Copy Response</button>
          </div>
        </div>
        <!-- Loading Animation -->
        <div v-if="isLoading" class="message chatbot loading-message">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
      <div class="chat-input">
        <textarea v-model="newMessage" placeholder="Type your message here..." @keydown.enter.prevent="sendMessage"
                  rows="3"></textarea>
        <button @click="sendMessage" :disabled="!newMessage.trim() || isLoading" class="send-button">
          <span v-if="!isLoading"></span>
          <span v-else class="send-loading"></span>
        </button>
      </div>
      <div v-if="queryInfo" class="query-context">
        <h3>Current Query Context</h3>
        <div class="query-context-info">
          <p><strong>Query ID:</strong> {{ queryInfo.id }}</p>
          <p><strong>Subject:</strong> {{ queryInfo.subject }}</p>
        </div>
        <button @click="goToQueryDetails" class="context-action-button">
          Go to Query Details
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Chatbot',
  data() {
    return {
      messages: [
        {
          sender: 'chatbot',
          text: 'Hello! I\'m your AI assistant. How can I help you today?'
        }
      ],
      newMessage: '',
      queryInfo: null,
      isLoading: false,
      apiUrl: 'http://127.0.0.1:5000/chat' // API endpoint for chat service
    }
  },
  mounted() {
    // Check if we have pre-filled message from query details
    const prefill = this.$route.query.prefill
    const queryId = this.$route.query.queryId
    if (prefill) {
      this.newMessage = prefill
      // Fetch query details if
      if (queryId) {
        this.fetchQueryInfo(queryId)
      }
    }
    this.scrollToBottom()
  },
  updated() {
    this.scrollToBottom()
  },
  methods: {
    async sendMessage() {
      if (!this.newMessage.trim() || this.isLoading) return

      // Add user message
      this.messages.push({
        sender: 'user',
        text: this.newMessage
      })
      const userMessage = this.newMessage
      this.newMessage = ''

      // Show loading animation
      this.isLoading = true

      try {
        // Call the chatbot API
        const token = localStorage.getItem("access_token");
        const response = await fetch(this.apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', "Authorization": `Bearer ${token}` },
          body: JSON.stringify({ query: userMessage })
        });

        if (response.ok) {
          const data = await response.json();
          this.messages.push({
            sender: 'chatbot',
            text: data.response || 'I understand your message. How can I assist further?'
          });
        } else {
          // Handle error response
          this.messages.push({
            sender: 'chatbot',
            text: 'Sorry, I encountered an error processing your request. Please try again later.'
          });
        }
      } catch (error) {
        // Handle network or other errors
        console.error('Chat API error:', error);
        this.messages.push({
          sender: 'chatbot',
          text: 'Error: Unable to connect to the server. Please check your connection and try again.'
        });
      } finally {
        this.isLoading = false;
      }
    },

    formatMessage(text) {
      // Format code blocks, links, etc.
      return text
          // Replace URLs with clickable links
          .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>')
      // Other formatting could be added here
    },

    copyToResponse(text) {
      // Strip HTML tags to get plain text
      const plainText = text.replace(/<[^>]*>/g, '');

      // Copy to clipboard
      navigator.clipboard.writeText(plainText).then(() => {
        alert("Copied to clipboard!"); // Optional: Show confirmation
      }).catch(err => {
        console.error("Failed to copy: ", err);
      });

      // Emit event for parent component if needed
      this.$emit('use-response', plainText);

      // Navigate to another view with the copied response
      this.$router.push({
        name: 'query-response',
        query: {
          responseText: plainText,
          queryId: this.queryInfo ? this.queryInfo.id : null
        }
      }).catch(err => console.warn("Navigation error: ", err));
    },

    scrollToBottom() {
      if (this.$refs.messagesContainer) {
        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight
      }
    },

    fetchQueryInfo(queryId) {
      // In a real app, this would be an API call
      // For now, simulate with dummy data
      setTimeout(() => {
        this.queryInfo = {
          id: queryId,
          subject: 'Technical Support Request #' + queryId,
          // Other query details could be added here
        }
      }, 500)
    },

    goToQueryDetails() {
      if (this.queryInfo) {
        this.$router.push({
          name: 'QueryDetails',
          params: {id: this.queryInfo.id}
        })
      }
    }
  }
}
</script>

<style scoped>
.chatbot-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Inter', 'Segoe UI', Roboto, -apple-system, sans-serif;
}

.chatbot-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  background-color: #fff;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 690px;
}

.chat-header {
  padding: 16px 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eaeaea;
  display: flex;
  flex-direction: column;
}

.chat-header h2 {
  margin: 0 0 6px 0;
  font-size: 1.25rem;
  color: #2d3748;
  font-weight: 600;
}

.chat-header p {
  margin: 0;
  font-size: 0.875rem;
  color: #718096;
  line-height: 1.4;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background-color: #f9fafc;
  background-image: radial-gradient(circle at 25px 25px, rgba(20, 227, 148, 0.05) 2%, transparent 0%),
  radial-gradient(circle at 75px 75px, rgba(0, 123, 255, 0.05) 2%, transparent 0%);
  background-size: 100px 100px;
  scrollbar-width: thin;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.message {
  max-width: 75%;
  padding: 14px 18px;
  border-radius: 18px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  position: relative;
  animation: messageAppear 0.3s ease-out;
}

@keyframes messageAppear {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #1a73e8, #4e87e3);
  color: #ffffff;
  border-bottom-right-radius: 4px;
}

.message.user::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: -8px;
  width: 16px;
  height: 16px;
  background: linear-gradient(225deg, #0d62c8, transparent);
  border-bottom-left-radius: 15px;
}

.message.chatbot {
  align-self: flex-start;
  background-color: white;
  color: #2d3748;
  border: 1px solid #eaeaea;
  border-bottom-left-radius: 4px;
}

.message.chatbot::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: -8px;
  width: 16px;
  height: 16px;
  background: white;
  border-left: 1px solid #eaeaea;
  border-bottom: 1px solid #eaeaea;
  border-bottom-right-radius: 15px;
}

.message-content p {
  margin: 0;
  word-break: break-word;
  line-height: 1.5;
  font-size: 0.95rem;
}

.message-content a {
  color: inherit;
  text-decoration: underline;
}

.message-content code {
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 0.9em;
  padding: 2px 5px;
  background: rgba(0, 0, 0, 0.06);
  border-radius: 3px;
}

.message-content pre {
  margin: 10px 0;
  padding: 12px;
  background: #2b2b2b;
  color: #f8f8f2;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.9em;
}

.message-content pre code {
  background: transparent;
  padding: 0;
  color: inherit;
  font-family: 'Fira Code', 'Consolas', monospace;
}

.message-actions {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.message:hover .message-actions {
  opacity: 1;
}

.copy-button {
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 0.8rem;
  cursor: pointer;
  color: #4a5568;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s ease;
}

.copy-button:hover {
  background-color: #f5f7fa;
  border-color: #cbd5e0;
}

.copy-button::before {
  content: '';
  display: inline-block;
  width: 14px;
  height: 14px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234a5568' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='9' y='9' width='13' height='13' rx='2' ry='2'/%3E%3Cpath d='M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.chat-input {
  padding: 16px 20px;
  border-top: 1px solid #eaeaea;
  display: flex;
  gap: 12px;
  background-color: white;
}

.chat-input textarea {
  flex: 1;
  padding: 13px 16px;
  border: 1px solid #dcdfe4;
  border-radius: 24px;
  resize: none;
  font-family: inherit;
  font-size: 0.95rem;
  line-height: 1.5;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.chat-input textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
}

.chat-input textarea::placeholder {
  color: #a0aec0;
}

.send-button {
  background-color: #1a73e8;
  color: white;
  border: none;
  border-radius: 24px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  flex-shrink: 0;
  box-shadow: 0 2px 5px rgba(26, 115, 232, 0.2);
  position: relative;
}

.send-button > span:not(.send-loading) {
  width: 20px;
  height: 20px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='22' y1='2' x2='11' y2='13'/%3E%3Cpolygon points='22 2 15 22 11 13 2 9 22 2'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  display: inline-block;
}

.send-loading {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.send-button:hover {
  background-color: #0d62c8;
}

.send-button:active {
  transform: scale(0.97);
}

.send-button:disabled {
  background-color: #cbd5e0;
  cursor: not-allowed;
  box-shadow: none;
}

.query-context {
  padding: 16px 20px;
  border-top: 1px solid #eaeaea;
  background-color: #f8f9fa;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.query-context h3 {
  margin: 0 0 10px 0;
  font-size: 0.95rem;
  color: #4a5568;
  font-weight: 600;
}

.query-context-info {
  margin-bottom: 12px;
  padding: 10px 14px;
  background-color: white;
  border-radius: 8px;
  border: 1px solid #eaeaea;
}

.query-context-info p {
  margin: 6px 0;
  font-size: 0.875rem;
  color: #4a5568;
  display: flex;
  align-items: center;
  gap: 6px;
}

.query-context-info p strong {
  color: #2d3748;
  font-weight: 600;
}

.context-action-button {
  background-color: #4a5568;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 16px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.2s, transform 0.1s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.context-action-button::before {
  content: '';
  display: inline-block;
  width: 16px;
  height: 16px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cpolyline points='12 16 16 12 12 8'/%3E%3Cline x1='8' y1='12' x2='16' y2='12'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.context-action-button:hover {
  background-color: #2d3748;
}

.context-action-button:active {
  transform: scale(0.98);
}

/* Typing indicator styles */
.loading-message {
  padding: 12px 16px;
  min-height: 42px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: #cbd5e0;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
    background-color: #cbd5e0;
  }
  40% {
    transform: scale(1.0);
    background-color: #4299e1;
  }
}
</style>