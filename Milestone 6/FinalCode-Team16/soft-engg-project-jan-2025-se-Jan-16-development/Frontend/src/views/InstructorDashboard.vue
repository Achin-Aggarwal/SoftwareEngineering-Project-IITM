<template>
  <InstructorNavBar/>
  <div class="dashboard-container">
    <label>Welcome, {{ instructorName }}</label>
    <br>
    <br>
 
 
    <div class="quick-actions">
      <h2>Quick Actions</h2>
      <br>
      <div class="action-buttons">
        <router-link to="/add-live-session" class="action-button">
          <i class="fas fa-video"></i>
          Add Live Session
        </router-link>
        <router-link to="/add-assignment" class="action-button">
          <i class="fas fa-video"></i>
          Add Assignment
        </router-link>
      </div>
    </div>
 
 
    <div class="top-queries-section">
      <h2>Top 5 Student Queries</h2>
      <br>
      <div v-if="loading">Loading...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="query-list">
        <div
            v-for="query in weeklyQueries"
            :key="query.id"
            class="query-card"
            @click="goToQueryDetails(query)"
        >
          <h3>{{ query.query_text }}</h3>
          <p class="query-preview">Asked {{ query.count }} times</p>
        </div>
      </div>
    </div>
  </div>
 </template>
 
 
 <script>
 import axios from 'axios';
 import InstructorNavBar from "@/components/Instructor/InstructorNavBar.vue";
 
 
 export default {
  name: 'Dashboard',
  components: {
    InstructorNavBar
  },
  data() {
    return {
      weeklyQueries: [],
      loading: true,
      error: null
    };
  },
  computed: {
    instructorName() {
      const instructorData = JSON.parse(localStorage.getItem('instructorData') || '{}');
      return instructorData.name || 'Instructor';
    }
  },
  methods: {
    async fetchTopQueries() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://127.0.0.1:5000/topquery", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        // Add an ID to each query for navigation
        this.weeklyQueries = response.data.map((query, index) => ({
          ...query,
          id: index + 1
        }));
      } catch (error) {
        this.error = error.response ? error.response.data.message : error.message;
      } finally {
        this.loading = false;
      }
    },
    goToQueryDetails(query) {
      this.$router.push({
        name: 'QueryDetails',
        params: {id: query.id},
        query: {
          subject: query.query_text,
          count: query.count
        }
      });
    }
  },
  mounted() {
    this.fetchTopQueries();
  }
 };
 </script>
 
 
 
 
 <style scoped>
 .dashboard-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
 }
 
 
 .top-queries-section, .quick-actions {
  background-color: #f7f9f7;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 5px 9px rgba(0.5, 0, 0, 0.1);
  margin-bottom: 2rem;
 }
 
 
 .query-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
 }
 
 
 .query-card {
  border: 1px solid #a225cb;
  box-shadow: 0 5px 9px rgba(0.5, 0.5, 0.5, 0.1);
  border-radius: 20px;
  padding: 1rem;
  transition: transform 0.2s;
 }
 
 
 .query-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(1, 0.5, 0, 0.1);
 }
 
 
 .action-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
 }
 
 
 .action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
   background: linear-gradient(to right, #dc4825, #d96779);
  border-radius: 20px;
  padding: 1.5rem;
  text-decoration: none;
  color: #fefefe;
  transition: background-color 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  font-size: 1.2rem;
 }
 
 
 .action-button:hover {
  background-color: #f2873e;
 }
 
 
 .action-button i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #3498db;
 }
 
 
 @media (max-width: 768px) {
  .dashboard-stats, .action-buttons {
    grid-template-columns: 1fr;
  }
 }
 </style>
 
 