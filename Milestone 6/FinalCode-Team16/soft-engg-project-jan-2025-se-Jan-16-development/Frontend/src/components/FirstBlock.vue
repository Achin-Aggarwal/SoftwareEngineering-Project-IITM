<script setup>
import {defineProps} from 'vue';

defineProps({
  title: {
    type: String,
    default: 'Welcome'
  },
  subtitle: {
    type: String,
    default: 'sub'
  }
})
</script>

<template>
  <section class="hero-section">
    <div class="hero-container">
      <div class="hero-content">
        <h1 class="hero-title">{{ title }}</h1>
        <p class="hero-subtitle">{{ subtitle}}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-section {
  background-color: #f29857; /* Dark green background */
  padding: 90px 0; /* Top and bottom padding */
  margin-bottom: 16px; /* Space below the section */
}

.hero-container {
  max-width: 1200px; /* Limit the width */
  margin: 0 auto; /* Center the container */
  padding: 0 20px; /* Add padding for smaller screens */
  display: flex;
  flex-direction: column;
  align-items: center; /* Center content horizontally */
}

.hero-content {
  text-align: center; /* Center text */
}

.hero-title {
  color: white; /* White text color */
  font-size: 2.5rem; /* Base font size for smaller screens */
  font-weight: 800; /* Extra-bold font weight */
  line-height: 1.2;
}

@media (min-width: 640px) {
  .hero-title {
    font-size: 3rem; /* Larger font size for medium screens */
  }
}

@media (min-width: 768px) {
  .hero-title {
    font-size: 3.75rem; /* Even larger font size for larger screens */
  }
}

.hero-subtitle {
  color: white; /* White text color */
  margin-top: 16px; /* Space above subtitle */
  margin-bottom: 16px; /* Space below subtitle */
  font-size: 1.25rem; /* Font size for subtitle */
}
</style>