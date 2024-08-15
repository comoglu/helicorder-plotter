document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    fetch('station_data.json')
        .then(response => response.json())
        .then(stations => {
            stations.forEach(station => {
                const marker = L.marker([station.latitude, station.longitude]).addTo(map);
                const popupContent = `
                    <strong>${station.id}</strong><br>
                    Network: ${station.network}<br>
                    Station: ${station.station}<br>
                    <a href="${station.id}.html" target="_blank">View Helicorder</a>
                `;
                marker.bindPopup(popupContent);
            });
            
            if (stations.length > 0) {
                const bounds = L.latLngBounds(stations.map(s => [s.latitude, s.longitude]));
                map.fitBounds(bounds);
            }
        });
});
