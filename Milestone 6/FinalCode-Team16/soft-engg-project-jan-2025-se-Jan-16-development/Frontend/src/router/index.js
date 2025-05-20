import {createRouter, createWebHistory} from 'vue-router';
import HomeView from "@/views/HomeView.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import LoginPage from "@/views/LoginSignupPage.vue";
import CoursePage from "@/views/CoursePage.vue";
import InstructorDashboard from "@/views/InstructorDashboard.vue";
import QueryDetails from "@/views/QueryDetails.vue";
import AddLesson from "@/views/AddLesson.vue";
import AddAssignment from "@/views/AddAssignment.vue";
import AddLiveSession from "@/views/AddLiveSession.vue";
import Chatbot from "@/views/Chatbot.vue";
import CollegeHomePage from "@/views/CollegeHomePage.vue";
import AdminPage from "@/views/AdminPage.vue";
import ProfessorPage from "@/views/ProfessorPage.vue";
import AdminChatBot from "@/components/Admin/AdminChatBot.vue";
import InstructorChatBot from "@/components/Instructor/InstructorChatBot.vue";
import InstructorProfile from "@/components/Instructor/InstructorProfile.vue";
import AdminProfile from "@/components/Admin/AdminProfile.vue";
import ProfessorProfile from "@/components/Professor/ProfessorProfile.vue";
import ProfessorChatBot from "@/components/Professor/ProfessorChatBot.vue";
import StudentChatBot from "@/components/Student/StudentChatBot.vue";
import InstructorQueryChatBot from "@/views/InstructorQueryChatBot.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            // Project Main Page
            path: "/",
            name: "CollegeHomePage",
            component: CollegeHomePage
        },
        {
            // Login Page
            path: '/login',
            name: 'LoginPage',
            component: LoginPage
        },
                                        // // // Student Pages // // //
                                        {
                                            // Student Dashboard
                                            path: '/studentdashboard/:username?',
                                            name: 'Home',
                                            component: HomeView,
                                            props: true,
                                            meta: { requiresAuth: true }
                                        },
        {
            path: '/profile/:username?',
            name: 'ProfilePage',
            component: ProfilePage,
            meta: { requiresAuth: true }
        },
        {
            path: '/course/:id?',
            name: 'CoursePage',
            component: CoursePage,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            path: '/studentchatbot',
            name: 'StudentChatBot',
            component: StudentChatBot,
              meta: { requiresAuth: true }
          },
                                        // // // Instructor Pages // // //
        {
            // Instructor Dashboard
            path: '/instructordashboard/:username?',
            name: 'InstructorDashboard',
            component: InstructorDashboard,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            path: '/instructorprofile/:username?',
            name: 'InstructorProfile',
            component: InstructorProfile,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            // Students Queries in the Instructor Dashboard
            path: '/query/:id',
            name: 'QueryDetails',
            component: QueryDetails,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            // Add Lessons
            path: '/add-lesson',
            name: 'AddLesson',
            component: AddLesson
        },
        {
            // Add Assignment
            path: '/add-assignment',
            name: 'AddAssignment',
            component: AddAssignment,
            props:true,
            meta: {requiresAuth: true}
         },
        {
            // Add Live Session
            path: '/add-live-session',
            name: 'AddLiveSession',
            component: AddLiveSession,
            props: true,
            meta: { requiresAuth: true }             
        },
        {
            // Instructor Chatbot
            path: '/instructorchatbot',
            name: 'InstructorChatBot',
            component: InstructorChatBot,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            path: '/instructor/assistant',
            name: 'InstructorChatbot',
            component: InstructorChatBot
        },
        {
            path: '/instructorquery',
            name: 'InstructorQueryChatBot',
            component: InstructorQueryChatBot,
            meta: { requiresAuth: true }
        },
      
        {
            path: '/chatbot',
            name: 'Chatbot',
            component: Chatbot,
        },
                                        // // // Admin Pages // // //
        {
            // Admin Page
            path: '/adminpage/:username',
            name: 'AdminPage',
            component: AdminPage,
            meta: { requiresAuth: true }
        },
        {
            // Admin Profile
            path: '/admin/profile',
            name: 'AdminProfile',
            component: AdminProfile,
            meta: { requiresAuth: true }
        },
        {
            // Admin ChatBot
            path: '/adminchatbot',
            name: 'AdminChatbot',
            component: AdminChatBot,
            meta: { requiresAuth: true }
        },
                                            // // // Professor Pages // // //
        {
            // Professor Dashboard
            path: '/professorpage/:username',
            name: 'ProfessorPage',
            component: ProfessorPage,
            meta: { requiresAuth: true }
        },
        {
            // Professor Profile
            path: '/professor/profile',
            name: 'ProfessorProfile',
            component: ProfessorProfile,
            meta: { requiresAuth: true }
        },
        {
            // Professor Chat Bot
            path: '/professorchatbot',
            name: 'ProfessorChatbot',
            component: ProfessorChatBot,
            meta: { requiresAuth: true }
        }
    ]
});

// Add this navigation guard after creating the router
router.beforeEach((to, from, next) => {
    // Check if the route requires authentication
    if (to.meta.requiresAuth) {
        // Check if user is logged in - check both localStorage and sessionStorage
        const accessToken = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
        if (!accessToken) {
            // If not logged in, redirect to login page
            next('/login');
        } else {
            // Continue navigation
            next();
        }
    } else {
        // For non-protected routes, always allow access
        next();
    }
});


export default router;
