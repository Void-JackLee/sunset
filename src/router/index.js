import { createRouter, createWebHistory } from 'vue-router';
import Home from "../page/Home.vue";
import Windy from "../page/Windy.vue";
import WindyIframe from "../components/WindyIframe.vue";

const BASE = import.meta.env.BASE_URL;

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
        path: BASE.indexOf('sunset') === -1 ? '/sunset/windy_iframe' : '/windy_iframe',
        name: 'WindyIframe',
        component: WindyIframe,
    }
]

const router = createRouter({
    history: createWebHistory(BASE),
    routes
});

export default router;