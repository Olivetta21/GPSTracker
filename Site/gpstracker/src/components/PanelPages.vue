<template>
    <div id="home-page">
        <div id="panel-holder" class="panels-shadow">
            <div @click="contpanel = !contpanel" id="toggle-panel" :class="['button-a', { closed: !contpanel }]">
                <p> &lt; </p>
            </div>
            <div v-if="contpanel" id="panel"> 
                <div id="panel-header">
                    <p>usuario</p>
                </div>
                <div id="panel-content">
                    <div id="opt-buttons">
                        <span class="button-b" @click="router.push({ name: 'home' })"> Inicio </span>
                        <span class="button-b" @click="router.push({ name: 'cadveiculos' })"> Veiculos </span>
                    </div>
                    <div id="loc-registers">
                        <div>                            
                            <p>Registros de localização</p>
                            <p> {{ Home.veiculo.pick()?.nome || 'Nenhum veiculo selecionado' }} </p>
                        </div>
                        <div id="loc-date-selection">
                            <input type="date" v-model="Home.veiculo.r_dateIn" @change="Home.veiculo.r_atualizar()">
                            <p>até</p>
                            <input type="date" v-model="Home.veiculo.r_dateFi" @change="Home.veiculo.r_atualizar()">
                            <p class="button-b" @click="Home.veiculo.testDate(); console.log(Home.veiculo.r_dateIn, Home.veiculo.r_dateFi)">atualizar</p>
                        </div>
                        <div id="loc-list">
                            <p v-for="(v, idx) in Home.veiculo.r_get()" :key="idx"
                            :class="{'active': Home.veiculo.r_idx_act === idx}"
                            @click="Home.veiculo.r_idx_act = idx; Home.veiculo.r_centerMap()">
                            Hora: {{ formatDate(v.data, 'time') }}
                        </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id="pagina">
            <router-view/>
        </div>
    </div>
</template>

<script>
import Home from '../scripts/telas/home/Home';
import router from '../scripts/routes/router';
import { formatDate } from '../scripts/utils';

export default {
    data() {
        return {
            Home,
            router: router,
            contpanel: true,
            formatDate,
        };
    },
}
</script>

<style>
.button-a {
    cursor: pointer;
    color: gray;
}
.button-a:hover {
    color: black;
}
.button-b {
    cursor: pointer;
    padding: 8px;
    border: 2px solid #b3b3b3;
    border-radius: 5px;
}
.button-b:hover {
    background-color: #cccccc;
}
.panels-shadow {
    box-shadow: 20px -20px 20px 20px #0000001a;
}
</style>

<style scoped>
#home-page {
    width: 100vw;
    height: 100vh;

    display: flex;
    flex-direction: row;
}

#panel {
    width: 300px;
    height: auto;
}


#panel-holder {
    z-index: 1;
    background-color: #f0f0f0;
    display: flex;
    flex-direction: row-reverse;
}

#panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

#panel-content {
    display: flex;
    flex-direction: column;
}

#opt-buttons {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-evenly;
}

#loc-date-selection {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}
#loc-list {
    overflow: auto;
    scrollbar-width: none;
    height: 150px;
    width: 100%;
    text-wrap: nowrap;
}
#loc-list>p:hover {
    background-color: #a5a5a5;
    cursor: pointer;
}
#loc-list>p.active {
    background-color: black;
    color: white;;
}

#toggle-panel {
    padding: 5px;
    width: 25px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    border-left: 1px solid gray;
}
#toggle-panel.closed>p {
    transform: rotate(180deg);
}


#pagina {
    flex: 1;
}



@media (max-width: 600px) {
    #home-page {
        flex-direction: column-reverse;
    }
    #panel-holder {
        flex-direction: column;
    }

    #panel {
        width: auto;
        height: 300px;
    }

    #toggle-panel {
        flex-direction: row;
        width: auto;
        height: 25px;
        
        border-left: 0;
        border-bottom: 1px solid gray;
    }
    #toggle-panel>p {
        transform: rotate(-90deg);
    }
    #toggle-panel.closed>p {
        transform: rotate(90deg);
    }
}   
</style>