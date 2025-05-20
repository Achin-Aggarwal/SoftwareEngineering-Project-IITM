<template>
  <div class="navbar">
      <div class="logo-container" @click="reloadPage" style="cursor: pointer">
        <img class="logo" :src="iitm_logo" alt="IITM Logo"/>
        <span class="logo-text">IIT Madras</span>
      </div>

    <span class="text">
      Bachelor of Science (BS) <br/>
      Degree in Data Science and Applications
    </span>

    <div class="btn-container">
      <button class="btn" @click="login">Login and Signup</button>
    </div>
  </div>

  <!-- Main Content -->
  <div class="home-container">
    <div class="video-section">
      <div class="video-card">
        <template v-if="!isPlaying">
          <!-- YouTube Thumbnail with Play Button -->
          <div class="video-placeholder">
            <img class="youtube-thumbnail" :src="thumbnailUrl" alt="Video Thumbnail"/>
            <button class="play-btn" @click="playVideo">▶</button>
          </div>
        </template>

        <template v-else>
          <!-- Embedded YouTube Video -->
          <iframe
              class="youtube-video"
              :src="computedVideoUrl"
              allow="autoplay; encrypted-media"
              allowfullscreen
          ></iframe>
        </template>
      </div>
    </div>

    <!-- Text Section -->
    <div class="text-section">
      <h2>
        <span class="highlight-red">IIT Madras</span>, India's top technical
        institute, welcomes you to the
        <span class="highlight-gold"
        >world's first 4-year Bachelor of Science (BS) Degree in Data Science
          and Applications</span
        >
        with options to exit earlier in the foundation, diploma, or BSc degree
        level.
      </h2>
      <p>
        For the first time, you can work towards an undergraduate
        degree/diploma from an IIT regardless of your age, location, or
        academic background.
      </p>
      <p>More than 36,000 students currently studying with us in the program.</p>

    </div>
  </div>

  <!-- Message from Director Section -->
  <div class="director-section">
    <div class="director-card">
      <img class="director-image" :src="prof_image" alt="Professor Image"/>
      <div class="director-text">
        <h3 class="director-title">Message from Director</h3>
        <p>
          <strong>IIT Madras</strong> started this unique BS program to provide access to IIT-quality education to
          learners across the country.
          <span class="highlight">Data Science</span> is a growing field and the demand for skilled resources in the
          market is very high.
        </p>
        <p>
          <strong>IIT Madras</strong> has a rich history of providing high-quality education, and this program is
          designed to underline the fact that IIT is within the reach of everyone.
          This BS program is meticulously drafted and aligned with the goals of the National Educational Policy.
        </p>
        <p>
          We are planning to make <strong>IIT Madras</strong> a
          <span class="highlight-red">'Vishwa-guru (Global Teacher)'</span> through innovative approaches to enhance the
          quality of education.
        </p>
        <p class="director-name">
          <strong>Prof. V. Kamakoti</strong> <br/>
          Director, IIT Madras
        </p>
      </div>
    </div>
  </div>

  <div class="stats-section">
    <div class="stat-card" v-for="(stat, index) in stats" :key="index">
      <h2>{{ stat.value }}</h2>
      <p>{{ stat.description }}</p>
    </div>
  </div>
</template>

<script>
import iitm_logo from '@/assets/iitm_logo.png'
import prof_image from '@/assets/prof_image.png'

export default {
  data() {
    return {
      isPlaying: false,
      videoId: "lEMtlAqlJww",
      videoBaseUrl: "https://www.youtube.com/embed/lEMtlAqlJww",
      stats: [
        {
          value: '20,000+',
          description: 'Students doing this program along with another degree'
        },
        {
          value: '3000+',
          description: 'Working Professionals studying in the program'
        },
        {
          value: '850+',
          description:
              'Secured Admission to Masters/PhD programs within and outside India'
        },
        {
          value: '20+',
          description: 'BS students in Top 100 Ranks of GATE Exam 2024'
        }
      ]
    };
  },
  computed: {
    iitm_logo() {
      return iitm_logo
    },
    prof_image() {
      return prof_image
    },
    computedVideoUrl() {
      return this.isPlaying ? `${this.videoBaseUrl}?autoplay=1` : "";
    },
    thumbnailUrl() {
      // YouTube offers several thumbnail options, maxresdefault is the highest quality
      return `https://img.youtube.com/vi/${this.videoId}/maxresdefault.jpg`;
    },
    reloadPage(){
      window.location.reload();
    }
  },
  methods: {
    login() {
      this.$router.push("/login");
    },
    signIn() {
      this.$router.push("/login");
    },
    playVideo() {
      this.isPlaying = true;
    }
  }
};
</script>

<style scoped>
:root {
  --primary-gradient: linear-gradient(to right, #ff7e5f, #7b4397);
  --highlight-red: #b71c1c;
  --highlight-gold: goldenrod;
  --card-gradient: linear-gradient(135deg, #ff512f, #dd2476);
  --card-hover-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
  --director-bg: linear-gradient(to right, rgb(250, 205, 153), rgb(245, 215, 207));
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;

  background: linear-gradient(to right, #dc4825, #d96779);
  color: white;
  font-weight: bold;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  height: 70px;
  width: 70px;
}

.logo-text {
  font-size: 20px;
  font-weight: bold;
}

.text {
  flex-grow: 1;
  text-align: center;
  font-size: 24px;
}

.btn-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn {
  background-color: transparent;
  color: #ffffff;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 24px;
  transition: background-color 0.3s, color 0.3s;
}


.btn:hover {
  background-color: #6224d5;
}

/* Container Styling */
.home-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  padding-top: 100px; /* Adjust based on navbar height */
}

/* Video Section */
.video-section {
  flex: 1;
  display: flex;
  justify-content: center;
}

.video-card {
  position: relative;
  width: 400px;
  height: 250px;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 10px;
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.youtube-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 0, 0, 0.8);
  color: white;
  border: none;
  font-size: 20px;
  padding: 15px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s, transform 0.3s;
}

.play-btn:hover {
  background-color: red;
  transform: translate(-50%, -50%) scale(1.1);
}

/* YouTube Video */
.youtube-video {
  width: 100%;
  height: 100%;
  border-radius: 10px;
}

/* Text Section */
.text-section {
  flex: 2;
  font-size: 16px;
}

h2 {
  font-size: 20px;
  line-height: 1.5;
}

.highlight-red {
  color: #b71c1c;
  font-weight: bold;
}

.highlight-gold {
  color: goldenrod;
  font-weight: bold;
}

/* Links */
.links {
  margin-top: 10px;
}

.details-link, .fee-link {
  display: inline-flex;
  align-items: center;
  font-size: 16px;
  color: blue;
  font-weight: bold;
  text-decoration: none;
  margin-right: 20px;
}

.new-icon {
  width: 40px;
  height: auto;
  margin-right: 5px;
}

/* Message from Director Section */
.director-section {
  padding: 10px;
}

.director-card {
  display: flex;
  gap: 20px;
  padding: 20px;
  
}

.director-image {
  width: 400px;
  height: 400px;
  object-fit: cover;
  background: linear-gradient(to right, rgb(250, 205, 153), rgb(245, 215, 207));
  box-shadow: 0 10px 10px rgba(197, 6, 214, 0.6);
  padding: 20px;
  border-radius: 50px;
  /*box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);*/
}

.director-text {
  flex: 1;
  line-height: 1.6;
  font-size: 18px;
  color: #444;
  background: linear-gradient(to right, rgb(250, 205, 153), rgb(245, 215, 207));
 
  padding: 20px;
  border-radius: 50px;
  box-shadow: 0 10px 10px rgba(197, 6, 214, 0.6);
}

.director-title {
  font-size: 28px;
  font-weight: 700;
  color: #b71c1c;
  margin-bottom: 12px;
  text-transform: uppercase;
}

.director-text p {
  margin-bottom: 15px;
  font-weight: 400;
}

.director-text .highlight {
  color: #ff5722;
  font-weight: 600;
}

.director-text .highlight-red {
  color: #d32f2f;
  font-weight: 700;
}

.director-name {
  margin-top: 20px;
  font-size: 18px;
  font-weight: bold;
  color: #b71c1c;
}

/* Stats Section Styling */
.stats-section {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 30px;
  flex-wrap: wrap;
}

.stat-card {
  background: linear-gradient(135deg, #ff512f, #dd2476);
  color: #fff;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  width: 280px;
}

.stat-card h2 {
  font-size: 28px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 10px;
}

.stat-card p {
  font-size: 16px;
  font-weight: 500;
  color: #fdfdfd;
  line-height: 1.4;
}

/* Hover Effect */
.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .director-card {
    flex-direction: column;
    align-items: center;
  }

  .director-image {
    width: 300px;
    height: 300px;
  }
}

@media (max-width: 768px) {
  .home-container {
    flex-direction: column;
    padding-top: 120px;
  }

  .text-section {
    order: -1;
  }

  .navbar {
    flex-direction: column;
    padding: 10px;
  }

  .text {
    margin: 10px 0;
    font-size: 20px;
  }

  .stats-section {
    gap: 10px;
  }

  .stat-card {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .director-image {
    width: 200px;
    height: 200px;
  }

  .video-card {
    width: 100%;
    height: auto;
    aspect-ratio: 16/9;
  }
}
</style>