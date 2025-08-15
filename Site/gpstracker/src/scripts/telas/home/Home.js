import { ref } from "vue";
import Janela from "../Janela";
import CadastrosVeiculos from "../veiculos/CadastrosVeiculos";
import Gmaps from "@/scripts/mapa/Gmaps";
import WsTracks from "@/scripts/mapa/WsTracks";
import { formatDate } from "@/scripts/utils";

class Home extends Janela {



    static _veiculo = ref({
        
        selected: null,
        r_idx_act: null,
        r_dateIn: null,
        r_dateFi: null,

        get() {
            return CadastrosVeiculos.veiculos;
        },
        pick() {
            if (this.selected >= 0 && this.selected < this.get().length) {
                return this.get()[this.selected];
            }
            return null;
        },

        r_get() {
            let rastreios = this.pick()?.rastreios || [];
            if (rastreios.length > 0) {
                rastreios = rastreios.filter(r => new Date(formatDate(r.data, 'date')) >= new Date(this.r_dateIn) && new Date(formatDate(r.data, 'date')) <= new Date(this.r_dateFi));
            }
            return rastreios;
        },

        r_initTrack() {
            Gmaps.initTrack(this.r_get());
        },

        r_centerMap() {
            let rastreio = this.r_get()[this.r_idx_act];
            if (rastreio) {
                Gmaps.setCenter(rastreio.lat, rastreio.lng);
            } else {
                console.error("No rastreio found to center map on");
            }
        },

        r_next() {
            if (this.r_idx_act+1 < this.r_get().length) {
                this.r_idx_act++;
                this.r_centerMap();
            }
        },

        r_back() {
            if (this.r_idx_act-1 >= 0 && this.r_get().length > 0) {
                this.r_idx_act--;
                this.r_centerMap();
            }
        },

        r_atualizar() {
            this.r_idx_act = null;
            Gmaps.clearTrack();

            let tmp = this.r_get();
            if (tmp && tmp.length > 0) {
                this.r_idx_act = tmp.length - 1;                
                this.r_centerMap();
                this.r_initTrack();
            }
        },

        r_getID() {
            return this.r_idx_act !== null ? this.r_get()[this.r_idx_act]?.id : null;
        },

        r_getData() {
            return this.r_idx_act !== null ? this.r_get()[this.r_idx_act]?.data : null;
        },


        ws_watchVeh() {
            const codigo = this.pick()?.codigo_rastreamento;
            if (codigo) {
                WsTracks.watchVeiculo(codigo);
            }
        }

    })

    static get veiculo() {return this._veiculo.value;}
}

export default Home;