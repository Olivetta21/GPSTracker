import { ref } from "vue";

class TrackersRegister {
    static Adding_ = ref({
        token: '',
        tokenFound: false,
        dono: '',
        nome: '',
        senha: '',
    });

    static get Adding() {
        return this.Adding_.value
    }

}

export default TrackersRegister;