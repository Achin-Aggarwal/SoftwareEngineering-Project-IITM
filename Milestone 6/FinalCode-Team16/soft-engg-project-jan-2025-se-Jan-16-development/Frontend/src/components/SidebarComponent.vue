<template>
  <div class="sidebar">
    <div class="sidebar-content">
      <!-- Mobile Menu Toggle -->
      <div class="mobile-menu-toggle" @click="toggleMobileMenu">
        <span></span>
        <span></span>
        <span></span>
      </div>

      <!-- Sidebar/Lecture List -->
      <div class="lecture-list" :class="{ 'mobile-active': mobileMenuActive }">
        <div class="mobile-close" @click="toggleMobileMenu">&times;</div>
 
 
        <div v-if="loading" class="loading">Loading course...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="selectedCourse">
          <h1>{{ selectedCourse.name }}</h1>
 
 
          <!-- Weekly Materials -->
          <div>
            <ul v-if="organizedWeeks.length > 0">
              <li v-for="(week, index) in organizedWeeks" :key="index">
                <h3 @click="toggleWeek(index)">
                  Week {{ week.weekNumber }}
                  <span>{{ expandedWeek === index ? '▲' : '▼' }}</span>
                </h3>
                <ul v-show="expandedWeek === index">
                  <!-- Lectures -->
                  <li v-if="week.materials.length === 0" class="no-content">No materials available for this week</li>
                  <li
                      v-for="(material, idx) in week.materials"
                      :key="idx"
                      @click="selectContent(material.video_link, null, idx, index)"
                      :class="{ 'selected': selectedLecture === idx && currentWeek === index && !viewingSupplementary && !viewingLiveSession && !viewingPythonCompiler && !viewingAssignment && !viewingProgrammingAssignment }"
                  >
                    <span
                        v-if="selectedLecture === idx && currentWeek === index && !viewingSupplementary && !viewingLiveSession && !viewingPythonCompiler && !viewingAssignment && !viewingProgrammingAssignment"
                        class="dot"></span>
                    {{ material.title }}
                  </li>
 
 
                  <!-- Week Assignments -->
                  <li
                      v-for="(assignment, assignmentIdx) in week.assignments"
                      :key="`assignment-${assignmentIdx}`"
                      @click="selectAssignment(assignment, assignmentIdx, index)"
                      :class="{
                      'selected':
                        selectedAssignmentIndex === assignmentIdx &&
                        viewingAssignment &&
                        currentWeek === index
                    }"
                  >
                    <span
                        v-if="
                        selectedAssignmentIndex === assignmentIdx &&
                        viewingAssignment &&
                        currentWeek === index
                      "
                        class="dot"
                    ></span>
                    {{ assignment.name }} {{ assignment.weekNumber }}
                  </li>
 
 
                  <!-- Programming Assignments -->
                  <li
                      v-for="(programmingAssignment, progIndex) in week.programming_assignments"
                      :key="`prog-assignment-${progIndex}`"
                      @click="selectProgrammingAssignment(programmingAssignment, progIndex, index)"
                      :class="{
                      'selected':
                        selectedProgrammingAssignmentIndex === progIndex &&
                        viewingProgrammingAssignment &&
                        currentWeek === index
                    }"
                  >
                    <span
                        v-if="
                        selectedProgrammingAssignmentIndex === progIndex &&
                        viewingProgrammingAssignment &&
                        currentWeek === index
                      "
                        class="dot"
                    ></span>
                    {{ programmingAssignment.name }} {{ programmingAssignment.weekNumber }}
                  </li>
                </ul>
              </li>
            </ul>
            <div v-else class="no-data">No weekly content available for this course.</div>
 
 
            <!-- Supplementary Content -->
            <br>
            <h3 @click="toggleSupplementary">
              Supplementary Content
              <span>{{ showSupplementary ? '▲' : '▼' }}</span>
            </h3>
            <ul v-show="showSupplementary">
              <li v-if="!selectedCourse.supplementary_materials || selectedCourse.supplementary_materials.length === 0"
                  class="no-content">
                No supplementary content available for this course
              </li>
              <li
                  v-else
                  v-for="(material, idx) in selectedCourse.supplementary_materials"
                  :key="idx"
                  @click="selectSupplementaryContent(material.content, idx); toggleMobileMenuIfActive();"
                  :class="{ 'selected': selectedSupplementary === idx && viewingSupplementary }"
              >
                <span v-if="selectedSupplementary === idx && viewingSupplementary" class="dot"></span>
                {{ material.material_type }}
              </li>
            </ul>
 
 
            <!-- Live Sessions Section (New) -->
            <br>
            <h3 @click="toggleLiveSessions">
              Live Sessions
              <span>{{ showLiveSessions ? '▲' : '▼' }}</span>
            </h3>
            <ul v-show="showLiveSessions">
              <li v-if="!allLiveSessions || allLiveSessions.length === 0"
                  class="no-content">
                No live sessions available for this course
              </li>
              <li
                  v-else
                  v-for="(session, idx) in allLiveSessions"
                  :key="idx"
                  @click="selectLiveSession(session.yt_link, idx); toggleMobileMenuIfActive();"
                  :class="{ 'selected': selectedLiveSession === idx && viewingLiveSession }"
              >
                <span v-if="selectedLiveSession === idx && viewingLiveSession" class="dot"></span>
                {{ session.description }}
              </li>
            </ul>
 
 
            <!-- Python IDE Section -->
            <br>
            <h3
                @click="selectPythonCompiler"
                class="python-compiler-button flex items-center"
                :class="{ 'selected': viewingPythonCompiler }"
            >
              <span
                  v-if="viewingPythonCompiler"
                  class="h-2 w-2 bg-green-500 rounded-full inline-block"
              ></span>
              Python Compiler
              <span
                  v-if="viewingPythonCompiler"
                  class="h-2 w-2 bg-green-500 rounded-full inline-block"
              ></span>
            </h3>
          </div>
        </div>
      </div>
    </div>
  </div>
 
 
  <!-- Content Area -->
  <div class="content-area">
    <!-- Error Messages -->
    <div class="content-error" v-if="contentError">
      <h3>{{ contentError }}</h3>
      <p>Please select another item or contact support if this issue persists.</p>
    </div>
 
 
    <!-- Video Player -->
    <div class="video-player" v-else-if="selectedVideoUrl && !viewingSupplementary && !viewingLiveSession && !viewingPythonCompiler && !viewingAssignment && !viewingProgrammingAssignment">
      <VideoPlayerComponent :videoSrc="selectedVideoUrl" @error="handleContentError"/>
    </div>
 
 
    <!-- PDF Viewer -->
    <div class="pdf-viewer" v-else-if="selectedPdfUrl && viewingSupplementary">
      <PDFViewerComponent :pdfSrc="selectedPdfUrl" @error="handleContentError"/>
    </div>
 
 
    <!-- Live Session Video Player -->
    <div class="video-player" v-else-if="selectedVideoUrl && viewingLiveSession">
      <h2 class="live-session-title">Live Session: {{ currentLiveSessionTitle }}</h2>
      <VideoPlayerComponent :videoSrc="selectedVideoUrl" @error="handleContentError"/>
    </div>
 
 
    <!-- Python Compiler -->
    <div class="python-compiler" v-else-if="viewingPythonCompiler">
      <iframe
          src="https://trinket.io/embed/python3/a5bd54189b"
          width="100%"
          height="800"
          allowfullscreen
      ></iframe>
    </div>
 
 
    <!-- MCQ Assignment Viewer -->
    <div v-else-if="viewingAssignment" class="assignment-container">
      <div class="assignment-header">
        <h2>{{ currentAssignment.name }}</h2>
        <h2 style="color: red">Due on 2025-04-13, 23:59 IST.</h2>
        <p>Total Questions: {{ currentAssignment.questions.length }}</p>
      </div>
 
 
      <div class="assignment-questions">
        <div
            v-for="(question, qIndex) in currentAssignment.questions"
            :key="qIndex"
            class="mcq-question"
        >
          <h3>{{ question.text }}</h3>
          <div class="mcq-options">
            <label
                v-for="(option, optIndex) in question.options"
                :key="optIndex"
                class="mcq-option"
            >
              <input
                  type="radio"
                  :name="`question-${qIndex}`"
                  :value="option.text"
                  v-model="userAnswers[qIndex]"
              />
              {{ option.text }}
            </label>
          </div>
        </div>
      </div>
 
 
      <div class="assignment-actions">
        <button
            @click="submitAssignment"
            class="submit-btn"
        >
          Submit Assignment
        </button>
      </div>
 
 
      <!-- Results Section -->
      <div v-if="showResults" class="assignment-results">
        <h3>Assignment Results</h3>
        <p>Correct Answers: {{ correctAnswers }} / {{ currentAssignment.questions.length }}</p>
        <p>Score: {{ scorePercentage }}%</p>
        <div class="detailed-results">
          <h4>Detailed Breakdown</h4>
          <ul>
            <li
                v-for="(question, qIndex) in currentAssignment.questions"
                :key="qIndex"
                :class="{
                'correct-answer': userAnswers[qIndex] === question.correctAnswer,
                'incorrect-answer': userAnswers[qIndex] !== question.correctAnswer
              }"
            >
              <strong>Q{{ qIndex + 1 }}:</strong>
              {{ userAnswers[qIndex] === question.correctAnswer ? '✓' : '✗' }}
              Correct Answer: {{ question.correctAnswer }}
            </li>
          </ul>
        </div>
      </div>
    </div>
 
 
    <!-- Programming Assignment Viewer -->
    <div v-else-if="viewingProgrammingAssignment" class="programming-assignment-container">
      <div class="assignment-header">
        <h2>{{ currentProgrammingAssignment.name }}</h2>
        <h2 style="color: red">Due on 2025-04-13, 23:59 IST.</h2>
      </div>
 
 
      <div class="coding-area">
        <div class="problem-statement">
          <h3>Problem Statement</h3>
          <div v-for="(task, index) in currentProgrammingAssignment.tasks" :key="index">
            <h4>Task {{ index + 1 }}</h4>
            <p>{{ task.problemStatement }}</p>
            <p><strong>Example Input:</strong> {{ task.exampleInput }}</p>
            <p><strong>Expected Output:</strong> {{ task.expectedOutput }}</p>
          </div>
        </div>
 
 
        <div class="ide-container">
          <div class="code-editor">
            <textarea
                v-model="userCode"
                placeholder="Write your Python code here..."
                rows="15"
                class="w-full p-2 border rounded"
            ></textarea>
          </div>
 
 
          <div class="ide-actions">
            <button
                @click="runCode"
                class="run-btn bg-blue-500 text-white p-2 rounded mr-2"
            >
              Run Code
            </button>
            <button
                @click="submitCode"
                class="submit-btn bg-green-500 text-white p-2 rounded"
            >
              Submit
            </button>
            <button class="chat-button-small" @click="toggleChat">
              💬 Programming Assistant
            </button>
          </div>
          
          <div v-if="chatVisible">
            <ChatBoxComponent @close="toggleChat" />
          </div>

          <div v-if="codeOutput" class="output-area">
            <h4>Output:</h4>
            <pre>{{ codeOutput }}</pre>
          </div>
 
 
          <div v-if="submissionResult" class="submission-result">
            <h4>Submission Result:</h4>
            <p :class="{
              'text-green-600': submissionResult.correct,
              'text-red-600': !submissionResult.correct
            }">
              {{ submissionResult.message }}
            </p>
          </div>
        </div>
      </div>
    </div>
 
 
    <!-- Default Page -->
    <div class="default-page" v-else>
      <div class="welcome-container">
        <h3>Welcome to {{ selectedCourse ? selectedCourse.name : 'Course' }}</h3>
        <p v-if="selectedCourse">Select a lecture, live session, supplementary content, assignments, or Python Compiler to start learning!</p>
      </div>
    </div>
  </div>
 </template>
 
 
 <script>
 import VideoPlayerComponent from './VideoPlayerComponent.vue';
 import PDFViewerComponent from './PDFViewerComponent.vue';
 import ChatBoxComponent from "./ChatBoxComponent.vue";
 import axios from 'axios';
 
 
 export default {
  components: {
    VideoPlayerComponent,
    PDFViewerComponent,
    ChatBoxComponent,
  },
  data() {
    return {
      chatVisible: false,
      loading: true,
      error: null,
      contentError: null,
      selectedCourse: null,
      expandedWeek: null,
      selectedVideoUrl: null,
      selectedPdfUrl: null,
      selectedLecture: null,
      selectedSupplementary: null,
      currentWeek: null,
      showSupplementary: false,
      viewingSupplementary: false,
      // New live sessions related properties
      showLiveSessions: false,
      viewingLiveSession: false,
      selectedLiveSession: null,
      currentLiveSessionTitle: "",
      allLiveSessions: [],
      // Existing properties
      mobileMenuActive: false,
      showPythonIDE: false,
      viewingPythonCompiler: false,
      selectedAssignmentIndex: null,
      viewingAssignment: false,
      currentAssignment: null,
      userAnswers: [],
      showResults: false,
      correctAnswers: 0,
      selectedProgrammingAssignmentIndex: null,
      viewingProgrammingAssignment: false,
      currentProgrammingAssignment: null,
      userCode: "",
      codeOutput: "",
      isRunning: false,
      submissionResult: null
    };
  },
  computed: {
    organizedWeeks() {
      if (!this.selectedCourse) return [];
      const materials = this.selectedCourse.materials || [];
      const assignments  = this.selectedCourse.assignments || [] ;
      const programming_assignments = this.selectedCourse.programming_assignments_data || [];
      const weekNumbers = [...new Set(materials.map(m => m.week_number))].sort((a, b) => a - b);
      return weekNumbers.map(weekNumber => {
        return {
          weekNumber,
          materials: materials.filter(m => m.week_number === weekNumber),
          assignments: assignments.filter(m => m.weekNumber === weekNumber ),
          programming_assignments: programming_assignments.filter(m => m.weekNumber === weekNumber)
        };
      });
    }
  },
  created() {
    this.fetchCourseDetails();
  },
  methods: {
    toggleChat() {
      this.chatVisible = !this.chatVisible;
    },
    
    async fetchCourseDetails() {
      try {
        this.loading = true;
        this.error = null;
        const courseId = this.$route.params.id;
        const token = localStorage.getItem("access_token");
        if (!token) {
          this.error = "No access token found. Please log in again.";
          this.loading = false;
          return;
        }
        const headers = { Authorization: `Bearer ${token}` };
        const response = await axios.get(`http://localhost:5000/course/${courseId}`, { headers });
        if (response.data && response.data.course_data) {
          this.selectedCourse = response.data.course_data;
          // Store all live sessions in a separate array
          this.allLiveSessions = this.selectedCourse.live_sessions || [];
          console.log("Course Data:", this.selectedCourse);
        } else {
          throw new Error('Invalid course data format');
        }
        this.loading = false;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.error = 'Your session has expired. Please log in again.';
          this.$router.push('/login');
        } else {
          this.error = 'Failed to load course details. Please try again later.';
        }
        this.loading = false;
        console.error('Error fetching course details:', error);
      }
    },
    toggleWeek(index) {
      // If clicking the already expanded week, close it
      if (this.expandedWeek === index) {
        this.expandedWeek = null;
      } else {
        // Otherwise, open the clicked week and close other sections
        this.expandedWeek = index;
        this.showSupplementary = false;
        this.showLiveSessions = false;
        this.showPythonIDE = false;
      }
    },
    toggleSupplementary() {
      // Toggle supplementary and close any open week and live sessions
      this.showSupplementary = !this.showSupplementary;
      if (this.showSupplementary) {
        this.expandedWeek = null;
        this.showLiveSessions = false;
        this.showPythonIDE = false;
      }
    },
    // New method to toggle live sessions section
    toggleLiveSessions() {
      this.showLiveSessions = !this.showLiveSessions;
      if (this.showLiveSessions) {
        this.expandedWeek = null;
        this.showSupplementary = false;
        this.showPythonIDE = false;
      }
    },
    toggleMobileMenu() {
      this.mobileMenuActive = !this.mobileMenuActive;
    },
    toggleMobileMenuIfActive() {
      // Close menu on selection for mobile devices
      if (window.innerWidth <= 768 && this.mobileMenuActive) {
        this.mobileMenuActive = false;
      }
    },
    selectContent(videoUrl, pdfUrl, idx, weekIndex) {
      // Clear any previous errors
      this.contentError = null;
 
 
      // Check if videoUrl is valid
      if (!videoUrl) {
        this.contentError = "Video content is unavailable";
        this.selectedVideoUrl = null;
      } else {
        this.selectedVideoUrl = videoUrl;
      }
 
 
      this.selectedPdfUrl = null;
      this.selectedLecture = idx;
      this.currentWeek = weekIndex;
      this.viewingSupplementary = false;
      this.viewingLiveSession = false;
      this.viewingPythonCompiler = false;
      this.viewingAssignment = false;
      this.viewingProgrammingAssignment = false;
      this.selectedAssignmentIndex = null; // Reset assignment selection
      this.selectedProgrammingAssignmentIndex = null; // Reset programming assignment selection
      this.toggleMobileMenuIfActive();
    },
    selectSupplementaryContent(content, idx) {
        // Clear any previous errors
        this.contentError = null;

        if (!content) {
          this.contentError = "Supplementary content is unavailable";
          this.selectedPdfUrl = null;
        } else {
          // Check if the content is a Google Drive link
          if (content.includes("drive.google.com")) {
            const fileIdMatch = content.match(/[-\w]{25,}/); // Extract file ID
            if (fileIdMatch) {
              const fileId = fileIdMatch[0];
              this.selectedPdfUrl = `https://drive.google.com/file/d/${fileId}/preview`;
            } else {
              this.contentError = "Invalid Google Drive link";
              this.selectedPdfUrl = null;
            }
          } else {
            this.selectedPdfUrl = content; // Use regular URL if not from Google Drive
          }
        }

        // Reset other views
        this.selectedVideoUrl = null;
        this.selectedSupplementary = idx;
        this.viewingSupplementary = true;
        this.viewingPythonCompiler = false;
        this.viewingAssignment = false;
        this.viewingProgrammingAssignment = false;

        this.toggleMobileMenuIfActive();
      },
    // New method to select live session
    selectLiveSession(videoUrl, idx) {
      // Clear any previous errors
      this.contentError = null;
 
 
      // Check if videoUrl is valid
      if (!videoUrl) {
        this.contentError = "Live session video is unavailable";
        this.selectedVideoUrl = null;
      } else {
        this.selectedVideoUrl = videoUrl;
        this.currentLiveSessionTitle = this.allLiveSessions[idx].description || "Live Session";
      }
 
 
      this.selectedPdfUrl = null;
      this.selectedLiveSession = idx;
      this.viewingLiveSession = true;
      this.viewingSupplementary = false;
      this.viewingPythonCompiler = false;
      this.viewingAssignment = false;
      this.viewingProgrammingAssignment = false;
      this.selectedLecture = null; // Reset lecture selection
      this.selectedAssignmentIndex = null; // Reset assignment selection
      this.selectedProgrammingAssignmentIndex = null; // Reset programming assignment selection
      this.toggleMobileMenuIfActive();
    },
    selectPythonCompiler() {
      // Clear any previous errors
      this.contentError = null;
 
 
      // Reset other views
      this.selectedVideoUrl = null;
      this.selectedPdfUrl = null;
      this.selectedLecture = null;
      this.selectedSupplementary = null;
      this.selectedLiveSession = null;
      this.viewingSupplementary = false;
      this.viewingLiveSession = false;
      this.viewingPythonCompiler = true;
      this.viewingAssignment = false;
      this.viewingProgrammingAssignment = false;
      this.selectedAssignmentIndex = null; // Reset assignment selection
      this.selectedProgrammingAssignmentIndex = null; // Reset programming assignment selection
      this.toggleMobileMenuIfActive();
    },
    selectAssignment(assignment, index, weekNumber) {
      this.currentAssignment = assignment;
      this.selectedAssignmentIndex = index;
      this.currentWeek = weekNumber;
      this.viewingAssignment = true;
      this.viewingSupplementary = false;
      this.viewingLiveSession = false;
      this.viewingPythonCompiler = false;
      this.viewingProgrammingAssignment = false;
      this.selectedVideoUrl = null;
      this.selectedPdfUrl = null;
      this.selectedLecture = null; // Reset the lecture selection
      this.selectedProgrammingAssignmentIndex = null; // Reset programming assignment selection
 
 
      // Reset assignment state
      this.userAnswers = new Array(assignment.questions.length).fill(null);
      this.showResults = false;
      this.correctAnswers = 0;
      this.toggleMobileMenuIfActive();
    },
    selectProgrammingAssignment(assignment, index, weekNumber) {
      this.currentProgrammingAssignment = assignment;
      this.selectedProgrammingAssignmentIndex = index;
      this.currentWeek = weekNumber;
      this.viewingProgrammingAssignment = true;
 
 
      // Reset views
      this.viewingSupplementary = false;
      this.viewingLiveSession = false;
      this.viewingPythonCompiler = false;
      this.viewingAssignment = false;
      this.selectedVideoUrl = null;
      this.selectedPdfUrl = null;
      this.selectedLecture = null; // Reset the lecture selection
      this.selectedAssignmentIndex = null; // Reset assignment selection
 
 
      // Set initial code to solution template
      this.userCode = assignment.solutionTemplate;
      this.codeOutput = '';
      this.submissionResult = null;
 
 
      this.toggleMobileMenuIfActive();
    },
    async submitAssignment() {
      // Check answers
      this.correctAnswers = this.currentAssignment.questions.reduce((count, question, index) => {
        return this.userAnswers[index] === question.correctAnswer ? count + 1 : count;
      }, 0);
 
 
      // Calculate Score Percentage
      this.scorePercentage = ((this.correctAnswers / this.currentAssignment.questions.length) * 100).toFixed(2);
 
 
      // Show Results
      this.showResults = true;
 
 
      // Get Assignment ID
      const assignment_id = this.currentAssignment.id;
      // Prepare Data for API
      const payload = {
        assignment_id: assignment_id,
        score: this.scorePercentage
      };
      const token = localStorage.getItem("access_token");
      try {
        const response = await fetch("http://127.0.0.1:5000/submit_score", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(payload)
        });
 
 
        const data = await response.json();
 
 
        if (data.success) {
          console.log("Score updated successfully:", data);
        } else {
          console.error("Failed to update score:", data.error);
        }
      } catch (error) {
        console.error("Error updating score:", error);
      }
    },
    async runCode() {
      this.isRunning = true;
      console.log("userCode:", this.userCode);
 
 
      if (!this.userCode) {
        this.codeOutput = "Please write some code before running.";
        return;
      }
 
 
      // Convert test cases into correct format
      const testCases = this.currentProgrammingAssignment.tasks.map(task => ({
        input: String(task.exampleInput),  // Ensure input is a string
        expected_output: String(task.expectedOutput) // Ensure expected output is a string
      }));
 
 
      console.log("Test Cases:", testCases); // Debugging log
 
 
      try {
        const response = await fetch("http://127.0.0.1:5000/run_code", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code: this.userCode, test_cases: testCases })
        });
 
 
        const data = await response.json();
        if (data.errors) {
          this.codeOutput = `Error: ${data.errors}`;
        } else if (data.test_results) {
          this.codeOutput = data.test_results;
        } else {
          this.codeOutput = "Unexpected response from server.";
        }
      } catch (error) {
        this.codeOutput = `Error: ${error.message}`;
      } finally {
        this.isRunning = false;
      }
    },
    async submitCode() {
      this.isRunning = true;
      console.log("Submitting code:", this.userCode);
 
 
      if (!this.userCode) {
        this.submissionResult = {
          correct: false,
          message: "Please write some code before submitting."
        };
        return;
      }
 
 
      // Format test cases correctly
      const testCases = this.currentProgrammingAssignment.tasks.map(task => ({
        input: String(task.exampleInput), // Ensure input is a string
        expected_output: String(task.expectedOutput) // Ensure expected output is a string
      }));
      const assignment_id = this.currentProgrammingAssignment.id;
      const token = localStorage.getItem("access_token");
      try {
        const response = await fetch("http://127.0.0.1:5000/submit_code", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify({ code: this.userCode, test_cases: testCases, assignment_id: assignment_id })
        });
 
 
        const data = await response.json();
 
 
        if (data.errors) {
          this.submissionResult = {
            correct: false,
            message: `Error: ${data.errors}`
          };
        } else if (data.test_results) {
          const allPassed = data.test_results.every(test => test.passed);
 
 
          this.submissionResult = {
            correct: allPassed,
            message: allPassed
                ? "Congratulations! All test cases passed."
                : "Some test cases failed. Please review your code."
          };
        } else {
          this.submissionResult = {
            correct: false,
            message: "Unexpected response from server."
          };
        }
      } catch (error) {
        this.submissionResult = {
          correct: false,
          message: `Error: ${error.message}`
        };
      } finally {
        this.isRunning = false;
      }
    },
    handleContentError(message) {
      this.contentError = message || "Content failed to load";
    }
  },
 };
 </script>
 
 
 
 
 <style scoped>
 
 
 .default-page {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: 70%;
 }
 
 
 .welcome-container {
  text-align: center;
 }
 
 
 .default-page h3 {
  color: #333;
  font-size: 28px;
  margin-bottom: 25px;
  padding-left: 35%;
 }
 
 
 .default-page p {
  font-size: 19px;
  color: #777;
 }
 
 
 * {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
 }
 
 
 h1 {
  text-align: center;
  font-family: 'Arial', sans-serif;
  font-size: 25px;
 }
 
 
 h2, h3 {
  font-family: 'Arial', sans-serif;
  color: #333;
  text-align: center;
 }
 
 
 h3 {
  transition: all 0.3s ease;
 }
 
 
 h3:hover {
  color: #2e8b57; /* Green color */
 }
 
 
 .sidebar {
  display: flex;
  width: 15%;
  height: 80%;
  background: #f4f6f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
 }
 
 
 .sidebar-content {
  display: flex;
  width: 100%;
  position: relative;
 }
 
 
 .nav-item {
  color: #1d1c1c;
  text-decoration: none;
  font-size: 1rem;
  padding: 8px 16px;
  border-radius: 4px;
  background-color: #ded4cf; /* Medium green */
  transition: background-color 0.3s;
  margin-left: 60px;
 }
 
 
 /* Mobile Menu Toggle */
 .mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
  cursor: pointer;
 }
 
 
 .mobile-menu-toggle span {
  display: block;
  height: 3px;
  width: 100%;
  background-color: #333;
  border-radius: 3px;
 }
 
 
 .mobile-close {
  display: none;
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  cursor: pointer;
  color: #333;
 }
 
 
 .lecture-list {
  width: 303px;
  height: 900px;
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
 }
 
 
 .content-area {
  flex-grow: 1;
  margin-left: 20px;
  display: flex;
 }
 
 
 ul {
  list-style: none;
  padding: 0;
 }
 
 
 li {
  cursor: pointer;
  padding: 10px;
  font-size: 16px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s ease;
  background-color: transparent;
 }
 
 
 li:hover {
  background-color: #f9f9f9; /* Light hover effect */
 }
 
 
 li.selected {
  background-color: #e3f9e5; /* Light green background when selected */
 }
 
 
 h3 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 8px;
  background-color: #f4f6f9;
 }
 
 
 h3 span {
  font-size: 18px;
  color: #007BFF;
 }
 
 
 .video-player, .pdf-viewer {
  flex-grow: 1;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
 }
 
 
 .video-player iframe, .pdf-viewer iframe {
  width: 100%;
  height: 100%;
  min-height: 400px;
  border-radius: 8px;
 }
 
 
 .dot {
  width: 8px;
  height: 8px;
  background-color: #28a745; /* Green dot */
  border-radius: 50%;
  margin-right: 10px;
  display: inline-block;
 }
 
 
 .default-page {
  flex-grow: 1;
  text-align: center;
  padding: 100px 30px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
 }
 
 
 .default-page h3 {
  color: #333;
  font-size: 24px;
 }
 
 
 .default-page p {
  font-size: 18px;
  color: #777;
 }
 
 
 /* Responsive Styles */
 @media (max-width: 992px) {
  .sidebar-content {
    flex-direction: column;
  }
 
 
  .lecture-list {
    width: 100%;
    margin-bottom: 20px;
  }
 
 
  .content-area {
    margin-left: 0;
  }
 }
 
 
 @media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
  }
 
 
  .mobile-close {
    display: block;
  }
 
 
  .lecture-list {
    position: fixed;
    top: 0;
    left: -100%;
    width: 80%;
    height: 100%;
    z-index: 1000;
    overflow-y: auto;
    transition: left 0.3s ease;
    padding-top: 50px;
  }
 
 
  .lecture-list.mobile-active {
    left: 0;
  }
 
 
  .sidebar {
    padding: 10px;
  }
 
 
  .sidebar-content {
    padding-top: 40px;
  }
 
 
  .video-player, .pdf-viewer, .default-page {
    padding: 15px;
  }
 
 
  .default-page {
    padding: 40px 15px;
  }
 }
 
 
 @media (max-width: 480px) {
  h1 {
    font-size: 20px;
  }
 
 
  h3 {
    font-size: 16px;
    padding: 8px;
  }
 
 
  li {
    padding: 8px;
    font-size: 14px;
  }
 }
 
 
 .assignment-container {
  background-color: #ffffff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
 }
 
 
 .mcq-questions {
  margin-top: 20px;
 }
 
 
 .mcq-question {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
 }
 
 
 .mcq-options {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
 }
 
 
 .mcq-options label {
  margin: 5px 0;
  padding: 10px;
  background-color: #f1f1f1;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
 }
 
 
 .mcq-options label:hover {
  background-color: #e0e0e0;
 }
 
 
 .coding-assignment {
  display: flex;
  flex-direction: column;
  gap: 20px;
 }
 
 
 .code-editor textarea {
  width: 100%;
  padding: 10px;
  font-family: monospace;
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-radius: 5px;
  min-height: 300px;
 }
 
 
 .submission-actions {
  display: flex;
  gap: 10px;
 }
 
 
 .submit-btn, .reset-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
 }
 
 
 .submit-btn {
  background-color: #28a745;
  color: white;
 }
 
 
 .reset-btn {
  background-color: #dc3545;
  color: white;
 }
 
 
 .submit-btn:hover {
  background-color: #218838;
 }
 
 
 .reset-btn:hover {
  background-color: #c82333;
 }
 
 
 .assignment-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
 }
 
 
 .assignment-header {
  text-align: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
 }
 
 
 .mcq-question {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 15px;
 }
 
 
 .mcq-question h3 {
  margin-bottom: 10px;
  font-weight: bold;
 }
 
 
 .mcq-options {
  display: flex;
  flex-direction: column;
 }
 
 
 .mcq-option {
  display: flex;
  align-items: center;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #f0f0f0;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.3s ease;
 }
 
 
 .mcq-option:hover {
  background-color: #f5f5f5;
 }
 
 
 .mcq-option input {
  margin-right: 10px;
 }
 
 
 .assignment-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
 }
 
 
 .submit-btn {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
 }
 
 
 .submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
 }
 
 
 .assignment-results {
  margin-top: 20px;
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 5px;
 }
 
 
 .detailed-results {
  margin-top: 15px;
 }
 
 
 .detailed-results ul {
  list-style-type: none;
  padding: 0;
 }
 
 
 .detailed-results li {
  padding: 10px;
  margin: 5px 0;
  border-radius: 3px;
 }
 
 
 .correct-answer {
  background-color: rgba(76, 175, 80, 0.2);
 }
 
 
 .incorrect-answer {
  background-color: rgba(255, 0, 0, 0.2);
 }
 
 
 .python-compiler {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  background-color: #f4f4f4;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
 }
 
 
 .python-compiler iframe {
  width: 100%;
  min-height: 600px;
  max-height: 500px;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
 }
 
 
 @media screen and (max-width: 1200px) {
  .python-compiler iframe {
    min-height: 500px;
  }
 }
 
 
 @media screen and (max-width: 768px) {
  .python-compiler {
    padding: 10px;
  }
 
 
  .python-compiler iframe {
    min-height: 400px;
  }
 }
 
 
 .programming-assignment-container {
  max-width: 1200px; /* Increased width to use more space */
  width: 90%; /* Ensures it adapts on smaller screens */
  margin: 30px auto; /* Centers the container */
  padding: 20px;
  background: #ffffff;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
 }
 
 
 .assignment-header h2 {
  text-align: center;
  margin-bottom: 20px;
 }
 
 
 .coding-area {
  display: flex;
  flex-direction: column;
  align-items: center;
 }
 
 
 .problem-statement {
  width: 100%;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
 }
 
 
 .ide-container {
  width: 100%;
 }
 
 
 .code-editor textarea {
  width: 100%;
  min-height: 200px;
  font-family: monospace;
 }
 
 
 .ide-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
 }
 
 
 .output-area,
 .submission-result {
  width: 100%;
  background: #eef;
  padding: 10px;
  border-radius: 6px;
  margin-top: 15px;
 }
 .chat-button-small {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  cursor: pointer;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}
.chat-button-small {
  display: flex;
  align-items: center;
  justify-content: center;
  width: auto; /* Adjust width dynamically based on text */
  padding: 10px 15px; /* Add padding for better spacing */
  font-size: 14px; /* Ensure readable text */
  white-space: nowrap; /* Prevent text from wrapping */
  border-radius: 20px; /* Rounded corners */
}

.chat-button-small:hover {
  transform: scale(1.05);
}
 
 
 
 
 @media screen and (max-width: 480px) {
  .python-compiler iframe {
    min-height: 300px;
  }
 }
 
 
 </style>
 
 