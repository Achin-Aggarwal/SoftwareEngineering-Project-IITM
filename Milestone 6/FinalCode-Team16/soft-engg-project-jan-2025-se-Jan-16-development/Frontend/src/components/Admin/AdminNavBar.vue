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
      <div class="logo-section" @click="reloadPage" style="cursor:pointer">
        <img class="logo" :src="iitm_logo" alt="IITM Logo"/>
        <span class="title">Admin Dashboard</span>
      </div>

      <!-- Navigation Links -->
      <div class="nav-links">
        <router-link to="/adminpage/:username" class="nav-item">Home</router-link>
        <router-link to="/adminchatbot" class="nav-item">ChatBot</router-link>
        <router-link to="/admin/profile" class="nav-item">Profile</router-link>
        <router-link to="/" class="nav-item">Logout</router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* Navbar styling */
.navbar {
  background: linear-gradient(to right, #dc4825, #d96779);
  border-bottom: 2px solid #ffffff;
  padding: 10px 0;
}

.container {
  max-width: 1800px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
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
  cursor: pointer;
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
  background-color: transparent;
  color: #ffffff;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 24px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-item:hover {
  background-color: #6224d5; /* Even darker orange for hover effect */
}
</style>