<template>
  <CourseNavBar/>
  <div class="app-container">
    <div class="content">
      <SidebarComponent @select-content="updateVideo" />
      <VideoPlayerComponent :videoSrc="selectedVideo" />
      <ChatBotComponent />
    </div>
  </div>
</template>

<script>
import SidebarComponent from "@/components/SidebarComponent.vue";
import VideoPlayerComponent from "@/components/VideoPlayerComponent.vue";
import ChatBotComponent from "@/components/ChatBotComponent.vue";
import CourseNavBar from "@/components/courseNavBar.vue";

export default {
  components: {
    CourseNavBar,
    SidebarComponent,
    VideoPlayerComponent,
    ChatBotComponent,
  },
  data() {
    return {
      selectedVideo: "",
    };
  },
  methods: {
    updateVideo(videoUrl) {
      this.selectedVideo = videoUrl;
    },
  },
};
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.content {
  display: flex;
  flex-grow: 1;
}
</style>