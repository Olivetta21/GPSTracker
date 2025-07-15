import { ref } from "vue";
import Janela from "../Janela";
import CadastrosVeiculos from "../veiculos/CadastrosVeiculos";
import Gmaps from "@/scripts/mapa/Gmaps";

class Home extends Janela {



    static _veiculo = ref({
        
        selected: null,
        r_idx_act: null,

        get() {
            return CadastrosVeiculos.veiculos;
        },
        pick() {
            if (this.selected >= 0 && this.selected < this.get().length) {
                return this.get()[this.selected];
            }
            return null;
        },
        
        r_initTrack() {
            Gmaps.initTrack(this.pick()?.rastreios || []);
        },

        r_centerMap() {
            let rastreio = this.pick()?.rastreios?.[this.r_idx_act];
            if (rastreio) {
                Gmaps.setCenter(rastreio.lat, rastreio.lng);
            } else {
                console.error("No rastreio found to center map on");
            }
        },

        r_next() {
            if (this.r_idx_act+1 < this.pick()?.rastreios?.length) {
                this.r_idx_act++;
                this.r_centerMap();
            }
        },

        r_back() {
            if (this.r_idx_act-1 >= 0 && this.pick()?.rastreios?.length > 0) {
                this.r_idx_act--;
                this.r_centerMap();
            }
        },

        r_atualizar() {
            this.r_idx_act = null;

            let tmp = this.pick();
            if (tmp !== null) {
                if (tmp.rastreios.length > 0) {
                    this.r_idx_act = tmp.rastreios.length - 1;
                }
                this.r_centerMap();
            }
        },

        r_getID() {
            return this.r_idx_act !== null ? this.pick()?.rastreios[this.r_idx_act]?.id : null;
        },

        r_getData() {
            return this.r_idx_act !== null ? this.pick()?.rastreios[this.r_idx_act]?.data : null;
        },

    })

    static get veiculo() {return this._veiculo.value;}
}

export default Home;