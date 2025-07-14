<template>
    <div id="cadveiculos">
        <h1>Cadastro de Veículos</h1>
        <form @submit.prevent>
            <div>
                <label for="vehicleName">Nome do Veículo:</label>
                <input type="text" id="vehicleName" name="vehicleName" v-model="nome" required>
            </div>
            <div>
                <label for="vehicleType">Tipo de Veículo:</label>
                <select id="vehicleType" name="vehicleType" v-model="tipo">
                    <option value="carro">Carro</option>
                    <option value="moto">Moto</option>
                    <option value="caminhao">Caminhão</option>
                </select>
            </div>
            <div>
                <label for="codigorastreio">Codigo de Rastreamento:</label>
                <input type="text" id="codigorastreio" name="codigorastreio" v-model="codigo_rastreamento" required>
            </div>
            <button type="submit" @click="CadastrosVeiculos.addVeiculo(id++, nome, tipo, codigo_rastreamento)">Cadastrar</button>
        </form>
    </div>
</template>

<script>
import CadastrosVeiculos from '../../scripts/telas/veiculos/CadastrosVeiculos';

export default {
    data() {
        return {
            CadastrosVeiculos,
            id: 0,
            nome: '',
            tipo: '',
            codigo_rastreamento: ''
        }
    }
}
</script>