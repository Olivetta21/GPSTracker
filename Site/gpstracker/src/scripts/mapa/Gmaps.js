/* global google */

class Gmaps {
    static map = null;
    static marker = null;
    static line = null;

    static init(element) {
        if (this.map !== null) {
            element.appendChild(this.map.getDiv());
            console.log("Map already initialized");
            return;
        }
        this.map = new google.maps.Map(element, {
            zoom: 12,
            center: { lat: -34.397, lng: 150.644 },
        });
        console.log("Map initialized");
    }

    static setCenter(lat, lng) {
        if (this.map) {
            let pos = new google.maps.LatLng(lat, lng);
            this.map.panTo(pos);
            if (this.marker) {
                this.marker.setPosition(pos);
            }
        } else {
            console.error("Map not initialized");
        }
    }

    static initTrack(coords) {
        if (!coords || coords.length < 1) {
            console.error("No coordinates provided for tracking");
            return;
        }
        if (this.map === null) {
            console.error("Map not initialized. Call Gmaps.init() first.");
            return;
        }

        if (this.marker === null) {
            this.marker = new google.maps.Marker({
                position: coords[coords.length - 1],
                map: this.map,
                icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 6,
                fillColor: "#00F",
                fillOpacity: 1,
                strokeWeight: 0
                }
            });
        } else {
            this.marker.setPosition(coords[coords.length - 1]);
        }

        if (this.line === null) {
            this.line = new google.maps.Polyline({
                path: coords,
                strokeOpacity: 0,
                icons: [{
                    icon: {
                    path: 'M 0,-1 0,1',
                    strokeOpacity: 1,
                    scale: 4
                    },
                    offset: '0',
                    repeat: '10px'
                }],
                map: this.map
            });
        } else {
            this.line.setPath(coords);
        }
        
    }

    static clearTrack() {
        if (this.marker) {
            this.marker.setMap(null);
            this.marker = null;
        }
        if (this.line) {
            this.line.setMap(null);
            this.line = null;
        }
    }
}

export default Gmaps;