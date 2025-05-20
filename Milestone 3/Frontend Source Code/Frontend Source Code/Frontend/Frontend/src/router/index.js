import { createRouter, createWebHistory } from 'vue-router';
import HomeView from "@/views/HomeView.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import LoginPage from "@/views/LoginSignupPage.vue";
import CoursePage from "@/views/CoursePage.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/studentdashboard',
            name: 'Home',
            component: HomeView
        },
        {
            path: '/profile',
            name:'ProfilePage',
            component: ProfilePage
        },
        {
            path: '/',
            name: 'LoginPage',
            component: LoginPage
        },
        {
            path:'/course',
            name:'CoursePage',
            component: CoursePage
        }
    ]
});

export default router;
