<script setup>
import iitm_logo from '@/assets/iitm_logo.png'

function reloadPage() {
  window.location.reload();
}
</script>
<template>
  <nav class="navbar">
    <div class="container">
      <!-- Logo Section -->
      <div class="logo-section">
        <!-- Use router-link instead of <a> -->
        <router-link @click.prevent="reloadPage" class="logo-link">
          <img  class="logo" :src="iitm_logo" alt="IITM Logo" />
          <span  class="title">Welcome To Indian Institute of Technology, Madras</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* Navbar styling */
.navbar {
  background: linear-gradient(to right, #ff7e5f, #7b4397);
  border-bottom: 2px solid #ffffff; /* Slightly darker green */
  padding: 20px 0;
}

.container {
  max-width: 800px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

/* Logo section styling */
.logo-section {
  display: flex;
  align-items: center;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.logo {
  height: 60px;
  width: auto;
}

.title {
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: bold;
  margin-left: 10px;
}

/* Navigation links styling */
.nav-links {
  display: flex;
  gap: 15px;
}

.nav-item {
  color: #ffffff;
  text-decoration: none;
  font-size: 1rem;
  padding: 8px 16px;
  border-radius: 4px;
  background-color: #803101; /* Medium green */
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: #832b06; /* Darker green for hover effect */
}
</style>
