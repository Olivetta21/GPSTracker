//class Rastreio {
//    id;
//    lat;
//    lng;
//    data;
//}
let tmp = 0;
class Veiculo {
    id;
    nome;
    tipo;
    codigo_rastreamento;
    rastreios = [];

    addTesteR() {
        this.rastreios.push({
            id: tmp++,
            lat: 2,
            lng: 3,
            data: '2025-07-'+tmp
        })
    }
}

export default Veiculo;