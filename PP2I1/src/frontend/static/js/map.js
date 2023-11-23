/*L is a shortcut for Leaflet*/

const corner1 = L.latLng(-90, -180)
const corner2 = L.latLng(90, 180);
const bounds = L.latLngBounds(corner1, corner2);

var map = L.map('map',{minZoom: 2,maxBounds : bounds,maxBoundsViscosity: 1.0}).setView([51.505, -0.09],2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


var bin_entries = document.getElementsByClassName("bin-entry");
for (var i = 0; i < bin_entries.length; i++) {
    bin_entries[i].addEventListener("click", function() {
        this.children[0].classList.toggle("active");
        let lat = this.getAttribute("data-lat");
        let long = this.getAttribute("data-long");
        console.log(lat, long);
        map.setView([lat, long], 8);
    });
    
}