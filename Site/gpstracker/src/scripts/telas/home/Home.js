import { ref } from "vue";
import Janela from "../Janela";
import CadastrosVeiculos from "../veiculos/CadastrosVeiculos";

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
        
        r_next() {
            if (this.r_idx_act+1 < this.pick()?.rastreios?.length) {
                this.r_idx_act++;
                console.log("Next:" + this.r_idx_act);
            }
        },

        r_back() {
            if (this.r_idx_act-1 >= 0 && this.pick()?.rastreios?.length > 0) {
                this.r_idx_act--;
                console.log("Back:" + this.r_idx_act);
            }
        },

        r_atualizar() {
            console.log("Atualizando veiculo do indice: " + this.selected);
            this.r_idx_act = null;

            let tmp = this.pick();
            if (tmp !== null) {
                if (tmp.rastreios.length > 0) {
                    this.r_idx_act = tmp.rastreios.length - 1;
                }
                console.log("Veiculo atualizado", tmp);
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