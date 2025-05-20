<script setup>
import iitm_logo from '@/assets/iitm_logo.png'
import {useRouter} from 'vue-router';
import {ref, onMounted} from 'vue';


// Get router instance
const router = useRouter();
const currentUsername = ref('');


// Get username on component mount
onMounted(() => {
 const storedUsername = localStorage.getItem('username');
 if (storedUsername) {
   currentUsername.value = storedUsername;
 }
});


function logout() {
 // Clear tokens from both localStorage and sessionStorage
 localStorage.removeItem('access_token');
 localStorage.removeItem('refresh_token');
 localStorage.removeItem('username');


 sessionStorage.removeItem('access_token');
 sessionStorage.removeItem('refresh_token');
 sessionStorage.removeItem('username');


 console.log('Logged out, credentials cleared');


 // Redirect to login page
 router.push('/login');
}


function reloadPage() {
 window.location.reload();
}


</script>
<template>
 <nav class="navbar">
   <div class="container">
     <!-- Logo Section -->
     <div class="logo-section" @click="reloadPage" style="cursor: pointer">
       <img class="logo" :src="iitm_logo" alt="IITM Logo"/>
       <span class="title">Instructor Page</span>
     </div>


     <!-- Navigation Links -->
     <div class="nav-links">
       <router-link :to="`/instructordashboard/${currentUsername}`" class="nav-item">Home</router-link>
       <router-link to="/instructorchatbot" class="nav-item">ChatBot</router-link>
       <router-link :to="`/instructorprofile/${currentUsername}`" class="nav-item">Profile</router-link>
       <a @click="logout" class="nav-item" style="cursor: pointer;">Logout</a>
     </div>
   </div>
 </nav>
</template>


<style scoped>
/* Navbar styling */
.navbar {
 background: linear-gradient(to right, #dc4825, #d96779);
 border-bottom: 2px solid #ffffff; /* Slightly darker green */
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
 background-color: #6224d5; /* Darker green for hover effect */
}
</style>

