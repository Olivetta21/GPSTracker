import { createRouter, createWebHistory } from "vue-router";

//Componentes
import PanelPages from "../../components/PanelPages.vue";
import MapPage from "../../components/MapPage.vue";
import TrackerPage from "../../components/TrackersRegisterPage.vue";

//Logica

const routes = [
    {path: '/site', component: PanelPages,
        children: [
            { path: 'mapa', name: 'mapa', component: MapPage },
            { path: 'cadastros-rastreadores', name: 'cadrastreador', component: TrackerPage },
        ]
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;