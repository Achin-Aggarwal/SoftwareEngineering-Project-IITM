<!--<script setup>-->
<!--import {ref, onMounted} from "vue";-->
<!--import Navbar from "@/components/Student/Navbar.vue";-->
<!--import studentProfile from "@/assets/studentProfile.png";-->
<!--import axios from "axios";-->

<!--// Create reactive student data-->
<!--const student = ref({-->
<!--  name: "",-->
<!--  email: "",-->
<!--  username: "",-->
<!--  role: "",-->
<!--  last_login: "",-->
<!--  // Keep the static data for now as they're not in the API-->
<!--  degree: "B.S. Degree in Data Science and Applications",-->
<!--  branch: "Data Science and Programming",-->
<!--  college: "Indian Institute of Technology, Madras"-->
<!--});-->

<!--// New reactive property for courses data from dashboard API-->
<!--const enrolledCourses = ref([]);-->
<!--const enrolledCourses1 = ref([]);-->

<!--// Fetch student profile data from API-->
<!--const fetchStudentProfile = async () => {-->
<!--  try {-->
<!--    const token = localStorage.getItem("access_token");-->
<!--    if (!token) {-->
<!--      console.error("No access token found");-->
<!--      return;-->
<!--    }-->

<!--    const response = await axios.get("http://localhost:5000/student_profile", {-->
<!--      headers: {-->
<!--        Authorization: `Bearer ${token}`-->
<!--      }-->
<!--    });-->

<!--    // Update the student data with API response-->
<!--    const profileData = response.data;-->
<!--    // console.log("profile",profileData)-->
<!--    enrolledCourses1.value = response.data.courses;-->
<!--    student.value = {-->
<!--      ...student.value,-->
<!--      name: profileData.name,-->
<!--      email: profileData.email,-->
<!--      username: profileData.username,-->
<!--      role: profileData.role,-->
<!--      last_login: profileData.last_login-->
<!--    };-->
<!--  } catch (error) {-->
<!--    console.error("Error fetching student profile:", error);-->
<!--  }-->
<!--};-->

<!--// New function to fetch courses from dashboard API-->
<!--const fetchStudentDashboard = async () => {-->
<!--  try {-->
<!--    const token = localStorage.getItem("access_token");-->
<!--    if (!token) {-->
<!--      console.error("No access token found");-->
<!--      return;-->
<!--    }-->

<!--    const response = await axios.get("http://localhost:5000/student_dashboard", {-->
<!--      headers: {-->
<!--        Authorization: `Bearer ${token}`-->
<!--      }-->
<!--    });-->

<!--    // Update enrolled courses with data from API-->
<!--    enrolledCourses.value = response.data.courses_data;-->
<!--  } catch (error) {-->
<!--    console.error("Error fetching student dashboard:", error);-->
<!--  }-->
<!--};-->

<!--// Fetch data when component mounts-->
<!--onMounted(() => {-->
<!--  fetchStudentProfile();-->
<!--  fetchStudentDashboard();-->
<!--});-->
<!--</script>-->

<!--<template>-->
<!--  <Navbar/>-->
<!--  <div class="profile-page">-->
<!--    <div class="profile-container">-->
<!--      <div class="profile-header">-->
<!--        &lt;!&ndash; Profile image on top &ndash;&gt;-->
<!--        <div class="image-container">-->
<!--          <img-->
<!--              :src="studentProfile"-->
<!--              alt="Profile Picture"-->
<!--              class="profile-image"-->
<!--          />-->
<!--        </div>-->

<!--        &lt;!&ndash; Student details below the image &ndash;&gt;-->
<!--        <div class="student-details">-->
<!--          <h2 class="student-name">{{ student.name }}</h2>-->
<!--          <p class="email"><strong>Email:</strong> {{ student.email }}</p>-->
<!--          <p class="username"><strong>Username:</strong> {{ student.username }}</p>-->
<!--          <p class="role"><strong>Role:</strong> {{ student.role }}</p>-->
<!--          <p class="last-login"><strong>Last Login:</strong> {{ student.last_login }}</p>-->
<!--          <p class="degree-level"><strong>Degree:</strong> {{ student.degree }}</p>-->
<!--          <p class="branch"><strong>Branch:</strong> {{ student.branch }}</p>-->
<!--          <p class="college-name"><strong>College:</strong> {{ student.college }}</p>-->
<!--        </div>-->
<!--      </div>-->




<!--      &lt;!&ndash; Courses section &ndash;&gt;-->
<!--      <div class="courses-section">-->
<!--        <h3>Selected Courses</h3>-->
<!--        <ul>-->
<!--          <li v-for="course in enrolledCourses1" :key="course.course_name" class="course-item">-->
<!--            <strong>{{ course.course_name }}</strong>-->
<!--            <ul v-if="course.assignments.length">-->
<!--              <li v-for="assignment in course.assignments" :key="assignment.week_number" class="assignment-item">-->
<!--                <span><strong>Type:</strong> {{ assignment.assignment_type }}</span> |-->
<!--                <span><strong>Week:</strong> {{ assignment.week_number }}</span> |-->
<!--                <span><strong>Score:</strong> {{ assignment.score }}</span>-->
<!--              </li>-->
<!--            </ul>-->
<!--            <p v-else class="no-assignments">No assignments available</p>-->
<!--          </li>-->
<!--        </ul>-->
<!--      </div>-->

<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<style scoped>-->
<!--.profile-page {-->
<!--  font-family: Arial, sans-serif;-->
<!--  padding: 50px;-->
<!--}-->

<!--.profile-container {-->
<!--  max-width: 800px;-->
<!--  margin: 0 auto;-->
<!--  padding: 20px;-->
<!--  background-color: #f9f9f9;-->
<!--  border-radius: 8px;-->
<!--  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);-->
<!--}-->

<!--.profile-header {-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  align-items: center;-->
<!--  margin-bottom: 30px;-->
<!--}-->

<!--.image-container {-->
<!--  padding-bottom: 25px;-->
<!--  display: flex;-->
<!--  justify-content: center;-->
<!--  margin-bottom: 20px;-->
<!--}-->

<!--.profile-image {-->
<!--  width: 150px;-->
<!--  height: 150px;-->
<!--  border-radius: 50%;-->
<!--  object-fit: cover;-->
<!--}-->

<!--.student-details {-->
<!--  text-align: center;-->
<!--  width: 100%;-->
<!--}-->

<!--.student-details h2 {-->
<!--  margin: 0;-->
<!--  font-size: 24px;-->
<!--  font-weight: bold;-->
<!--  margin-bottom: 15px;-->
<!--}-->

<!--.student-details p {-->
<!--  margin: 5px 0;-->
<!--  font-size: 16px;-->
<!--}-->

<!--.courses-section {-->
<!--  margin-top: 30px;-->
<!--}-->

<!--.courses-section h3 {-->
<!--  font-size: 22px;-->
<!--  font-weight: bold;-->
<!--  text-align: center;-->
<!--}-->

<!--.courses-section ul {-->
<!--  list-style-type: none;-->
<!--  padding: 0;-->
<!--  text-align: center;-->
<!--}-->

<!--.courses-section li {-->
<!--  font-size: 16px;-->
<!--  margin: 5px 0;-->
<!--}-->
<!--</style>-->


<script setup>
import {ref, onMounted} from "vue";
import Navbar from "@/components/Student/Navbar.vue";
// import studentProfile from "@/assets/studentProfile.png";
import axios from "axios";

// Create reactive student data
const student = ref({
  name: "",
  email: "",
  username: "",
  role: "",
  last_login: "",
  // Keep the static data for now as they're not in the API
  degree: "B.S. Degree in Data Science and Applications",
  branch: "Data Science and Programming",
  college: "Indian Institute of Technology, Madras"
});

const gender = Math.random() < 0.5 ? "men" : "women";
const number = Math.floor(Math.random() * 100);
const studentProfile = ref(`https://randomuser.me/api/portraits/${gender}/${number}.jpg`);

// New reactive property for courses data from dashboard API
const enrolledCourses = ref([]);
const enrolledCourses1 = ref([]);

// Fetch student profile data from API
const fetchStudentProfile = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      console.error("No access token found");
      return;
    }

    const response = await axios.get("http://localhost:5000/student_profile", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    // Update the student data with API response
    const profileData = response.data;
    // console.log("profile",profileData)
    enrolledCourses1.value = response.data.courses;
    student.value = {
      ...student.value,
      name: profileData.name,
      email: profileData.email,
      username: profileData.username,
      role: profileData.role,
      last_login: profileData.last_login
    };
  } catch (error) {
    console.error("Error fetching student profile:", error);
  }
};

// New function to fetch courses from dashboard API
const fetchStudentDashboard = async () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      console.error("No access token found");
      return;
    }

    const response = await axios.get("http://localhost:5000/student_dashboard", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    // Update enrolled courses with data from API
    enrolledCourses.value = response.data.courses_data;
  } catch (error) {
    console.error("Error fetching student dashboard:", error);
  }
};

// Fetch data when component mounts
onMounted(() => {
  fetchStudentProfile();
  fetchStudentDashboard();
});
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
          <p class="email"><strong>Email:</strong> {{ student.email }}</p>
          <p class="username"><strong>Username:</strong> {{ student.username }}</p>
          <p class="role"><strong>Role:</strong> {{ student.role }}</p>
          <p class="last-login"><strong>Last Login:</strong> {{ student.last_login }}</p>
          <p class="degree-level"><strong>Degree: </strong> {{ student.degree }}</p>
          <p class="branch"><strong>Branch:</strong> {{ student.branch }}</p>
          <p class="college-name"><strong>College:</strong> {{ student.college }}</p>
        </div>
      </div>




      <!-- Courses section -->
      <div class="courses-section">
        <h3>Selected Courses</h3>
        <ul>
          <li v-for="course in enrolledCourses1" :key="course.course_name" class="course-item">
            <strong>{{ course.course_name }}</strong>
            <ul v-if="course.assignments.length">
              <li v-for="assignment in course.assignments" :key="assignment.week_number" class="assignment-item">
                <span><strong>Type:</strong> {{ assignment.assignment_type }}</span> |
                <span><strong>Week:</strong> {{ assignment.week_number }}</span> |
                <span><strong>Score:</strong> {{ assignment.score }}</span>
              </li>
            </ul>
            <p v-else class="no-assignments">No assignments available</p>
          </li>
        </ul>
      </div>

    </div>
  </div>
</template>

<style scoped>
.profile-page {
  font-family: 'Inter', Arial, sans-serif;
  background: linear-gradient(to right, #ff7e5f, #7b4397);
  padding: 50px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-container {
  width: 100%;
  max-width: 900px;
  background-color: #ffffff;
  padding: 30px;
  border-radius: 20px;
  /*box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);*/
  box-shadow: 0 10px 16px rgba(245, 103, 238, 0.68);

  transition: box-shadow 0.3s ease;
}

.profile-container:hover {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #e0e0e0;
}

.image-container {
  padding-bottom: 25px;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.profile-image {
  width: 100%;
  height: 320px;
  border-radius: 50%; /* Square with rounded corners */
  object-fit: cover;
  border: 2px solid #e0e0e0;
  box-shadow: 0 8px 16px rgba(195, 24, 247, 0.4);
  transition: transform 0.2s ease-in-out;
}

.profile-image:hover {
  transform: scale(1.05); /* Slight zoom on hover */
}


.student-details {
  text-align: left;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(195, 24, 247, 0.4);
  border: 1px solid #e0e0e0;
}

.student-details h2 {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  border-bottom: 2px solid #007bff;
  display: inline-block;
  padding-bottom: 4px;
}

.student-details p {
  font-size: 16px;
  color: #555;
  margin: 8px 0;
  line-height: 1.6;
  display: flex;
  align-items: center;
}

.student-details strong {
  font-weight: 500;
  color: #007bff;
  width: 150px; /* Aligns all labels vertically */
  display: inline-block;
}

.student-details span {
  flex-grow: 1;
}

.courses-section {
  margin-top: 30px;
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}


.courses-section:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.courses-section h3 {
  font-size: 24px;
  font-weight: 700;
  color: #6a11cb;
  margin-bottom: 16px;
  text-align: left;
  border-bottom: 2px solid #6a11cb;
  padding-bottom: 6px;
}

.courses-section ul {
  list-style: none;
  padding: 0;
}


.course-item {
  background: linear-gradient(to right, #f8f9fa, #e9ecef);
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  transition: background 0.3s ease;
}

.course-item:hover {
  background: linear-gradient(to right, #e9ecef, #d6d6d6);

}

.course-item strong {
  font-size: 18px;
  color: #343a40;
}

.courses-section li {
  background-color: #f8f9fa;
  padding: 12px 20px;
  margin-bottom: 10px;
  border-radius: 8px;
  font-size: 16px;
  color: #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.courses-section li:hover {
  background-color: #e9ecef;
}

.course-description {
  font-size: 14px;
  color: #777;
}


.assignment-item span {
  margin-right: 10px;
}

.no-assignments {
  font-size: 14px;
  color: #888;
  font-style: italic;
  padding-left: 5px;
}

@media (max-width: 768px) {
  .courses-section h3 {
    text-align: center;
  }

  .course-item {
    text-align: center;
  }
}
</style>
