import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../../components/HomePage.vue";
import TestePage from "../../components/TestePage.vue";

const routes = [
    {path: '/home', name: 'home', component: HomePage},
    {path: '/teste', name: 'teste', component: TestePage}
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;