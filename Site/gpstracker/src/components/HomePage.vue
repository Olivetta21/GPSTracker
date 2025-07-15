<template>
    <div id="map-chart">
        <div id="google-map"></div>
        <div id="map-floating-top" :class="{ closed: !mfltop }">
            <div id="map-cont" class="panels-shadow">
                <template v-if="mfltop">
                    <span class="button-a" @click="mfltop = !mfltop"> &#10799; </span>
                    <select v-if="Home.veiculo.get().length > 0" v-model="Home.veiculo.selected" @change="Home.veiculo.r_atualizar()">
                        <option v-for="(v, index) in Home.veiculo.get()" :key="v.id" :value="index">{{ v.nome }}</option>
                    </select>
                    <span v-else class="button-b" @click="$router.push({ name: 'criar-veiculo' })"> + Adicionar Veículo </span>
                    <template v-if="Home.veiculo.r_idx_act !== null">
                        <p> {{ Home.veiculo.r_getID() }}</p>
                        <span class="button-a" @click="Home.veiculo.r_back()"> &lt; </span>
                        <span class="button-a" @click="Home.veiculo.r_atualizar()"> &bull; </span>
                        <span class="button-a" @click="Home.veiculo.r_next()"> &gt; </span>
                        <p> {{ Home.veiculo.r_getData() }} </p>
                        <p @click="Home.veiculo.r_initTrack()"> track </p>
                    </template>
                    <p v-else @click="Home.veiculo.r_atualizar()"> Sem rastreios. </p>
                </template>
                <template v-else>
                    <span class="button-a" @click="mfltop = !mfltop"> &lt; </span>
                </template>
            </div>
        </div>
    </div>
</template>


<script>
import Gmaps from '@/scripts/mapa/Gmaps';
import Home from '../scripts/telas/home/Home';
import CadastrosVeiculos from '../scripts/telas/veiculos/CadastrosVeiculos';



export default {
    data() {
        return {
            CadastrosVeiculos,
            Home,


            mfltop: true,
        };
    },
    mounted() {
        Gmaps.init(document.getElementById("google-map"));
    }

    //
    //mounted() {
    //    const map = new google.maps.Map(document.getElementById("google-map"), {
    //        center: { lat: -23.5505, lng: -46.6333 },
    //        zoom: 8,
    //    });
    //    
    //    console.log(map);
    //},

};
</script>


<style scoped>

#map-chart {
    width: 100%;
    height: 100%;
    position: relative;
}
#google-map {
    background-color: burlywood;
    width: 100%;
    height: 100%;
}
#map-floating-top {
    pointer-events: none;

    position: absolute;
    top: 25px;
    left: 0;
    width: 100%;
    
    display: flex;
    justify-content: center;
}
#map-floating-top.closed {    
    justify-content: flex-end;
}
#map-cont {    
    pointer-events: visible;
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
    
    border-radius: 8px;
    background-color: white;

    gap: 10px;
    padding: 10px;
}



</style>