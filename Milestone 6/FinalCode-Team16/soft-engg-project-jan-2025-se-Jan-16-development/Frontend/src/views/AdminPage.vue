<template>
  <AdminNavBar/>
  <div class="dashboard-container">
    <br>
    <label>Welcome, Admin</label>
    <br>
    <br>

    <div class="quick-actions">
      <h2>Quick Actions</h2>
      <div class="action-buttons">

        <button @click="setActiveComponent('AdminDetails')" class="action-button"> Admin Details</button>
        <button @click="setActiveComponent('StudentDetails')" class="action-button">Student Details</button>
        <button @click="setActiveComponent('CourseDetails')" class="action-button">Course Details</button>
        <button @click="setActiveComponent('TopQueries')" class="action-button">Top Queries</button>


        <button @click="setActiveComponent('AddCourse')" class="action-button">Add Course</button>

        <button @click="setActiveComponent('AddCourseMaterial')" class="action-button">Add Course Material</button>
        <button @click="setActiveComponent('EditCourseMaterial')" class="action-button">Edit Course Material</button>
        <button @click="setActiveComponent('AssignCourse')" class="action-button">Assign Course</button>
      </div>
    </div>

    <div class="dashboard-stats">
      <div v-if="activeComponent === 'AdminDetails'" class="stat-card">
        <h2>Admin Details</h2>
        <ul v-if="admindetails">
          <li><strong>Name:</strong> {{ admindetails.name }}</li>
          <li><strong>Email:</strong> {{ admindetails.email }}</li>
          <li><strong>Role:</strong> {{ admindetails.role }}</li>
        </ul>
        <p v-else>No queries found.</p>
      </div>

      <!-- Student Details -->
      <div v-if="activeComponent === 'StudentDetails'" class="stat-card">
        <h2>Student Details</h2>
        <div class="card-grid-wrapper">
          <div v-if="studentdetails.length" class="card-grid">
            <div v-for="student in studentdetails" :key="student.id" class="card-item">
              <strong>Name:</strong> {{ student.name }} <br/>
              <strong>Email:</strong> {{ student.email }} <br/>
              <strong>Total Courses:</strong> {{ student.total_courses }} <br/>
              <strong>Created At:</strong> {{ student.created_at }}
            </div>
          </div>
          <p v-else>No student details found.</p>
        </div>

      </div>

      <!-- Course Details -->
      <div v-if="activeComponent === 'CourseDetails'" class="stat-card">
        <h2>Course Details</h2>
        <div class="card-grid-wrapper">
          <div v-if="coursedetails.length" class="card-grid">
            <div v-for="course in coursedetails" :key="course.id" class="card-item">
              <strong>Course Name:</strong> {{ course.name }} <br/>
              <strong>Description:</strong> {{ course.description }} <br/>
              <strong>Total Assignments:</strong> {{ course.total_assignments }} <br/>
              <strong>Created At:</strong> {{ course.created_at }} <br/>
              <button @click="openEditModal(course)" class="action-button">
                Edit Course
              </button>
            </div>
          </div>
          <p v-else>No course details found.</p>
        </div>
      </div>

      <!-- Edit Course Modal -->
      <div v-if="isEditModalOpen" class="modal">
        <div class="modal-content">
          <h2>Edit Course</h2>
          <input v-model="selectedCourse.id" type="number" disabled/>
          <input v-model="selectedCourse.name" placeholder="New Name"/>
          <input v-model="selectedCourse.description" placeholder="New Description"/>
          <button @click="editCourse" class="save-button">Save Changes</button>
          <button @click="closeEditModal" class="close-button">Cancel</button>
        </div>
      </div>


      <!-- Top Queries -->
      <div v-if="activeComponent === 'TopQueries'" class="stat-card">
        <h2>Top Support Queries</h2>

        <div class="card-grid-wrapper">
          <div v-if="queries.length" class="card-grid">
            <div v-for="query in queries" :key="query.query" class="card-item">
              <strong>Query:</strong> {{ query.query_text }} <br/>
              <strong>Count:</strong> {{ query.count }} times
            </div>
          </div>
          <p v-else>No queries found.</p>
        </div>
      </div>

      <div v-if="activeComponent === 'AddCourse'" class="stat-card bg-white shadow-lg rounded-xl p-6 max-w-md mx-auto">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Add Course</h2>

        <div class="space-y-4">
          <!-- Course Name Input -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Course Name:</label>
            <input
                v-model="course.name"
                type="text"
                placeholder="Enter Course Name"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
          </div>

          <!-- Course Description Input -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Course Description:</label>
            <textarea
                v-model="course.description"
                placeholder="Enter Course Description"
                rows="3"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            ></textarea>
          </div>

          <!-- Add Course Button -->
          <button
              @click="addCourse"
              class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-lg transition duration-300"
          >
            Add Course
          </button>
        </div>
      </div>


      <div v-if="activeComponent === 'AddCourseMaterial'"
           class="stat-card bg-white shadow-lg rounded-xl p-6 max-w-md mx-auto">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Add Course Material</h2>

        <div class="space-y-4">
          <!-- Course Selection Dropdown -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Select Course:</label>
            <select
                v-model="courseId"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            >
              <option value="" disabled>Select a Course</option>
              <option v-for="course in coursedetails" :key="course.id" :value="course.id">
                {{ course.name }}
              </option>
            </select>
          </div>

          <!-- Week Number Input -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Week Number:</label>
            <input
                v-model="material.week_number"
                type="number"
                placeholder="Enter Week Number"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
          </div>

          <!-- Material Title Input -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Material Title:</label>
            <input
                v-model="material.title"
                type="text"
                placeholder="Enter Material Title"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
          </div>

          <!-- Material Link Input -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Material Link:</label>
            <input
                v-model="material.material_link"
                type="text"
                placeholder="Enter Material Link"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
          </div>

          <!-- Add Course Material Button -->
          <button
              @click="addCourseMaterial"
              class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-lg transition duration-300"
          >
            Add Material
          </button>
        </div>
      </div>


      <div v-if="activeComponent === 'EditCourseMaterial'" class="stat-card">
        <h2>Edit Course Material</h2>
        <input v-model="materialId" type="number" placeholder="Material ID"/>
        <input v-model="material.title" placeholder="New Title"/>
        <input v-model="material.link" placeholder="New Link"/>
        <button @click="editCourseMaterial">Edit</button>
      </div>

      <div v-if="activeComponent === 'AssignCourse'"
           class="stat-card bg-white shadow-lg rounded-xl p-6 max-w-md mx-auto">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4 text-center">Assign Course</h2>

        <div class="space-y-4">
          <!-- Course Selection -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Select Course:</label>
            <select
                v-model="selectedCourseId"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            >
              <option value="" disabled>Select Course</option>
              <option v-for="course in coursedetails" :key="course.id" :value="course.id">
                {{ course.name }}
              </option>
            </select>
          </div>

          <!-- Student Selection -->
          <div>
            <label class="block text-gray-600 font-medium mb-1">Select Student:</label>
            <select
                v-model="selectedStudentId"
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            >
              <option value="" disabled>Select Student</option>
              <option v-for="student in studentdetails" :key="student.id" :value="student.id">
                {{ student.name }}
              </option>
            </select>
          </div>

          <!-- Assign Button -->
          <button
              @click="assignCourse"
              class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-lg transition duration-300"
          >
            Assign Course
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import AdminNavBar from "@/components/Admin/AdminNavBar.vue";
import axios from "axios";

const activeComponent = ref("");
const isExpanded = ref(false);

const toggleSidebar = () => {
  isExpanded.value = !isExpanded.value;
};
const admindetails = ref(null);
const studentdetails = ref(null);
const coursedetails = ref(null);
const queries = ref([]);
const queryId = ref(null);
const queryDetails = ref("");
const solveMessage = ref("");
const course = ref({name: "", description: ""});
const courseId = ref(null);
const studentId = ref(null);
const material = ref({week_number: "", title: "", material_link: ""});
const materialId = ref(null);
const selectedCourseId = ref(null);
const selectedStudentId = ref(null);
const selectedCourse = ref({});
const isEditModalOpen = ref(false);

const setActiveComponent = (component) => {
  activeComponent.value = component;
  if (component === "TopQueries") fetchTopQueries();
  if (component == "AdminDetails") fetchAdminDetails();
  if (component === "StudentDetails") fetchStudentDetails();
  if (component === "CourseDetails") fetchCourseDetails();
  if (component === "AssignCourse") fetchStudentDetails();
  fetchCourseDetails();
};


const fetchStudentDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/admin_students", {
      headers: {Authorization: `Bearer ${token}`},
    });
    studentdetails.value = response.data.students || [];
    console.log(studentdetails);
  } catch (error) {
    console.error("Error fetching student details:", error);
  }
};

// Fetch Course Details
const fetchCourseDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/admin_courses", {
      headers: {Authorization: `Bearer ${token}`},
    });
    coursedetails.value = response.data.courses || [];
    console.log(coursedetails);
  } catch (error) {
    console.error("Error fetching course details:", error);
  }
};

const fetchAdminDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get("http://127.0.0.1:5000/admin_details", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    // console.log(response.data);
    admindetails.value = response.data; // Adjust according to API response structure
    // console.log(admindetails);
  } catch (error) {
    console.error("Error fetching admin details:", error);
  }
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

const fetchQueryDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get(`http://127.0.0.1:5000/query_detail/${queryId.value}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );
    queryDetails.value = response.data.details;
  } catch (error) {
    console.error("Error fetching query details:", error);
  }
};

const solveQuery = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.post(`http://127.0.0.1:5000/solve_query/${queryId.value}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );
    solveMessage.value = "Query marked as solved!";
  } catch (error) {
    console.error("Error solving query:", error);
  }
};

const addCourse = async () => {
  try {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Unauthorized: No access token found.");
      return;
    }

    const payload = {
      name: course.value.name?.toString().trim() || "",
      description: course.value.description?.toString().trim() || ""
    };

    console.log("Sending Payload:", payload); // Debugging step

    const response = await axios.post(
        "http://127.0.0.1:5000/add_course",
        payload,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );

    alert("Course added successfully!");
  } catch (error) {
    console.error("Error adding course:", error.response?.data || error);
    alert(error.response?.data?.message || "Failed to add course.");
  }
};

const openEditModal = (course) => {
  selectedCourse.value = {...course}; // Pre-fill modal with course data
  isEditModalOpen.value = true;
};

const closeEditModal = () => {
  isEditModalOpen.value = false;
};

const editCourse = async () => {
  try {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Unauthorized: No access token found.");
      return;
    }

    const response = await axios.put(
        `http://127.0.0.1:5000/edit_course/${selectedCourse.value.id}`,
        {
          name: selectedCourse.value.name,
          description: selectedCourse.value.description,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );

    alert("Course updated successfully!");
  } catch (error) {
    console.error("Error editing course:", error.response?.data || error);
    alert(error.response?.data?.message || "Failed to edit course.");
  }
};


const addCourseMaterial = async () => {
  if (!courseId.value || !material.value.week_number || !material.value.title || !material.value.material_link) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Unauthorized: No access token found.");
      return;
    }

    const response = await axios.post(
        `http://127.0.0.1:5000/add_course/${courseId.value}/material`,
        material.value,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );

    alert("Material added successfully!");

    // Reset input fields after successful submission
    material.value = {week_number: "", title: "", material_link: ""};
  } catch (error) {
    console.error("Error adding material:", error.response?.data || error);
    alert(error.response?.data?.message || "Failed to add material.");
  }
};


const editCourseMaterial = async () => {
  try {
    const token = localStorage.getItem("access_token");
    await axios.put(`http://127.0.0.1:5000/edit_course/material/${materialId.value}`, material.value,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );
    alert("Material updated successfully!");
  } catch (error) {
    console.error("Error editing material:", error);
  }
};

const assignCourse = async () => {
  if (!selectedCourseId.value || !selectedStudentId.value) {
    alert("Please select both a course and a student.");
    return;
  }

  try {
    const token = localStorage.getItem("access_token");
    await axios.post(
        `http://127.0.0.1:5000/assign-course/${selectedCourseId.value}/${selectedStudentId.value}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
    );
    alert("Course assigned successfully!");
  } catch (error) {
    console.error("Error assigning course:", error);
    alert("Failed to assign course. Please check permissions.");
  }

};

</script>


<style scoped>
/* Dashboard Container */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 500px;
  text-align: left;
  position: relative;
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

.save-button {
  margin-top: 10px;
  margin-right: 10px;
  background: #227c0b;
  border-radius: 15px;
  color: white;
  border: none;
  padding: 8px;
  cursor: pointer;
}

.close-button {
  margin-top: 10px;
  background: #d42c2c;
  border-radius: 15px;
  color: white;
  border: none;
  padding: 8px;
  cursor: pointer;
}

.dashboard-container {
  max-width: 1100px;
  margin: 0 auto;
  font-family: "Poppins", sans-serif;
  color: #333;
}

.dashboard-stats {
  display: grid;
  gap: 1rem;
  margin-bottom: 1rem;
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

label {
  color: rgb(102, 3, 97);
  font-size: 22px;
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
  border-right: 5px solid #c9325f;
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
  grid-template-columns: repeat(8, 1fr);
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
  max-width: 1200px;
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


</style>