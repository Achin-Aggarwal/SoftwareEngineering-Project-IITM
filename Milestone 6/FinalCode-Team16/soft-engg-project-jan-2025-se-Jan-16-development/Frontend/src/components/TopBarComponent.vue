<template>
  <div class="top-bar">
    <button @click="goHome">Home</button>
    <button @click="viewProfile">User</button>
  </div>
</template>

<script>
export default {
  methods: {
    goHome() {
      console.log("Navigating to Home");
    },
    viewProfile() {
      console.log("Viewing User Profile");
    },
  },
};
</script>

<style scoped>
.top-bar {
  display: flex;
  justify-content: space-between;
  background: #333;
  color: white;
  padding: 10px;
}
button {
  background: #555;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}
</style>