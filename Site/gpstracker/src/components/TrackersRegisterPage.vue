<template>
    <div id="tracker-page">
        <ModalBase v-if="editingUsers" id="editing-users" @close="editingUsers = false">
            <div>
                <input type="text">
                <p>Pesq</p>
                <p>Reca</p>
            </div>
            <div id="editing-users-table">
                <table>
                    <tbody>
                        <tr>
                            <td><div class="color-state g"></div></td>
                            <td> Ivan </td>
                            <td>
                                <button> Pausar </button>
                                <button> Deletar </button>
                            </td>
                        </tr>
                        <tr>
                            <td><div class="color-state o"></div></td>
                            <td> kelvin </td>
                            <td>
                                <button> Iniciar </button>
                                <button> Deletar </button>
                            </td>
                        </tr>
                        <tr>
                            <td><div class="color-state r"></div></td>
                            <td> kaio </td>
                            <td>
                                <button> Aprovar </button>
                                <button> Deletar </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </ModalBase>
        <ModalBase v-if="addingTracker" id="adding-tracker" @close="addingTracker = false">
            <template v-if="!TC.Adding.tokenFound">
                <input type="text" placeholder="token" v-model="TC.Adding.token">
                <button @click="TC.Adding.tokenFound = true" > Procurar </button>
            </template>
            <template v-else>
                <p>Token: {{ TC.Adding.token }}</p>
                <input type="text" placeholder="Nome do Rastreador" v-model="TC.Adding.nome">
                <p>Dono: {{ TC.Adding.dono || "Você" }}</p>
                <p v-if="TC.Adding.dono"> Esse token já tem dono, confirme para enviar uma solicitação. </p>
                <input v-else type="text" placeholder="senha" v-model="TC.Adding.senha">
                <button >confirmar</button>
            </template>
        </ModalBase>
        <div id="trackers-container">
            <div id="trackers-header">
                <input type="text">
                <p>Pesq</p>
                <p>Reca</p>
                <p>Adic</p>
            </div>
            <div id="trackers-table">
                <table>
                    <tbody>
                        <tr>
                            <td> <div class="color-state g"></div> </td>
                            <td> Carro1 </td>
                            <td> XXXXXXXXXX </td>
                            <td> Rastr </td>
                            <td> Usrs </td>
                            <td> Excl </td>
                        </tr>
                        <tr>
                            <td> <div class="color-state r"></div> </td>
                            <td> Carro2 </td>
                            <td> XXXXXXXXXX </td>
                            <td> Rastr </td>
                            <td> Usrs </td>
                            <td> Excl </td>
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
            addingTracker: true,

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