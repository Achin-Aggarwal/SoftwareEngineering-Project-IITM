<template>
  <div class="login-container">

    <!-- Notification Message -->
      <div v-if="notification.show"
          :class="['notification', notification.type]"
          class="error-message">
        {{ notification.message }}
      </div>

      <div class="back-to-dashboard">
        <h5 @click="goBack" class="dashboard">← Back to Dashboard</h5>
      </div>
    
    <div class="login-card">         
      <div class= login-section>
      <div class= iitm-heading>
       <img src="@/assets/iitm_logo.png" alt="IITM Logo" class="iitm-logo" />IITM
      </div>
        <h2>{{ isLogin ? 'Login' : 'Sign Up' }}</h2>
         <div class="form-scroll">
        <form @submit.prevent="handleSubmit">
            <!-- Name Field (Only for Signup) -->
            <div v-if="!isLogin" class="form-group">
              <label for="name">Full Name</label>
              <input type="text" id="name" v-model="name" required/>
            </div>   

            <!-- Email / Username Field -->
            <div class="form-group">
              <label for="email">Email</label>
              <input type="email" id="email" v-model="email" @input="generateUsername" required/>
            </div>  

            <!-- Username (Automatically Generated) -->
            <div v-if="!isLogin" class="form-group">
              <label for="username">Username</label>
              <input type="text" id="username" v-model="username" readonly/>
            </div> 
            
            <!-- Password Field with Show/Hide Toggle -->
            <div class="form-group">
              <label for="password">Password</label>
              <div class="password-input">
                <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password" required/>
                <button type="button" @click="togglePassword" class="password-toggle">
                  {{ showPassword ? 'Hide' : 'Show' }}
                </button>
              </div>
            </div>

            <div v-if="!isLogin" class="form-group">
              <label for="confirmPassword">Confirm Password</label>
              <div class="password-input">
                <input :type="showConfirmPassword ? 'text' : 'password'" id="confirmPassword" v-model="confirmPassword"
                      required/>
                <button type="button" @click="toggleConfirmPassword" class="password-toggle">
                  {{ showConfirmPassword ? 'Hide' : 'Show' }}
                </button>
              </div>
            </div>

            <!-- Role Selection (Only for Signup) -->
            <div v-if="!isLogin" class="form-group">
              <label for="role">Select Role</label>
              <select v-model="role" required>
                <option disabled value="">Choose a role</option>
                <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
              </select>
            </div>

            <!-- About Field (Only for Signup) -->
            <div v-if="!isLogin" class="form-group">
              <label for="about">About You</label>
              <textarea id="about" v-model="about" rows="3"></textarea>
            </div>

            <button type="submit" >{{ isLogin ? 'Login' : 'Sign Up' }}</button>

            <!-- Toggle Mode -->
            <p class="toggle-mode">
              {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
              <button @click="toggleMode" class="animate-link">
                {{ isLogin ? 'Sign Up' : 'Login' }}
              </button>

            </p>         
        </form> 
        </div>        
      </div>         
    </div>

    <div class="updates-card">
      <h2 class="U_heading">Latest Updates / Announcements</h2>
      <div class="quiz-info">
        <span class="quiz-label">Quiz Dates for</span>
        <span class="term-badge">Jan <b>2025</b> Term</span>
      </div>
      <ul class="quiz-dates">
        <li>Quiz 1: 23 Feb 2025</li>
        <li>Quiz 2: 16 Mar 2025</li>
        <li>End Term: 13 Apr 2025</li>
      </ul>
    </div>
  </div>
</template>

<script>
import LoginNavBar from "@/components/loginNavBar.vue";
import axios from "axios";
import {jwtDecode} from 'jwt-decode';

export default {
  components: {LoginNavBar},
  data() {
    return {
      isLogin: true,
      name: "",
      email: "",
      username: "",
      password: "",
      confirmPassword: "",
      role: "",
      about: "",
      roles: ["Student", "Instructor"],
      showPassword: false,
      showConfirmPassword: false,
      notification: {
        show: false,
        message: "",
        type: "", // success or error
        timeout: null
      }
    };
  },
  methods: {
    goBack() {
      this.$router.push({path: "/"});
    },
    toggleMode() {
      this.isLogin = !this.isLogin;
      this.name = "";
      this.email = "";
      this.username = "";
      this.password = "";
      this.confirmPassword = "";
      this.role = "";
      this.about = "";
      this.clearNotification();
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    generateUsername() {
      if (this.email.includes("@")) {
        this.username = this.email.split("@")[0].toLowerCase();
      } else {
        this.username = this.email;
      }
    },
    showNotification(message, type = "success") {
      // Clear any existing notification
      this.clearNotification();

      // Set the new notification
      this.notification.show = true;
      this.notification.message = message;
      this.notification.type = type;

      // Auto-hide the notification after 5 seconds
      this.notification.timeout = setTimeout(() => {
        this.notification.show = false;
      }, 5000);
    },
    clearNotification() {
      if (this.notification.timeout) {
        clearTimeout(this.notification.timeout);
      }
      this.notification.show = false;
    },
    async handleSubmit() {
      try {
        if (this.isLogin) {
          const response = await axios.post('http://127.0.0.1:5000/login', {
            username: this.email,
            password: this.password,
          });

          this.showNotification(response.data.message, "success");

          if (response.data.access_token) {
            const {access_token, refresh_token, username} = response.data;

            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);
            localStorage.setItem('username', username);

            // Slight delay before redirecting to show the success message
            setTimeout(() => {
              this.redirectBasedOnRole(access_token);
            }, 1000);
          }
        } else {
          // Validate password match
          if (this.password !== this.confirmPassword) {
            this.showNotification("Passwords do not match!", "error");
            return;
          }
          // Validate role selection
          if (!this.role) {
            this.showNotification("Please select a role.", "error");
            return;
          }

          const response = await axios.post('http://127.0.0.1:5000/signup', {
            name: this.name,
            username: this.email,
            email: this.email,
            password: this.password,
            about: this.about,
            role: this.role,
          });

          this.showNotification(response.data.message, "success");

          if (response.data.message.includes("registered successfully")) {
            // Slight delay before switching to login mode
            setTimeout(() => {
              this.toggleMode();
            }, 2000);
          }
        }
      } catch (error) {
        console.log("Error occurred:", error.response?.data?.message);
        console.log("Setting notification type:", "error");
        this.showNotification(
            error.response?.data?.message || "An error occurred",
            "error"
        );
      }
    },
    redirectBasedOnRole(access_token) {
      try {
        // Decode the JWT token to extract user role
        const decodedToken = jwtDecode(access_token);
        
        const userRole = decodedToken.role;
        // console.log("utoken:",userRole);
        const username = localStorage.getItem('username');

        // Redirect based on user role
        switch (userRole) {
          case 'Admin':
            this.$router.push({name: 'AdminPage', params: {username}});
            break;
          case 'Student':
            this.$router.push({name: 'Home', params: {username}});
            break;
          case 'Professor':
            this.$router.push({name: 'ProfessorPage', params: {username}});
            break;
          case 'Instructor':
            this.$router.push({name: 'InstructorDashboard', params: {username}});
            break;
          default:
            // Redirect to login if role is unknown
            this.$router.push('/admin-login');
            break;
        }
      } catch (error) {
        console.error("Error decoding token:", error);
        this.$router.push('/');
      }
    }
  },
};
</script>


<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: start;
  gap: 30px;
  padding: 40px;
  background: linear-gradient(to right, #ff7e5f, #7b4397);
  height: 100vh;
}

.dashboard {
  position: absolute;
  top: 20px;
  right: 30px;
  z-index: 10;
  font-size: 16px;
  font-weight: 500;
  color: #ffffff;
  cursor: pointer;
  transition: transform 0.3s ease, color 0.3s ease;
}

.dashboard:hover {
  transform: scale(1.1); 
  color: #ffffff;
  
}
.login-card {
  flex: 1;
  justify-content: center;
  align-items: center;
  position: relative;
  background-color: #ffffff;
  padding: 30px;
  width: 100px;
  height: 550px;
  border-radius: 42px;
  box-shadow: 0 10px 16px rgba(245, 103, 238, 0.68);
  display: flex;
  justify-content: center;   
  position: relative; 

}

.login-section {
  width: 400px;
  margin: 100px auto;
  max-height: 550px;  
  padding: 30px;
  border-radius: 35px;
  background: linear-gradient(135deg, #ffffff, #f3f4f6);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  color: #333;
}


.form-scroll {
  max-height: 300px;
  overflow-y: auto;
  padding-right: 10px;
}

.iitm-heading {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
  
  font-size: 2.4rem;
  font-weight: 500;
  color: #222; 
  
}

.iitm-logo {
  width: 40px;
  margin-right: 10px;
}


h2 {
    text-align: center;
    font-size: 1.8rem;
    margin-bottom: 20px;
    color: #222;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    font-weight: bold;
    margin-bottom: 8px;
    color: #555;
}

.form-group input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1rem;
    background: #fff;
    color: #333;
    transition: border-color 0.3s ease;
}

.form-group input:focus {
    border-color: #007bff;
    box-shadow: 0 0 8px rgba(0, 123, 255, 0.3);
    outline: none;
}

.password-input {
  position: relative;
  display: flex;
}

.password-input input {
  flex: 1;
  padding-right: 70px;
}

.password-toggle {
  position: absolute;
  right: 0;
  top: 0;
  width: auto;
  height: 100%;
  padding: 0 10px;
  background: #e9e9e9;
  border: 1px solid #ddd;
  border-left: none;
  border-radius: 0 5px 5px 0;
  font-size: 12px;
  color: #666;
  margin: 0;
}

.password-toggle:hover {
  background: #d9d9d9;
  color: #333;
}

button {
    width: 100%;
    padding: 12px;
    background:linear-gradient(135deg,rgb(116, 65, 235),rgb(81, 207, 230));
    color: #fff;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s, transform 0.2s ease-in-out;
}

button:hover {
    background:linear-gradient(135deg,rgb(102, 209, 252),rgb(92, 74, 248));
    transform: scale(1.02);
}

.toggle-mode {
  margin-top: 15px;
  font-size: 16px;
  color: #666;
}

.toggle-mode button {
  background: none;
  border: none;
  color: #007bff;
  font-size: 14px;
  cursor: pointer;
  padding: 0;
  margin: 0;
  width: auto;
}

.toggle-mode button:hover {
  
  background: none;
  transform: scale(1.02);
}

label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  color: #666;
}

input, select, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

input:focus, select:focus, textarea:focus {
  

  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.3);
  outline: none;
}

.animate-link {
  transition: color 0.3s ease-in-out;
  
}

.animate-link:hover {
  color: #0056b3;
  transform: scale(1.1);
}

.error-message {
    position: absolute;
    top: 10px; /* Adjust the top value as needed */
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 20px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    z-index: 1000;     
    width: auto;
    max-width: 80%;
    text-align: center;
    background: linear-gradient(135deg, #ffffff, #f3f4f6);
    box-shadow: 0 8px 16px rgba(80, 30, 161, 0.3);
    color: #333;
}


@media (max-width: 768px) {
    .login-container {
        padding: 20px;
    }

    button {
        font-size: 0.9rem;
    }
}


.updates-card {
  flex: 1;
  color: #ffffff;
  padding: 20px;
  width: 350px;
  margin-top: 140px;
  
}

.U_heading{
  font-size: 34px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 30px;
}

.quiz-info {
   
  align-items: center;
  margin-bottom: 10px;
}

.quiz-label {
  font-size: 26px;
  font-weight: 500;
}

.term-badge {
  background-color: #ffffff;
  color: #b6411c;
  font-size: 24px;
  padding: 4px 10px;
  border-radius: 12px;
  margin-left: 8px;
}

.quiz-dates {
  
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.quiz-dates li {
  font-size: 20px;
  font-weight: 300;
  
  margin-bottom: 10px;
}
</style>
