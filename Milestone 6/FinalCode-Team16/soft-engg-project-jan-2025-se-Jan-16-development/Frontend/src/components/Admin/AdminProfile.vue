<template>
  <AdminNavBar/>
  <div class="profile-page">
   <div class="profile-container">
     <div class="profile-header">
       <!-- Loading state -->
       <div v-if="isLoading" class="loading-state">
         Loading instructor details...
       </div>

       <!-- Error state -->
       <div v-else-if="error" class="error-message">
         {{ error }}
       </div>

       <!-- Content when data is loaded -->
       <div v-else>
         <!-- Profile image on top -->
         <div class = "header">
         <div class="image-container">
          <img
              :src="studentProfile"
              alt="Profile Picture"
              class="profile-image"
            />
         </div>


         <!-- Instructor details below the image -->
         <div class="instructor-details">
           <h2 class="instructor-name">{{ instructor.name }}</h2>
           <p class="instructor-role"><strong>Role: </strong> {{ instructor.role }}</p>
           <p class="instructor-email"><strong>Email: </strong> {{ instructor.email }}</p>
           <p class="instructor-username"><strong>Username:</strong> {{ instructor.username }}</p>
         </div>
         </div>
       </div>
     </div>


     <!-- Additional information section -->
     <div v-if="!isLoading && !error" class="additional-info">
       <h3>Account Information</h3>
       <div class="info-item">
         <span class="info-label"><strong>Account Created:</strong></span>
         <span class="info-value">{{ formatDate(instructor.created_at) }}</span>
       </div>
       <div class="info-item">
         <span class="info-label"><strong>Last Login:</strong></span>
         <span class="info-value">{{ formatDate(instructor.last_login) }}</span>
       </div>
     </div>
   </div>
 </div>
</template>



<script setup>
import Navbar from "@/components/Student/Navbar.vue";
import AdminNavBar from "@/components/Admin/AdminNavBar.vue";
// import studentProfile from "@/assets/studentProfile.png";
import {ref, onMounted} from 'vue';
import axios from 'axios';


const instructor = ref({
 id: null,
 name: '',
 username: '',
 email: '',
 role: '',
 created_at: '',
 last_login: ''
});

const gender = Math.random() < 0.5 ? "men" : "women";
const number = Math.floor(Math.random() * 100);
const studentProfile = ref(`https://randomuser.me/api/portraits/${gender}/${number}.jpg`);

const isLoading = ref(true);
const error = ref(null);


// Fetch Instructor profile data from API
const fetchInstructorProfile = async () => {
 try {
   isLoading.value = true;
   error.value = null;


   const token = localStorage.getItem("access_token");
   if (!token) {
     error.value = "No access token found. Please log in again.";
     isLoading.value = false;
     console.error("No access token found");
     return;
   }


   const response = await axios.get("http://localhost:5000/admin_details", {
     headers: {
       Authorization: `Bearer ${token}`
     }
   });


   console.log("API Response:", response.data);


   // Update the instructor data with API response
   const profileData = response.data;
   instructor.value = {
     ...instructor.value,
     name: profileData.name,
     email: profileData.email,
     username: profileData.username,
     role: profileData.role,
     created_at: profileData.created_at,
     last_login: profileData.last_login
   };


   isLoading.value = false;
 } catch (err) {
   error.value = err.response?.data?.message || 'Failed to load instructor details';
   isLoading.value = false;
   console.error("Error fetching instructor profile:", err);
 }
};


// Format date function
const formatDate = (dateString) => {
 if (!dateString) return 'N/A';
 return new Date(dateString).toLocaleDateString('en-US', {
   year: 'numeric',
   month: 'long',
   day: 'numeric'
 });
};


// Call the fetch function when component mounts
onMounted(() => {
 fetchInstructorProfile();
});
</script>



<style scoped>
.profile-page {
  font-family: 'Inter', Arial, sans-serif;
  background: linear-gradient(to right, #ff7e5f, #7b4397);
  padding: 50px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-container {
  width: 100%;
  max-width: 900px;
  background-color: #ffffff;
  padding: 30px;
  border-radius: 20px;
  /*box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);*/
  box-shadow: 0 10px 16px rgba(245, 103, 238, 0.68);
  
  transition: box-shadow 0.3s ease;
}

.profile-container:hover {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

/*.profile-header {
  display: flex;
  align-items: center;
  gap: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #e0e0e0;
  
}*/

.header{
  display: flex;  
  align-items: center;
  gap: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #e0e0e0;  

}


.image-container {
  padding-bottom: 25px;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.profile-image {
  width: 100%;
  height: 320px;
  border-radius: 50%; /* Square with rounded corners */
  object-fit: cover;
  border: 2px solid #e0e0e0;
  box-shadow: 0 8px 16px rgba(195, 24, 247, 0.4);
  transition: transform 0.2s ease-in-out;
}

.profile-image:hover {
  transform: scale(1.05); 
}

.instructor-details {
  width: 50%;
  height: 360px;
  text-align: left;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(195, 24, 247, 0.4);
  border: 1px solid #e0e0e0;
}

.instructor-details h2 {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  border-bottom: 2px solid #007bff;
  display: inline-block;
  padding-bottom: 4px;
}

.instructor-details p {
  font-size: 20px;
  color:  #333;
  margin: 8px 0;
  line-height: 1.6;
  display: flex;
  align-items: center;
}

.instructor-details strong {
  font-weight: 500;
  color: #007bff;
  width: 150px; 
  display: inline-block;
}

.additional-info{
  margin-top: 30px;
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}


.additional-info:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.additional-info h3 {
  font-size: 24px;
  font-weight: 700;
  color: #6a11cb;
  margin-bottom: 16px;
  text-align: left;
  border-bottom: 2px solid #6a11cb;
  padding-bottom: 6px;
}


.info-item {
  background-color: #f8f9fa;
  padding: 12px 20px;
  margin-bottom: 10px;
  border-radius: 8px;
  font-size: 16px;
  color: #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.info-item:hover {
  background-color: #e9ecef;
}

.info-item span {
  margin-right: 10px;
}

@media (max-width: 768px) {
  .additional-info h3 {
    text-align: center;
  }

  .info-item {
    text-align: center;
  }
}
</style>