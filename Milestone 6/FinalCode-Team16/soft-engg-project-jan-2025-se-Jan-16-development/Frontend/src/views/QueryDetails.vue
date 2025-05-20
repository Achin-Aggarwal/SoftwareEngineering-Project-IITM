<template>
  <instructor-nav-bar/>
  <div class="query-details-container">
    <div class="back-button">
      <button @click="goBack">← Back to Dashboard</button>
    </div>
 
 
    <div v-if="query" class="query-card">
      <div class="query-header">
        <h1>{{ query.subject }}</h1>
      </div>
 
 
      <div class="query-info">
        <div class="info-item">
          <span class="label">Frequency:</span>
          <span>Asked {{ $route.query.count }} times</span>
        </div>
      </div>
 
 
      <div class="query-resolution">
        <div class="resolution-actions">
          <button class="chatbot-button" @click="useAssistant">
            Use Chatbot Assistant
          </button>
        </div>
      </div>
    </div>
 
 
    <div v-else class="loading">
      Loading query details...
    </div>
  </div>
 </template>
 
 
 <script>
 import InstructorNavBar from "@/components/Instructor/InstructorNavBar.vue";
 
 
 export default {
  name: 'QueryDetails',
  components: {
    InstructorNavBar
  },
  data() {
    return {
      query: null
    }
  },
  created() {
    // Use route query or params to populate query details
    this.query = {
      subject: this.$route.query.subject || 'Query Details',
      id: parseInt(this.$route.params.id)
    }
  },
  methods: {
    useAssistant() {
      // Navigate to the chatbot view with query details
      this.$router.push({
        name: 'InstructorQueryChatBot',
        query: {
          prefill: this.query.subject,
          queryId: this.query.id
        }
      })
    },
    goBack() {
      this.$router.push({name: 'InstructorDashboard'})
    }
  }
 }
 </script>
 
 
 
 
 <style scoped>
 .query-details-container {
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
 }
 
 
 .back-button button {
  background: none;
  border: none;
  color: #7b4397;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.5rem 0;
  margin-bottom: 1rem;
 }
 
 
 .query-card {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
 }
 
 
 .query-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
 }
 
 
 .query-header h1 {
  margin: 0;
  font-size: 1.8rem;
 }
 
 
 .status-tag {
  padding: 0.3rem 0.8rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 500;
 }
 
 
 .status-pending {
  background-color: #fff3e0;
  color: #e67e22;
 }
 
 
 .status-resolved {
  background-color: #e0f2f1;
  color: #27ae60;
 }
 
 
 .query-info {
  display: flex;
  margin-bottom: 1.5rem;
 }
 
 
 .info-item {
  margin-right: 2rem;
 }
 
 
 .label {
  font-weight: 500;
  margin-right: 0.5rem;
 }
 
 
 .query-content, .query-response {
  margin-bottom: 2rem;
 }
 
 
 .query-content h3, .query-response h3, .query-resolution h3, .related-resources h3 {
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  color: #333;
 }
 
 
 .query-resolution textarea {
  width: 100%;
  min-height: 150px;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;
  font-family: inherit;
  font-size: 1rem;
  margin-bottom: 1rem;
  resize: vertical;
 }
 
 
 .resolution-actions {
  display: flex;
  gap: 1rem;
 }
 
 
 .resolve-button, .chatbot-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
 }
 
 
 .resolve-button {
  background-color: #27ae60;
  color: white;
 }
 
 
 .resolve-button:hover {
  background-color: #219653;
 }
 
 
 .chatbot-button {
  background: linear-gradient(to right, #ff7e5f, #9b32c9);
  color: white;
 }
 
 
 .chatbot-button:hover {
  background-color: #2980b9;
 }
 
 
 .related-resources {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
 }
 
 
 .resource-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
 }
 
 
 .resource-item {
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 1rem;
 }
 
 
 .resource-item h4 {
  margin-top: 0;
  color: #3498db;
 }
 
 
 .resource-item a {
  display: inline-block;
  color: #3498db;
  margin-top: 0.5rem;
  text-decoration: none;
 }
 
 
 .resource-item a:hover {
  text-decoration: underline;
 }
 
 
 .loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
 }
 
 
 @media (max-width: 768px) {
  .query-header {
    flex-direction: column;
    align-items: flex-start;
  }
 
 
  .status-tag {
    margin-top: 0.5rem;
  }
 
 
  .query-info {
    flex-direction: column;
  }
 
 
  .info-item {
    margin-bottom: 0.5rem;
  }
 
 
  .resource-list {
    grid-template-columns: 1fr;
  }
 
 
  .resolution-actions {
    flex-direction: column;
  }
 
 
  .resolve-button, .chatbot-button {
    width: 100%;
  }
 }
 </style>
 
 