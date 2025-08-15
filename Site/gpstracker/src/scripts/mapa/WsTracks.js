import Home from "../telas/home/Home";
import CadastrosVeiculos from "../telas/veiculos/CadastrosVeiculos";
import { formatDate } from "../utils"; 

const wsUrl = "ws://localhost:12344";

class WsTracks {
    static ws = null;

    static stop() {
        console.log("Parando WebSocket");
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }

    static setupSrv() {
        console.log("Iniciando WebSocket");
        if (this.ws) {
            this.ws.close();
            return;
        }

        this.ws = new WebSocket(wsUrl);
        this.ws.onopen = () => this.wsOnOpen();
        this.ws.onclose = () => this.wsOnClose();
        this.ws.onmessage = (event) => this.wsOnMessage(event);
    }

    static wsOnOpen() {
        console.log("WebSocket conectado");
        this.ws.send("ident:test");
    }

    static wsOnClose() {
        console.log("WebSocket desconectado");
    }

    static tmp = 0;
    static lats = 1;
    static lngs = 1;
    static wsOnMessage(event) {
        console.log("Mensagem recebida:", event.data);
        
        //mock
        if (event.data.startsWith("Nova localização de arduino001")) {
            const id= this.tmp++;
            const lat= 10 + this.lats * Math.random();
            const lng= this.lngs * Math.random() + (-this.lngs) * Math.random();
            const data= formatDate(new Date(), 'date') + ' ' + formatDate(new Date(), 'time') + '-04';

            console.log(`Nova localização recebida: ${lat}, ${lng}`);

            CadastrosVeiculos.veiculos.forEach(veiculo => {
                if (veiculo.codigo_rastreamento === "arduino001") {
                    veiculo.rastreios.push({ id, lat, lng, data });
                }
            });
            
            Home.veiculo.r_atualizar();
        }

    }

    static watchVeiculo(codigo) {
        if (this.ws) {
            this.ws.send(`va:${codigo}`);
        }
    }

}

export default WsTracks;
