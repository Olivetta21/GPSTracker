<template>
    <div id="cadastrosveiculos">
        <button class="button-b" @click="$router.push({ name: 'criar-veiculo' })"> + NOVO </button>
        <div v-for="v in CadastrosVeiculos.veiculos" :key="v.id" id="lista-veiculos">
            <div id="veiculo-info">
                <p id="live-id">id: {{ v.id }}</p>
                <p id="live-nome">Nome: {{ v.nome }}</p>
                <p id="live-tipo">Tipo: {{ v.tipo }}</p>
                <p id="live-codigo" @click="v.addTesteR()">Código de Rastreamento: {{ v.codigo_rastreamento }}</p>
            </div>
            <div id="veiculo-rastreios">
                <p v-for="r in v.rastreios" :key="r.id">Rastreio: {{ r.id }}, {{ r.lat }}, {{ r.lng }}, {{ r.data }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import CadastrosVeiculos from '../../scripts/telas/veiculos/CadastrosVeiculos';

export default {
    data() {
        return {
            CadastrosVeiculos
        }
    }
}

</script>

<style>
#lista-veiculos {
    border: 1px solid var(--border-color-a);
    border-radius: 5px;
    padding: 5px;
    margin-bottom: 5px;
}
#veiculo-info {
    display: flex;
    flex-direction: row;
    gap: 5px;
}
#veiculo-rastreios {
    display: flex;
    flex-direction: column;
    gap: 5px;

    padding-left: 10px;
}
</style>