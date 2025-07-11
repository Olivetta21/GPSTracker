<template>
    <div id="home-page">
        <div id="content-panel"> 
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
            <button> test </button>
        </div>
        <div id="map-chart">
            <div id="google-map"></div>
            <div id="map-floating-top">
                <div id="map-cont">
                    <button> back </button>    
                    <button> next </button>
                    <button> zoom in </button>
                    <button> zoom out </button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>


export default {
    name: 'HomePage',

    ///* global google */
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
#home-page {
    width: 100vw;
    height: 100vh;

    display: flex;
    flex-direction: row;
}
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
    position: absolute;
    top: 5px;
    left: 0;
    width: 100%;
    
    display: flex;
    justify-content: center;
}
#map-cont {
    display: flex;
    justify-content: space-around;
    
    border-radius: 5px;
    background-color: white;

    gap: 5px;
    padding: 5px;
}
#content-panel {
    background-color: #f0f0f0;
    padding: 20px;
}
</style>