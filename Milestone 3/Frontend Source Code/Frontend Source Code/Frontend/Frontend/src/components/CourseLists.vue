<script setup>
import courseData from "@/courses.json"

const coursesData = courseData
</script>

<template>
  <section class="bg-blue-50 px-4 py-10">
    <div class="container-xl lg:container m-auto">
      <h2 class="text-3xl font-bold text-black mb-6 text-center">
        Browse Course
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="course in coursesData.courses" :key="course.id">
          {{ course.subject_name }}
        </div>
      </div>
    </div>
  </section>

</template>

<style scoped>

</style>