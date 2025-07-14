import { ref } from "vue";
import Janela from "../Janela";
import Veiculo from "./Veiculo";


class CadastrosVeiculos extends Janela {
    static beforeOpen() {
        console.log("abrir cadastros de veículos.");
    }
    static afterOpen() {
        console.log("cadastros de veículos aberta.");
    }
    static beforeClose() {
        console.log("fechar cadastros de veículos.");
    }
    static afterClose() {
        console.log("cadastros de veículos fechada.");
    }


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

    static tmpid = 0;
    static newTest() {
        this.addVeiculo(this.tmpid++, "Carro A" + this.tmpid, "Carro", "123456");
    }
}

export default CadastrosVeiculos;
