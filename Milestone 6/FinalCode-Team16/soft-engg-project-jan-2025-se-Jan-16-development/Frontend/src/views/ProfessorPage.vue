<template>
  <ProfessorNavBar/>
  <div class="dashboard-container">
    <label>Welcome Professor</label>
    <br>
    <br>
    <div class="quick-actions">
      <h2>Quick Actions</h2>
      <div class="action-buttons">
      <button @click="setActiveComponent('ProfessorDetails')"   class="action-button">Professor Details</button>
      <button @click="setActiveComponent('CourseDetails')"  class="action-button">Course Details</button>
      <button @click="setActiveComponent('TopQueries')" class="action-button">Top Queries</button>
      <button @click="setActiveComponent('PendingInstructors')" class="action-button">Pending Instructors</button>
      
    </div>
  </div>
    
    
  <div class="dashboard-stats">
      <div v-if="activeComponent === 'ProfessorDetails'" class="stat-card">
        <h2>Professor Details</h2>
        <ul v-if="professordetails">
          <li><strong>Name:</strong> {{ professordetails.name }}</li>
          <li><strong>Email:</strong> {{ professordetails.email }}</li>
          <li><strong>Role:</strong> {{ professordetails.role }}</li>
        </ul>
        <p v-else>No queries found.</p>
      </div>

      <div v-if="activeComponent === 'TopQueries'" class="stat-card">
        <h2>Top Support Queries</h2>
        <div class="card-grid-wrapper">
          <div v-if="queries.length" class="card-grid">
          <div v-for="query in queries" :key="query.query" class="card-item">
            {{ query.query_text }} - {{ query.count }} times
          </div>
        </div>
        <p v-else>No queries found.</p>
      </div>
    </div>

       <!-- Course Details -->
    <div v-if="activeComponent === 'CourseDetails'" class="stat-card">
      <h2>Course Details</h2>
      <div class="card-grid-wrapper">
        <div v-if="coursedetails.length" class="card-grid">
        <div v-for="course in coursedetails" :key="course.id" class="card-item" >
          <strong>Course Name:</strong> {{ course.name }} <br />
          <strong>Description:</strong> {{ course.description }} <br />
          <strong>Total Assignments:</strong> {{ course.total_assignments }} <br />
          <strong>Created At:</strong> {{ course.created_at }}
          <button @click="openAddLessonModal(course.id)" class="action-button">Add Suplementary</button>
        </div>
      </div>
      <p v-else>No course details found.</p>
    </div>
    </div>

     <!-- Pending Instructors -->
     <div v-if="activeComponent === 'PendingInstructors'" class="stat-card">
        <h2>Pending Instructor Requests</h2>
        <div class="card-grid-wrapper">
        <div v-if="pendingInstructors.length" class="card-grid">
          <div v-for="request in pendingInstructors" :key="request.id" class="card-item">
            <strong>ID:</strong> {{ request.id }} <br />
            <strong>Instructor ID:</strong> {{ request.instructor_id }} <br />
            <strong>Instructor Name:</strong> {{ request.instructor_name }} <br />
            <strong>Status:</strong> {{ request.status }} <br />
  
            <strong>Created At:</strong> {{ request.created_at }} <br />
            <button 
  @click="approveInstructor(request.id, 'Approved')" 
  class="action-button"
  :style="{ backgroundColor: '#28a745', color: 'white' }"
>
  Approve
</button>

<button 
  @click="approveInstructor(request.id, 'Rejected')" 
  class="action-button"
  :style="{ backgroundColor: '#dc3545', color: 'white' }"
>
  Reject
</button>
          </div>
        </div>
        <p v-else>No pending instructor requests.</p>
      </div>
    </div>

    <div v-if="showAddLessonModal" class="modal-overlay">
    <div class="modal-content">
      <h2>Add Lesson</h2>
      <form @submit.prevent="addLesson">
        <label>Course ID:</label>
        <input v-model="lesson.course_id" type="text" readonly required />

        <label>Material Title:</label>
        <input v-model="lesson.material_type" type="text" required />

        <label>Content:</label>
        <textarea v-model="lesson.content" required></textarea>

        <div class="modal-actions">
          <button type="submit" class="modal-submit">Submit</button>
          <button type="button" class="modal-close" @click="closeAddLessonModal">Cancel</button>

        </div>
      </form>
    </div>
  </div>



    </div>
</div>
</template>

<script setup>
import { ref } from "vue";
import ProfessorNavBar from "@/components/Professor/ProfessorNavBar.vue";
import axios from "axios";

const activeComponent = ref("");
const professordetails = ref("");
const coursedetails = ref(null);
const queries = ref([]);
const pendingInstructors = ref([]);
const showAddLessonModal = ref(false);
const lesson = ref({ course_id: "", material_type: "", content: "" });

const openAddLessonModal = (courseId) => {
  lesson.value.course_id = courseId;
  showAddLessonModal.value = true;
  document.body.classList.add("modal-open"); // Prevents background scroll
};


const closeAddLessonModal = () => {
  showAddLessonModal.value = false;
  document.body.classList.remove("modal-open");
};

const setActiveComponent = (component, courseId = null) => {
  activeComponent.value = component;

  // If navigating to "AddLesson", store the selected course ID
  if (component === "AddLesson" && courseId) {
    lesson.value.course_id = courseId;
  }

  if (component === "TopQueries") fetchTopQueries();
  if (component === "ProfessorDetails") fetchProfessorDetails();
  if (component === "CourseDetails") fetchCourseDetails();
  if (component === "PendingInstructors") fetchPendingInstructors();
};


const fetchTopQueries = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/topquery",
    {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    queries.value = response.data;
  } catch (error) {
    console.error("Error fetching queries:", error);
  }
};

const fetchCourseDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/admin_courses", {
      headers: { Authorization: `Bearer ${token}` },
    });
    coursedetails.value = response.data.courses || [];
    console.log(coursedetails);
  } catch (error) {
    console.error("Error fetching course details:", error);
  }
};

const fetchProfessorDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/professor_details", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    // console.log(response.data);
    professordetails.value = response.data; // Adjust according to API response structure
    // console.log(professordetails);
  } catch (error) {
    console.error("Error fetching admin details:", error);
  }
};

const fetchPendingInstructors = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/pending_instructor", {
      headers: { Authorization: `Bearer ${token}` },
    });
    pendingInstructors.value = response.data;
    console.log(response.data);
  } catch (error) {
    console.error("Error fetching pending instructors:", error);
  }
};

const approveInstructor = async (requestId, status) => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.put(`http://127.0.0.1:5000/approve_instructor/${requestId}`, 
      { status: status },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    console.log(response.data);
    fetchPendingInstructors(); // Refresh the list after approval/rejection
  } catch (error) {
    console.error(`Error approving instructor (${status}):`, error);
  }
};

const addLesson = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.post("http://127.0.0.1:5000/add_suplementary", lesson.value, {
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log(response.data);
    alert("Lesson added successfully!");
    showAddLessonModal.value = false; // Close modal after submission
  } catch (error) {
    console.error("Error adding lesson:", error);
  }
};


</script>

<style scoped>
/* Dashboard Container */
.dashboard-container {
  padding: 2rem;
  max-width: 1100px;
  margin: 0 auto;
  font-family: "Poppins", sans-serif;
  color: #333;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0;
  color: #3498db;
}

label{
  color:rgb(102, 3, 97);
  font-size:22px;
  font-weight: bold;
}

/* Sections */
.top-queries-section,
.quick-actions {
  background: #ffffff;
  border-radius: 14px;
  padding: 2rem;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  border-left: 5px solid #9b32c9; /* Accent Border */
  transition: all 0.3s ease-in-out;
}

.top-queries-section:hover,
.quick-actions:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.query-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.query-card {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1rem;
  transition: transform 0.2s;
}

.query-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.query-meta {
  display: flex;
  justify-content: space-between;
  margin: 1rem 0;
  font-size: 0.9rem;
  color: #666;
}

.status-pending {
  color: #e67e22;
}

.status-resolved {
  color: #27ae60;
}

.view-button {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.view-button:hover {
  background-color: #2980b9;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
 }
 
 
 .action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to right, #ff7e5f, #9b32c9);
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
 
 


@media (max-width: 768px) {
  .dashboard-stats, .action-buttons {
    grid-template-columns: 1fr;
  }
}
.card-grid-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  overflow: hidden; /* Prevents horizontal scrolling */
  padding: 1rem; /* Ensures proper spacing */
}

.card-grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  max-width: 1000px;
  width: 100%;
}

.card-item {
  background-color: white;
  border: 1px solid #ddd; /* Light grey border */
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: left;
  transition: transform 0.2s ease-in-out; /* Smooth hover effect */
}

.card-item:hover {
  transform: scale(1.05);
}

/* Ensure container has correct width */
.student-container {
  width: 100%;
  max-width: 1200px;
  margin: auto;
  padding: 1rem;
}
/* Global heading styles */
h1 {
  font-size: 2rem; /* Adjust size */
  font-weight: bold;
  color: #222;
  text-align: center;
  margin-bottom: 1rem;
}

h2 {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.75rem;
}

h3 {
  font-size: 1.3rem;
  font-weight: bold;
  color: #444;
  margin-bottom: 0.5rem;
}

/* Action button inside cards */
.card-item .action-button {
  width: 100%; /* Makes it full-width inside the card */
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.75rem;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease-in-out, transform 0.2s ease-in-out;
  text-align: center;
  margin-top: 1rem; /* Adds spacing from the text above */
  display: block; /* Ensures button spans full width inside the card */
}

/* Hover effect */
.card-item .action-button:hover {
  background-color: #0056b3;
  transform: scale(1.03);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensures modal is above everything */
}

.modal-content {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 500px; /* More responsive */
  text-align: left;
  position: relative; /* Ensures proper alignment */
  animation: fadeIn 0.3s ease-in-out;
}

.modal-content h2 {
  text-align: center;
  margin-bottom: 1rem;
}

.modal-content form {
  display: flex;
  flex-direction: column;
}

.modal-content label {
  font-weight: bold;
  margin-top: 0.5rem;
}

.modal-content input,
.modal-content textarea {
  width: 100%;
  padding: 0.75rem;
  margin-top: 0.3rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.modal-submit {
  background: #28a745;
  color: white;
  padding: 10px 16px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1rem;
  transition: background 0.3s ease-in-out;
}

.modal-submit:hover {
  background: #218838;
}

.modal-close {
  background: #dc3545;
  color: white;
  padding: 10px 16px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1rem;
  transition: background 0.3s ease-in-out;
}

.modal-close:hover {
  background: #c82333;
}

/* Prevent background scrolling when modal is open */
body.modal-open {
  overflow: hidden;
}

/* Fade-in animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}


</style>