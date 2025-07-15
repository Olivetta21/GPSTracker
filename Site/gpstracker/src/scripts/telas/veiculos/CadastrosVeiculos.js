import { ref } from "vue";
import Janela from "../Janela";
import Veiculo from "./Veiculo";


class CadastrosVeiculos extends Janela {
    static _veiculos = ref([]);
    static get veiculos() {return this._veiculos.value;}

    static addVeiculo(id, nome, tipo, codigo_rastreamento) {
        const veiculo = new Veiculo();
        veiculo.id = id;
        veiculo.nome = nome;
        veiculo.tipo = tipo;
        veiculo.codigo_rastreamento = codigo_rastreamento;
        veiculo.rastreios = [];
        this.veiculos.push(veiculo);
    }

}

export default CadastrosVeiculos;
