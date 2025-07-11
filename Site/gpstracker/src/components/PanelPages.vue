<template>
    <div id="home-page">
        <div v-if="contpanel" id="content-panel"> 
            <div id="content-header">
                <span @click="contpanel = !contpanel" class="button-a toggle-panel"> &lt; </span>
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
        <div v-else id="content-panel" class="closed">
            <p @click="contpanel = !contpanel" class="button-a toggle-panel"> &gt; </p>
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
    width: 300px;
    height: auto;
    background-color: #f0f0f0;
    padding: 20px;

    display: flex;
    flex-direction: column;
}
#content-panel.closed {
    padding: 5px;
    width: 25px;
    align-items: center;
    justify-content: center;
}


#pagina {
    flex: 1;
}



@media (max-width: 600px) {
    #home-page {
        flex-direction: column-reverse;
    }
    #content-panel {
        width: auto;
        height: 300px;
    }
    #content-panel.closed {
        width: auto;
        height: 25px;
    }
    .toggle-panel {
        transform: rotate(-90deg);
    }
}   
</style>