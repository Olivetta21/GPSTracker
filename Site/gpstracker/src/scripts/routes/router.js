import { createRouter, createWebHistory } from "vue-router";

import HelloWorld from "../../components/HelloWorld.vue";
import TestePage from "../../components/TestePage.vue";

const routes = [
    {path: '/home', name: 'home', component: HelloWorld},
    {path: '/teste', name: 'teste', component: TestePage}
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;