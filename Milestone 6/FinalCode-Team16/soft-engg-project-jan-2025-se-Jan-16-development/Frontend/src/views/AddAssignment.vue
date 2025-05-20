<template>
  <InstructorNavBar />
  <div class="add-assignment-container">
    <div class="add-assignment-form">
      <label>Add Assignment</label>
      <br />

      <form @submit.prevent="submitAssignment" class="assignment-form">
        <!-- Course Dropdown -->
        <div class="form-group">
          <label for="courseId">Select Course</label>
          <select id="courseId" v-model="selectedCourseId" required>
            <option value="" disabled>Select a course</option>
            <option v-for="course in courses" :key="course.id" :value="course.id">
              {{ course.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="weekNumber">Week Number</label>
          <input
            type="number"
            id="weekNumber"
            v-model.number="assignment.week_number"
            placeholder="Enter Week Number"
            min="1"
            required
          />
        </div>

        <div class="form-group">
          <label for="assignmentType">Assignment Type</label>
          <select id="assignmentType" v-model="assignment.assignment_type" required>
            <option value="Assignment">Assignment</option>
            <option value="Programming Assignment">Programming Assignment</option>
          </select>
        </div>

        <div class="form-group">
          <label for="fileUpload">Upload File</label>
          <input type="file" id="fileUpload" @change="handleFileUpload" required />
        </div>

        <div class="form-actions">
          <button type="button" @click="clearForm" class="cancel-button">Cancel</button>
          <button type="submit" class="save-button" :disabled="isSubmitting">
            {{ isSubmitting ? "Submitting..." : "Submit Assignment" }}
          </button>
        </div>
      </form>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import InstructorNavBar from "@/components/Instructor/InstructorNavBar.vue";

export default {
  name: "AddAssignment",
  components: {
    InstructorNavBar,
  },
  setup() {
    const courses = ref([]);
    const selectedCourseId = ref("");
    const assignment = ref({
      week_number: null,
      assignment_type: "Assignment",
      file: null,
    });
    const isSubmitting = ref(false);
    const errorMessage = ref("");

    // Fetch courses from API
    const fetchCourses = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://127.0.0.1:5000/courses", {
          headers: { Authorization: `Bearer ${token}` },
        });
        courses.value = response.data;
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    };

    // Handle file upload
    const handleFileUpload = (event) => {
      assignment.value.file = event.target.files[0];
    };

    // Submit assignment
    const submitAssignment = async () => {
      errorMessage.value = "";

      if (!selectedCourseId.value || !assignment.value.week_number || !assignment.value.file) {
        errorMessage.value = "Please fill in all fields.";
        return;
      }

      

      isSubmitting.value = true;
      const token = localStorage.getItem("access_token");
      try {
        const formData = new FormData();
        formData.append("course_id", selectedCourseId.value);
        formData.append("week_number", assignment.value.week_number);
        formData.append("assignment_type", assignment.value.assignment_type);
        formData.append("file", assignment.value.file);

        await axios.post("http://127.0.0.1:5000/add_assigments", formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        });

        alert("Assignment added successfully!");
        clearForm();
      } catch (error) {
        console.error("Failed to add assignment:", error);
        errorMessage.value = error.response?.data?.message || "Failed to add assignment.";
      } finally {
        isSubmitting.value = false;
      }
    };

    // Clear form
    const clearForm = () => {
      selectedCourseId.value = "";
      assignment.value = { week_number: null, assignment_type: "Assignment", file: null };
      errorMessage.value = "";
    };

    onMounted(fetchCourses);

    return {
      courses,
      selectedCourseId,
      assignment,
      isSubmitting,
      errorMessage,
      handleFileUpload,
      submitAssignment,
      clearForm,
    };
  },
};
</script>

<style scoped>
.add-assignment-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.add-assignment-form {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.cancel-button,
.save-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-button {
  background-color: #f1f1f1;
  color: #333;
}

.cancel-button:hover {
  background-color: #e1e1e1;
}

.save-button {
  background: linear-gradient(to right, #ff7e5f, #7b4397);
  color: white;
}

.save-button:hover {
  opacity: 0.9;
}

.save-button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8d7da;
  color: #721c24;
  border-radius: 4px;
  text-align: center;
}

@media (max-width: 768px) {
  .form-group {
    grid-template-columns: 1fr;
  }
}
</style>
