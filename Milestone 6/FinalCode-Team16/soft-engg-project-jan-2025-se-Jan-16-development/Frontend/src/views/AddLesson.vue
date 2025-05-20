<template>
  <InstructorNavBar/>
  <div class="add-lesson-container">
    <h1>Add Supplementary Lesson</h1>

    <form @submit.prevent="saveLesson" class="lesson-form">
      <div class="form-group">
        <label for="title">Lesson Title</label>
        <input
            type="text"
            id="title"
            v-model="lesson.title"
            placeholder="Enter lesson title"
            required
        >
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
            id="description"
            v-model="lesson.description"
            placeholder="Enter lesson description"
            rows="4"
            required
        ></textarea>
      </div>

      <div class="form-group">
        <label for="content">Lesson Content</label>
        <textarea
            id="content"
            v-model="lesson.content"
            placeholder="Enter lesson content/notes"
            rows="10"
            required
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="category">Category</label>
          <select id="category" v-model="lesson.category" required>
            <option value="">Select a category</option>
            <option value="frontend">Frontend Development</option>
            <option value="backend">Backend Development</option>
            <option value="database">Database</option>
            <option value="devops">DevOps</option>
            <option value="mobile">Mobile Development</option>
            <option value="design">UI/UX Design</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div class="form-group">
          <label for="difficulty">Difficulty Level</label>
          <select id="difficulty" v-model="lesson.difficulty" required>
            <option value="">Select difficulty</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label for="resources">Additional Resources (Optional)</label>
        <textarea
            id="resources"
            v-model="lesson.resources"
            placeholder="Enter links to additional resources, one per line"
            rows="3"
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="button" @click="clearForm" class="cancel-button">Cancel</button>
        <button type="submit" class="save-button">Save Lesson</button>
      </div>
    </form>

    <div v-if="showSuccess" class="success-message">
      Lesson has been successfully added!
    </div>
  </div>
</template>

<script>
import InstructorNavBar from "@/components/Instructor/InstructorNavBar.vue";
export default {
  name: 'AddLesson',
  components: {
    InstructorNavBar
  },
  data() {
    return {
      lesson: {
        title: '',
        description: '',
        content: '',
        category: '',
        difficulty: '',
        resources: ''
      },
      showSuccess: false
    }
  },
  methods: {
    saveLesson() {
      // In a real app, this would call an API
      // For demo, we'll just show a success message
      console.log('Saving lesson:', this.lesson)

      // Show success message
      this.showSuccess = true
      setTimeout(() => {
        this.showSuccess = false
        this.clearForm()
      }, 3000)
    },
    clearForm() {
      this.lesson = {
        title: '',
        description: '',
        content: '',
        category: '',
        difficulty: '',
        resources: ''
      }
    }
  }
}
</script>

<style scoped>
.add-lesson-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.lesson-form {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input, textarea, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.cancel-button, .save-button {
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
  background-color: #3498db;
  color: white;
}

.save-button:hover {
  background-color: #2980b9;
}

.success-message {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #d4edda;
  color: #155724;
  border-radius: 4px;
  text-align: center;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>