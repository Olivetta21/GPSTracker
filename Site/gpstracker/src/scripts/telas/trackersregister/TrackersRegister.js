import { ref } from "vue";


export class User{
    constructor(id, name, state){
        this.id = id;
        this.name = name;
        this.state = state;
    }
}
export class Track {
    constructor(id, date, lat_, lng_) {
        this.id = id;
        this.date = date;
        this.pos = {lat: lat_, lng: lng_}
    }
}
export class Tracker{
    constructor(id, state, name, token, users, tracks) {
        this.id = id;
        this.state = state;
        this.name = name;
        this.token = token;
        this.users = users;
        this.tracks = tracks;
    }
}

class TrackersRegister {
    static trackers_ = ref([]);
    static get trackers() { return this.trackers_.value }


    static delTracker(idx, id) {
        if (this.trackers[idx].id === id) {
            this.trackers.splice(idx, 1);
        }
    }
}



TrackersRegister.AddTracker = class {

    static cfg_ = ref({
        state: false,
        token: '',
        tokenFound: false,
        owner: '',
        name: '',
        password: '',
    });
    static get cfg() {return this.cfg_.value}

    static start() {
        this.stop();
        this.cfg.state = true;
    }

    static stop() {
        this.cfg.state = false;
        this.cfg.token = '';
        this.cfg.tokenFound = false;
        this.cfg.owner = '';
        this.cfg.name = '';
        this.cfg.password = '';
    }

    static find() {
        //mock
        this.cfg.tokenFound = true;
        this.cfg.owner = '';
    }

    static tmpSerial = 0;
    static confirm() {
        //mock
        const tracker = new Tracker(
            this.tmpSerial++,
            'g',
            this.cfg.name,
            this.cfg.token,
            [],
            []
        );
        TrackersRegister.trackers.push(tracker);
        this.stop();
    }

}


TrackersRegister.EditUser = class {
    static cfg_ = ref({
        state: false,
        trackerIdx: null,
        users: []
    });
    static get cfg() { return this.cfg_.value }

    static start(idx, id) {
        if (TrackersRegister.trackers[idx].id != id) return;
        this.cfg.state = true;
        this.cfg.trackerIdx = idx;
        this.cfg.users = TrackersRegister.trackers[idx].users;
    }

    static stop() {
        this.cfg.state = false;
        this.cfg.trackerIdx = null;
        this.cfg.users = [];
    }

    static deleteUser(idx, id) {
        if (this.cfg.users[idx].id != id) return;
        TrackersRegister.trackers[this.cfg.trackerIdx].users.splice(idx, 1);
    }

    static tmpSerial = 0;
    static mockUser(idx, id) {
        if (TrackersRegister.trackers[idx].id != id) return;
        const user = new User(this.tmpSerial++, 'mock user', 'g');
        TrackersRegister.trackers[idx].users.push(user);
    }
}



export default TrackersRegister;