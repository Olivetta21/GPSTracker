//class Rastreio {
//    id;
//    lat;
//    lng;
//    data;

import { formatDate } from "../../../scripts/utils";

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
            data: formatDate(new Date(), 'date') + ' ' + formatDate(new Date(), 'time') + '-04'
        })
    }

    addTesteR2() {
        let lat_lng = [
            {lat: -22.243168, lng: -54.807837},
            {lat: -22.243157, lng: -54.807713},
            {lat: -22.243134, lng: -54.807509},
            {lat: -22.243113, lng: -54.807306},
            {lat: -22.243008, lng: -54.806273},
            {lat: -22.243084, lng: -54.806162},
            {lat: -22.243624, lng: -54.806096},
            {lat: -22.243745, lng: -54.806184},
            {lat: -22.243902, lng: -54.807671},
            {lat: -22.243846, lng: -54.807767},
            {lat: -22.243599, lng: -54.807810},
            {lat: -22.243471, lng: -54.807418},
            {lat: -22.243647, lng: -54.807391},
            {lat: -22.243537, lng: -54.806280},
            {lat: -22.243364, lng: -54.806309},
            {lat: -22.243493, lng: -54.807152},
            {lat: -22.243313, lng: -54.807158},
            {lat: -22.243372, lng: -54.807826},
            {lat: -22.243210, lng: -54.807853}
        ]

        lat_lng.forEach(coord => {
            this.rastreios.push({
                id: tmp++,
                lat: coord.lat,
                lng: coord.lng,
                data: formatDate(new Date(), 'date') + ' ' + formatDate(new Date(), 'time') + '-04'
            })
        })
    }
}

export default Veiculo;