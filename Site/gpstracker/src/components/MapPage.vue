<template>
    <div id="map-page">
        <div id="google-map"></div>
        <div id="map-content">
            <div v-if="isTracking" id="rastr-tracking" class="rastr">
                <div id="track-info">
                    <input type="date">
                    <input type="date">
                    <p> Rastr 1 </p>
                    <div id="tracks-change">
                        <p>&leftarrow;</p>
                        <p>&dot;</p>
                        <p>&rightarrow;</p>
                    </div>
                </div>
                <div id="track-list">
                    <table>
                        <tbody>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                            <tr>
                                <td>2025-01-01</td>
                                <td>Rastr 1</td>
                                <td>Rastr 2</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-else id="rastr-select" class="rastr">
                <p> Rastr 1 </p>
                <p> Rastr 1 </p>
                <p> Rastr 1 </p>
                <p> Rastr 1 </p>
            </div>
        </div>
    </div>
</template>


<script>
import { formatDate } from '../scripts/utils';
import Gmaps from '../scripts/mapa/Gmaps';
import WsTracks from '../scripts/mapa/WsTracks';
import Home from '../scripts/telas/home/Home';


export default {
    data() {
        return {
            Home,
            formatDate,

            isTracking: true,
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

</style>