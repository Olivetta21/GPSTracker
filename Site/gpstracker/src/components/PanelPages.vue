<template>
    <div id="home-page">
        <div id="content-panel">
            <div @click="contpanel = !contpanel" id="toggle-panel" :class="['button-a', { closed: !contpanel }]">
                <p> &lt; </p>
            </div>
            <div v-if="contpanel" id="content"> 
                <div id="content-header">
                    <p>usuario</p>
                </div>
                <div>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                        <li>Item 3</li>
                    </ul>
                </div>
            </div>
        </div>
        <div id="pagina">
            <router-view/>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            contpanel: true,
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
</style>

<style scoped>
#home-page {
    width: 100vw;
    height: 100vh;

    display: flex;
    flex-direction: row;
}

#content-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

#content-panel {
    background-color: #f0f0f0;
    display: flex;
    flex-direction: row-reverse;
}

#content {
    width: 300px;
    height: auto;
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
    #content-panel {
        flex-direction: column;
    }

    #content {
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