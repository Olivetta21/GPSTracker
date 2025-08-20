<template>
    <div id="panel-pages">
        <div id="panel-holder" class="panels-shadow">
            <div @click="panelVisible = !panelVisible" id="toggle-panel" :class="['button-a', { closed: !panelVisible }]">
                <p> &lt; </p>
            </div>
            <div v-if="panelVisible" id="panel"> 
                <div id="panel-header">
                    <p>usuario</p>
                </div>
                <div id="panel-buttons">
                    <span class="button-b" @click="router.push({ name: 'mapa' })"> Mapa </span>
                    <span class="button-b" @click="router.push({ name: 'cadrastreador' })"> Rastreadores </span>
                    <span class="button-b" @click="router.push({ name: 'perfiluser' })"> Perfil </span>
                </div>
            </div>
        </div>
        <div id="pagina">
            <router-view/>
        </div>
    </div>
</template>

<script>
import router from '../scripts/routes/router';
export default {
    data() {
        return {
            router: router,
            panelVisible: true,
        };
    },
}
</script>

<style>
.button-a {
    cursor: pointer;
    color: var(--border-color-a);
}
.button-a:hover {
    color: black;
}
.button-b {
    cursor: pointer;
    padding: 8px;
    border: 2px solid var(--border-color-a);
    border-radius: 5px;
}
.button-b:hover {
    background-color: var(--border-color-a);
}
.panels-shadow {
    box-shadow: 20px -20px 20px 20px #0000001a;
}
</style>

<style scoped>
#panel-pages {
    width: 100vw;
    height: 100vh;

    display: flex;
    flex-direction: row;
}

#panel {
    width: 300px;
    height: auto;
    padding: 5px;
}


#panel-holder {
    z-index: 1;
    background-color: #f0f0f0;
    display: flex;
    flex-direction: row-reverse;
}

#panel-header {
    padding: 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

#panel-buttons {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: space-evenly;
    gap: 4px;
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
    overflow: auto;
    position: relative;
}



@media (max-width: 600px) {
    
}   
</style>