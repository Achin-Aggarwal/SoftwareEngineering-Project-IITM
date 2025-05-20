<script setup>
import iitm_logo from '@/assets/iitm_logo.png';
import {ref, onMounted} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import axios from 'axios';

const router = useRouter();
const route = useRoute();
const currentUsername = ref(route.params.username || '');
const courses_data = ref([]);

onMounted(async () => {
  // Get username from localStorage if not in route
  if (!currentUsername.value) {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      currentUsername.value = storedUsername;
    }
  }

  // Fetch courses data from API
  await fetchCoursesData();
});

async function fetchCoursesData() {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      await router.push('/login');
      return;
    }

    const response = await axios.get('http://localhost:5000/student_dashboard', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    courses_data.value = response.data.courses_data;
    console.log(courses_data.value)
  } catch (error) {
    console.error('Error fetching courses data:', error);
    if (error.response && error.response.status === 401) {
      // Token expired or invalid
      await router.push('/login');
    }
  }
}

function reloadPage() {
  window.location.reload();
}

function logout() {
  // Clear tokens from both localStorage and sessionStorage for consistency
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('username');
  sessionStorage.removeItem('access_token');
  sessionStorage.removeItem('refresh_token');
  sessionStorage.removeItem('username');
  console.log('Logged out, credentials cleared');
  router.push('/login');
}
</script>

<template>
  <!-- Navbar Section -->
  <nav class="navbar">
    <div class="container">
      <div class="logo-section">
        <router-link @click.prevent="reloadPage" class="logo-link" to="/studentdashboard">
          <img class="logo" :src="iitm_logo" alt="IITM Logo"/>
          <span class="title">Student Dashboard</span>
        </router-link>
      </div>
      <div class="nav-links">
        <router-link :to="`/studentdashboard/${currentUsername}`" class="nav-item">Home</router-link>
        <router-link :to="`/profile/${currentUsername}`" class="nav-item">Profile</router-link>
        <a @click.prevent="logout" class="nav-item" style="cursor: pointer;">Logout</a>
      </div>
    </div>
  </nav>

  <!-- Course Cards Section -->
  <section class="py-4">
    <div class="container-xl lg:container m-auto">
      <h1 class="text-2xl font-bold text-black mb-6">My Current Courses</h1>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-4 rounded-lg">
        <div v-for="course in courses_data" :key="course.id" class="course-card">
          <h2 class="text-2xl font-bold">{{ course.name }}</h2>
          <router-link :to="`/course/${course.id}`">
            <button class="go-to-course-btn">Go to Course</button>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Navbar Styling */
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

.logo-section {
  display: flex;
  align-items: center;
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
  background-color: #6224d5;
}

.course-card {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.go-to-course-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #089f29;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.go-to-course-btn:hover {
  background-color: #45a049;
}

</style>