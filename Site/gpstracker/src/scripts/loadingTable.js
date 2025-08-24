import { ref } from "vue"

export default class LoadingTable {
    static TABLE_ = ref({
        'editUser': 0,
        'editTracker': 0,
        'trackersList': 0
    });
    static get T() { return this.TABLE_.value }

    static start(loading) {
        if (loading in this.T) {
            this.T[loading]++;
        } else {
            throw new Error('Loading não encontrado');
        }
    }

    static stop(loading) {
        if (loading in this.T) {
            if (this.T[loading] <= 0) throw new Error('Um loading nunca deveria ser negativo');
            this.T[loading]--;
        } else {
            throw new Error('Loading não encontrado');
        }
    }
}
