import { ref } from "vue";
import TrackersRegister from "../trackersregister/TrackersRegister";
import Gmaps from "../../mapa/Gmaps";
import { formatDate } from "../../utils";

class MapTrackers {
    
    static tConfig_ = ref({
        idx: -1,    // Índice do rastreador selecionado
        trackIdx: -1, // Índice do ponto selecionado da trilha
        dateIn: null,
        dateFi: null
    })
    static get tConfig() {return this.tConfig_.value}

    static tracker_ = ref({
        id: null,
        name: null,
        tracks: [],
        tracksFiltered: []
    })
    static get tracker() {return this.tracker_.value}

    static clearTracker() {
        Gmaps.clearTrack();   
        this.tConfig.idx = -1;
        this.tConfig.trackIdx = -1;
        this.tracker.id = null;
        this.tracker.name = null;
        this.tracker.tracks = [];
        this.tracker.tracksFiltered = [];
    }

    static setTracker(idx, id) {
        this.clearTracker();

        if (idx >= 0 && idx < TrackersRegister.trackers.length) {
            const refTracker = TrackersRegister.trackers[idx];            
            if (refTracker && refTracker.id == id) {
                this.tConfig.idx = idx;
                this.tConfig.trackIdx = refTracker.tracks.length - 1;

                this.tracker.id = refTracker.id;
                this.tracker.name = refTracker.name;
                this.tracker.tracks = refTracker.tracks;
            }
        }

        this.updateTrail();
    }

    static getFilteredTracks() {
        const Tracker = this.tracker;
        if (!Tracker || !Tracker.tracks) return [];
        return Tracker.tracks.filter(t => {
            const fDate = new Date(formatDate(t.date, 'date'));
            return fDate >= new Date(this.tConfig.dateIn) && fDate <= new Date(this.tConfig.dateFi);
        });        
    }

    static prevTrailPoint() {
        if (this.tConfig.trackIdx - 1 >= 0) {
            this.tConfig.trackIdx--;
            this.updateTrailPoint();
        }
    }
    static lastTrailPoint() {
        this.tConfig.trackIdx = this.tracker.tracksFiltered.length - 1;
        this.updateTrailPoint();
    }
    static nextTrailPoint() {
        if (this.tConfig.trackIdx + 1 < this.tracker.tracksFiltered.length) {
            this.tConfig.trackIdx++;
            this.updateTrailPoint();
        }
    }
    static setTrailPoint(idx) {
        this.tConfig.trackIdx = idx;
        this.updateTrailPoint();
    }

    static updateTrailPoint(onlyDraw) {
        const idx = this.tConfig.trackIdx;
        const tracks = this.tracker.tracksFiltered;
        if (idx >= 0 && idx < tracks.length) {
            const pos = tracks[idx].pos;
            if (onlyDraw) Gmaps.setMarkerPosition(pos.lat, pos.lng);
            else Gmaps.centerOn(pos.lat, pos.lng);
        }
    }

    static updateTrail() {
        const lastIdx = this.tConfig.trackIdx;

        Gmaps.clearTrack();
        this.tracker.tracksFiltered = [];
        const tracks = this.getFilteredTracks();
        if (tracks.length < 1) return;
        this.tracker.tracksFiltered = tracks;
        this.tConfig.trackIdx = tracks.length - 1;

        // Cria um vetor com as propriedades "pos" dentro de cada objeto track
        const positions = tracks.map(track => track.pos);        
        Gmaps.initTrack(positions);

        if (lastIdx >= 0 && lastIdx + 1 < this.tConfig.trackIdx) { // O usuario não esta vendo o ultimo, então não reposicione a camera
            this.tConfig.trackIdx = lastIdx;
            this.updateTrailPoint(true);
        } else {
            this.updateTrailPoint();
        }

    }
}

export default MapTrackers;