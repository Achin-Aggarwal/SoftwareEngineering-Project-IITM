<script setup>
import Navbar from "@/components/Navbar.vue";
import studentProfile from "@/assets/studentProfile.png";

// Sample student data (can later be fetched from the backend)
const student = {
  name: "Atharva Sarbhukan",
  degree: "B.S. Degree in Data Science and Applications",
  branch: "Data Science and Programming",
  college: "Indian Institute of Technology, Madras",
  courses: [
    "Modern Application Development - 1",
    "Modern Application Development - 2",
    "Machine Learning Practice",
    "Business Data Management"
  ]
};
</script>

<template>
  <Navbar/>
  <div class="profile-page">
    <div class="profile-container">
      <div class="profile-header">

        <!-- Profile image on top -->
        <div class="image-container">
          <img
              :src="studentProfile"
              alt="Profile Picture"
              class="profile-image"
          />
        </div>

        <!-- Student details below the image -->
        <div class="student-details">
          <h2 class="student-name">{{ student.name }}</h2>
          <p class="degree-level">Degree: {{ student.degree }}</p>
          <p class="branch">Branch: {{ student.branch }}</p>
          <p class="college-name">College: {{ student.college }}</p>
        </div>
      </div>

      <!-- Courses section -->
      <div class="courses-section">
        <h3>Selected Courses</h3>
        <ul>
          <li v-for="(course, index) in student.courses" :key="index">{{ course }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  font-family: Arial, sans-serif;
  padding: 50px;
}

.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.image-container {
  padding-bottom: 25px;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.student-details {
  text-align: center;
}

.student-details h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.student-details p {
  margin: 5px 0;
  font-size: 16px;
}

.courses-section {
  margin-top: 30px;
}

.courses-section h3 {
  font-size: 22px;
  font-weight: bold;
  text-align: center;
}

.courses-section ul {
  list-style-type: none;
  padding: 0;
  text-align: center;
}

.courses-section li {
  font-size: 16px;
  margin: 5px 0;
}
</style>
