<template>
  <LoginNavBar/>

 

  <div class="container">
    <div class="form-container" v-bind:class="{ 'animate-fade-in': true }">
      <h2>{{ isLogin ? 'Login' : 'Sign Up' }}</h2>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">Email</label>
          <input
              type="email"
              id="email"
              v-model="email"
              required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
              type="password"
              id="password"
              v-model="password"
              required
          />
        </div>

        <div v-if="!isLogin" class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              required
          />
        </div>

        <button type="submit" v-bind:class="{ 'animate-button': true }">
          {{ isLogin ? 'Login' : 'Sign Up' }}
        </button>
      </form>

      <p class="toggle-mode">
        {{ isLogin ? "Don't have an account?" : 'Already have an account?' }}
        <button @click="toggleMode" v-bind:class="{ 'animate-link': true }">
          {{ isLogin ? 'Sign Up' : 'Login' }}
        </button>
      </p>
    </div>
  </div>
</template>

<script>
// import Navbar from "@/components/Navbar.vue";
import LoginNavBar from "@/components/loginNavBar.vue";

export default {
  components: {LoginNavBar},
  data() {
    return {
      isLogin: true, // Toggle between login and signup
      email: '',
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    toggleMode() {
      this.isLogin = !this.isLogin;
      this.email = '';
      this.password = '';
      this.confirmPassword = '';
    },
    handleSubmit() {
      if (this.isLogin) {
        if (this.email === 'atharva@gmail.com' && this.password === '123') {
          alert('Login successful! Redirecting to dashboard...');
          this.$router.push('/studentdashboard');
        } else {
          alert('Invalid email or password!');
        }
      } else {
        if (this.password !== this.confirmPassword) {
          alert('Passwords do not match!');
          return;
        }
        alert('Sign Up successful!');
        this.toggleMode();
      }
    },
  },
};
</script>

<style scoped>
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes buttonHover {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.animate-fade-in {
  animation: fadeIn 0.6s ease-out;
}

.animate-button:hover {
  animation: buttonHover 0.4s ease-in-out;
}

.animate-link {
  transition: color 0.3s ease-in-out;
}

.animate-link:hover {
  color: #0056b3;
}

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f9;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.form-container {
  background: #fff;
  padding: 20px 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  color: #666;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

input:focus {
  border-color: #007bff;
  outline: none;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #0056b3;
}

.toggle-mode {
  margin-top: 15px;
  font-size: 14px;
  color: #666;
}

.toggle-mode button {
  background: none;
  border: none;
  color: #007bff;
  font-size: 14px;
  cursor: pointer;
}

.toggle-mode button:hover {
  text-decoration: underline;
}
</style>
