<template>
  <div class="sidebar">
    <div class="sidebar-content">
      <div class="lecture-list">
        <h1>Software Engineering</h1>
        <ul>
          <li v-for="(week, index) in courseContent" :key="index">
            <h3 @click="toggleWeek(index)">
              {{ week.title }}
              <span>{{ expandedWeek === index ? '▲' : '▼' }}</span>
            </h3>
            <ul v-show="expandedWeek === index">
              <li
                  v-for="(item, idx) in week.items"
                  :key="idx"
                  @click="selectContent(item.videoUrl, idx)"
                  :class="{ 'selected': selectedLecture === idx && currentWeek === index }"
              >
                <span v-if="selectedLecture === idx && currentWeek === index" class="dot"></span>
                {{ item.name }}
              </li>
            </ul>
          </li>
        </ul>
      </div>

      <!-- Video Player or Default Page Section -->
      <div class="video-player" v-if="selectedVideoUrl">
        <VideoPlayerComponent :videoSrc="selectedVideoUrl" />
      </div>
      <div class="default-page" v-else>
        <h3>Welcome to the Software Engineering Course</h3>
        <p>Select a lecture from the list to start learning!</p>
      </div>
    </div>
  </div>
</template>

<script>
import VideoPlayerComponent from './VideoPlayerComponent.vue';

export default {
  components: {
    VideoPlayerComponent,
  },
  data() {
    return {
      expandedWeek: null,
      selectedVideoUrl: null,
      selectedLecture: null,
      currentWeek: null,
      courseContent: [
        {
          title: "Week 1",
          items: [
            { name: "Lecture 1", videoUrl: "https://www.youtube.com/watch?v=hKm_rh1RTJQ&list=PLZ2ps__7DhBYt5yvXrYAjjWtf5O399Xea&index=1&pp=iAQB" },
            { name: "Lecture 2", videoUrl: "https://www.youtube.com/watch?v=81BaOIrfvJA&list=PLZ2ps__7DhBYt5yvXrYAjjWtf5O399Xea&index=2&pp=iAQB" },
            { name: "Lecture 3", videoUrl: "https://www.youtube.com/watch?v=SU2CBhSFUUA&list=PLZ2ps__7DhBYt5yvXrYAjjWtf5O399Xea&index=3&pp=iAQB" },
          ],
        },
        {
          title: "Week 2",
          items: [
            { name: "Lecture 1", videoUrl: "https://www.youtube.com/watch?v=6cjKDEoCvMc&list=PLZ2ps__7DhBYt5yvXrYAjjWtf5O399Xea&index=8&t=2s&pp=iAQB" },
            { name: "Lecture 2", videoUrl: "https://www.youtube.com/watch?v=L9-CUa0BlLk&list=PLZ2ps__7DhBYt5yvXrYAjjWtf5O399Xea&index=9&pp=iAQB" },
          ],
        },
      ],
    };
  },
  methods: {
    toggleWeek(index) {
      this.expandedWeek = this.expandedWeek === index ? null : index;
    },
    selectContent(videoUrl, idx) {
      this.selectedVideoUrl = videoUrl;
      this.selectedLecture = idx;
      this.currentWeek = this.expandedWeek;
    },
  },
};
</script>

<style scoped>
/* Global Styles */
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
  width: 100%;
  height: 90%;
  background: #f4f6f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.sidebar-content {
  display: flex;
  width: 100%;
}

.lecture-list {
  width: 300px;
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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
  background-color: transparent; /* Remove hover effect */
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

.video-player {
  flex-grow: 1;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.video-player iframe {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  background-color: #28a745; /* Green dot */
  border-radius: 50%;
  margin-right: 10px;
}

.default-page {
  margin-left: 450px;
  margin-top: 20px;
  margin-bottom: 20px;
  text-align: center;
  padding: 100px;
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
</style>
