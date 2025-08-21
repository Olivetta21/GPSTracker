<template>
    <div id="map-page">
        <div id="google-map"></div>
        <div id="map-content">
            <div v-if="MT.tConfig.idx >= 0" id="rastr-tracking" class="rastr">
                <div id="track-info">
                    <button @click="MT.updateTrail()">Test</button>
                    <input type="date" v-model="MT.tConfig.dateIn" @change="MT.updateTrail()">
                    <input type="date" v-model="MT.tConfig.dateFi" @change="MT.updateTrail()">
                    <p @click="MT.clearTracker()">{{ MT.tracker.name }}</p>
                    <div id="tracks-change">
                        <button @click="MT.prevTrailPoint()">&leftarrow;</button>
                        <button @click="MT.lastTrailPoint()">&dot;</button>
                        <button @click="MT.nextTrailPoint()">&rightarrow;</button>
                    </div>
                </div>
                <div id="track-list">
                    <table>
                        <tbody>
                            <tr v-for="(t, idx) in MT.tracker.tracksFiltered" :key="idx" :class="['track-item', { 'active': MT.tConfig.trackIdx === idx }]" @click="MT.setTrailPoint(idx)">
                                <td>{{ t.date }}</td>
                                <td>{{ t.pos.lat }}</td>
                                <td>{{ t.pos.lng }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-else id="rastr-select" class="rastr">
                <p v-for="(t, idx) in TR.trackers" :key="idx" @click="MT.setTracker(idx, t.id)"> {{ t.name }}</p>
            </div>
        </div>
    </div>
</template>


<script>
import TrackersRegister from '../scripts/telas/trackersregister/TrackersRegister';
import Gmaps from '../scripts/mapa/Gmaps';
import WsTracks from '../scripts/mapa/WsTracks';
import MapTrackers from '../scripts/telas/map/MapTrackers';


export default {
    data() {
        return {
            MT: MapTrackers,
            TR: TrackersRegister
        };
    },
    mounted() {
        Gmaps.init(document.getElementById("google-map"));
        WsTracks.setupSrv();
    },
    beforeUnmount() {
        WsTracks.stop();
    },
};
</script>


<style scoped>

#map-page {
    width: 100%;
    height: 100%;
    position: relative;
}
#google-map {
    background-color: burlywood;
    width: 100%;
    height: 100%;
}

#map-content {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    display: flex;
    align-items: center;
    flex-direction: column-reverse;
    padding: 10px;
}


.rastr {
    border: 1px solid var(--border-color-a);
    background-color: white;
    width: 90%;
    height: 25%;
    pointer-events: all;
}

#rastr-select>p {
    border: 1px solid var(--border-color-a);
    background-color: white;
    padding: 5px;
}


#rastr-tracking {
    display: flex;
    flex-direction: row;
}

#track-info {
    display: flex;
    flex-direction: column;
}
#tracks-change {
    display: flex;
    flex-direction: row;
    align-items: center;
}


#track-list {    
    flex: 1;
    width: 0;
    overflow: auto;
}

#track-list>table {
    width: 100%;
}
#track-list>table>tbody>tr:hover {
    background-color: rgb(177, 177, 177);
}

.track-item.active {
    background-color: rgb(49, 49, 49);
    color: white;
}

</style>