<template>
    <div id="map-chart">
        <div id="google-map"></div>
        <div v-if="mfltop" id="map-floating-top">
            <div id="map-cont">
                <span class="button-a" @click="mfltop = !mfltop"> &#10799; </span>
                <select>
                    <option v-for="i in 100" :key="i">Option {{ i }}</option>
                </select>
                <p> 10 </p>
                <span class="button-a"> &lt; </span>
                <span class="button-a"> &bull; </span>
                <span class="button-a"> &gt; </span>
                <p> 12:25,33 </p>
            </div>
        </div>
        <div v-else id="map-floating-top" class="closed">
            <div id="map-cont">
                <span class="button-a" @click="mfltop = !mfltop"> &lt; </span>
            </div>
        </div>
    </div>
</template>


<script>


export default {
    data() {
        return {
            mfltop: true,
        };
    },

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
    flex-wrap: wrap;
    
    border-radius: 8px;
    background-color: white;

    gap: 10px;
    padding: 10px;
}



</style>