import { createRouter, createWebHistory } from 'vue-router';
import Home from "../page/Home.vue";
import Windy from "../page/Windy.vue";
import WindyIframe from "../components/WindyIframe.vue";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        children: [
            {
                path: '',
                redirect: '/windy',
            },
            {
                path: '/windy',
                component: Windy,
            }
        ]
    },
    {
        path: '/windy_iframe',
        name: 'WindyIframe',
        component: WindyIframe,
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

export default router;