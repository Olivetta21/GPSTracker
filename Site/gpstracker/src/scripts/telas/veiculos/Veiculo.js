//class Rastreio {
//    id;
//    lat;
//    lng;
//    data;
//}
let tmp = 0;
let lats = 1;
let lngs = 1;
class Veiculo {
    id;
    nome;
    tipo;
    codigo_rastreamento;
    rastreios = [];

    addTesteR() {
        this.rastreios.push({
            id: tmp++,
            lat: 10 + lats * Math.random(),
            lng: lngs * Math.random() + (-lngs) * Math.random(),
            data: '2025-07-'+tmp
        })
    }
}

export default Veiculo;