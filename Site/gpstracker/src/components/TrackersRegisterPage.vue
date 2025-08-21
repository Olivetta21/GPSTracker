<template>
    <div id="tracker-page">
        <ModalBase v-if="TC.EditUser.cfg.state" id="editing-users" @close="TC.EditUser.stop()">
            <div>
                <input type="text">
                <p>Pesq</p>
                <p>Reca</p>
            </div>
            <div id="editing-users-table">
                <table>
                    <tbody>
                        <tr v-for="(u, idx) in TC.EditUser.cfg.users" :key="idx">
                            <td><div class="color-state g"></div></td>
                            <td> {{ u.name }} </td>
                            <td>
                                <button @click="TC.EditUser.pauseUser(idx, u.id)"> Pausar </button>
                                <button @click="TC.EditUser.deleteUser(idx, u.id)"> Deletar </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </ModalBase>
        <ModalBase v-if="TC.AddTracker.cfg.state" id="adding-tracker" @close="TC.AddTracker.stop()">
            <template v-if="!TC.AddTracker.cfg.tokenFound">
                <input type="text" placeholder="token" v-model="TC.AddTracker.cfg.token">
                <button @click="TC.AddTracker.find()" > Procurar </button>
            </template>
            <template v-else>
                <p>Token: {{ TC.AddTracker.cfg.token }}</p>
                <input type="text" placeholder="Nome do Rastreador" v-model="TC.AddTracker.cfg.name">
                <p>Dono: {{ TC.AddTracker.cfg.owner || "Você" }}</p>
                <p v-if="TC.AddTracker.cfg.owner"> Esse token já tem dono, confirme para enviar uma solicitação. </p>
                <input v-else type="text" placeholder="senha" v-model="TC.AddTracker.cfg.password">
                <button @click="TC.AddTracker.confirm()">confirmar</button>
            </template>
        </ModalBase>
        <div id="trackers-container">
            <div id="trackers-header">
                <input type="text">
                <p>Pesq</p>
                <p>Reca</p>
                <p @click="TC.AddTracker.start()">Adic</p>
            </div>
            <div id="trackers-table">
                <table>
                    <tbody>
                        <tr v-for="(t, idx) in TC.trackers" :key="idx">
                            <td> <div :class="['color-state', t.state]"></div> </td>
                            <td> {{ t.name }} </td>
                            <td> {{ t.token }} </td>
                            <td> Rastrear </td>
                            <td> <button @click="TC.EditUser.start(idx, t.id)"> Usuarios </button> <button @click="TC.EditUser.mockUser(idx, t.id)"> mock </button></td>
                            <td> <button @click="TC.delTracker(idx, t.id)"> Excluir </button> </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>


<script>

import ModalBase from './ModalBase.vue';
import TrackersRegister from '../scripts/telas/trackersregister/TrackersRegister';

export default {
    data() {
        return {
            editingUsers: true,

            TC: TrackersRegister
        };
    },
    components: { ModalBase },
};
</script>


<style scoped>
    #tracker-page {
        width: 100%;
        height: 100%;
    }

    #trackers-container {
        padding: 20px;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    #trackers-header {
        padding: 8px;
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    #trackers-table {
        flex: 1;
        overflow: auto;
        height: 0;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    tr {
        border: 1px solid #ddd;
    }
    td {
        padding: 8px;
    }

    tr:hover {
        background-color: #f5f5f5;
    }

    .color-state.g {
        background-color: green;
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    .color-state.o {
        background-color: orange;
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    .color-state.r {
        background-color: red;
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }










</style>