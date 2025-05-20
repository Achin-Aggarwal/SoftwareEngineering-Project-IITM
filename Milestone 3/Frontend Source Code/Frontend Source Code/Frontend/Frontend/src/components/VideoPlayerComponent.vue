<template>
    <div class="video-player" v-if="isYoutubeVideo(videoSrc)">
      <iframe
          :src="'https://www.youtube.com/embed/' + getVideoId(videoSrc)"
          width="1200"
          height="615"
          frameborder="0"
          allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
      ></iframe>
    </div>
</template>

<script>
export default {
  props: ["videoSrc"],
  methods: {
    // Check if the URL is a valid YouTube video URL
    isYoutubeVideo(url) {
      return url && (url.startsWith("https://youtu.be") || url.startsWith("https://www.youtube.com"));
    },

    // Extract video ID from the URL for embedding
    getVideoId(url) {
      const match = url.match(/(?:v=|\/)([a-zA-Z0-9_-]{11})/);
      return match ? match[1] : '';
    }
  },
};
</script>



<style scoped>
.video-player {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
  color: #fff;
  padding: 10px;
}

iframe {
  max-width: 100%;
  max-height: 100%;
}
</style>
