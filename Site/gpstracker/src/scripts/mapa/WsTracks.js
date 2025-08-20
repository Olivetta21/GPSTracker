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
    static wsOnMessage(event) {
        let msg = null;
        try {
            msg = JSON.parse(event.data);
        } catch {
            console.error("Erro ao processar mensagem WebSocket:", event.data);
            return;
        }
        
        console.log("WS message received:", msg);
        switch (msg.t) {
            case "loc":{
                const id = this.tmp++;
                const lat = msg.lat;
                const lng = msg.lng;
                const data = formatDate(new Date(), 'date') + ' ' + formatDate(new Date(), 'time') + '-04';

                CadastrosVeiculos.veiculos.forEach(veiculo => {
                    if (veiculo.codigo_rastreamento === msg.tk) {
                        veiculo.rastreios.push({ id, lat, lng, data });
                    }
                });
                
                Home.veiculo.r_atualizar();
            }
        }
    }

    static watchVeiculo(codigo, adding) {
        if (this.ws) {
            this.ws.send(`${adding ? 'wva' : 'wvr'}:${codigo}`);
        }
    }

    static watchVeiculoUnique(codigo) {
        if (this.ws) {
            this.ws.send(`wvu:${codigo}`);
        }
    }

}

export default WsTracks;
