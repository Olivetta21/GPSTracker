<template>
    <div id="cadastrosveiculos">
        <button class="button-b" @click="$router.push({ name: 'criar-veiculo' })"> + NOVO </button>
        <div v-for="v in CadastrosVeiculos.veiculos" :key="v.id">
            <p>id: {{ v.id }}</p>
            <p>Nome: {{ v.nome }}</p>
            <p>Tipo: {{ v.tipo }}</p>
            <p @click="v.addTesteR()">Código de Rastreamento: {{ v.codigo_rastreamento }}</p>
            <div>
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