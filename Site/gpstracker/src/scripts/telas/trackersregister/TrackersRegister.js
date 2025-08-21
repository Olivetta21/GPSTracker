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
    static Adding_ = ref({
        token: '',
        tokenFound: false,
        owner: '',
        name: '',
        password: '',
    });
    static get Adding() {return this.Adding_.value}


    static trackers_ = ref([]);
    static get trackers() { return this.trackers_.value }

    static addTracker(tracker) {
        this.trackers_.value.push(tracker);
    }


    static testAddTracker() {
        const tracker = new Tracker(
            1,
            'active',
            'Tracker 1',
            'AB',
            [new User(1, 'User 1', 'active')],
            [new Track(1, '2023-01-01', 12.34, 56.78)]
        );
        this.addTracker(tracker);
    }

}

export default TrackersRegister;