import { createRouter, createWebHistory } from "vue-router";

//Componentes
import HomePage from "../../components/HomePage.vue";
import TestePage from "../../components/TestePage.vue";
import PanelPages from "../../components/PanelPages.vue";
import CadastrosVeiculosPage from "../../components/veiculos/CadastrosVeiculosPage.vue";
import CriarVeiculoPage from "../../components/veiculos/CriarVeiculoPage.vue";

//Logica
import CadastrosVeiculos from "../telas/veiculos/CadastrosVeiculos";

const routes = [
    {path: '/site', component: PanelPages,
        children: [
            { path: 'home', name: 'home', component: HomePage },
            { path: 'cadastros-veiculos', name: 'cadveiculos', component: CadastrosVeiculosPage, meta: { classe: CadastrosVeiculos}},
            { path: 'criar-veiculo', name: 'criar-veiculo', component: CriarVeiculoPage}
        ]
    },
    {path: '/teste', name: 'teste', component: TestePage}
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;