<!--<script setup>-->
<!--import Card from "@/components/Card.vue";-->
<!--import courses from '@/courses.json';-->
<!--import Navbar from "@/components/Student/Navbar.vue";-->

<!--const courseData = courses;-->
<!--</script>-->

<!--<template>-->
<!--  <Navbar></Navbar>-->
<!--  <section class="py-4">-->
<!--    <div class="container-xl lg:container m-auto">-->
<!--      <h1 class="text-2xl font-bold text-black mb-6">-->
<!--        My Current Courses-->
<!--      </h1>-->
<!--      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-4 rounded-lg">-->
<!--        <Card v-for="course in courseData.courses" :key="course.id">-->
<!--          <h2 class="text-2xl font-bold">-->
<!--            {{ course.subject_name }}-->
<!--          </h2>-->
<!--          <br>-->
<!--          <ul class="mt-2 mb-4">-->
<!--            &lt;!&ndash; Loop over the marks object to display assignment marks &ndash;&gt;-->
<!--            <li v-for="(mark, assignment) in course.marks" :key="assignment">-->
<!--              {{ assignment }}- {{ mark }}-->
<!--            </li>-->
<!--          </ul>-->
<!--          <router-link to="/course">-->
<!--            <button class="go-to-course-btn">Go to Courses</button>-->
<!--          </router-link>-->
<!--        </Card>-->
<!--      </div>-->
<!--    </div>-->
<!--  </section>-->
<!--</template>-->

<!--<style scoped>-->
<!--.go-to-course-btn {-->
<!--  margin-top: 20px;-->
<!--  padding: 10px 20px;-->
<!--  background-color: #089f29;-->
<!--  color: white;-->
<!--  border: none;-->
<!--  border-radius: 5px;-->
<!--  cursor: pointer;-->
<!--  font-size: 16px;-->
<!--}-->

<!--.go-to-course-btn:hover {-->
<!--  background-color: #45a049;-->
<!--}-->
<!--</style>-->