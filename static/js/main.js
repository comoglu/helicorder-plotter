document.addEventListener('DOMContentLoaded', function() {
    var mapEl = document.getElementById('map');
    if (!mapEl) return;

    var map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    fetch('station_data.json')
        .then(function(response) { return response.json(); })
        .then(function(stations) {
            stations.forEach(function(station) {
                var marker = L.marker([station.latitude, station.longitude]).addTo(map);
                var popupContent =
                    '<strong>' + station.id + '</strong><br>' +
                    'Network: ' + station.network + '<br>' +
                    'Station: ' + station.station + '<br>' +
                    '<a href="' + station.id + '.html" target="_blank">View Helicorder</a>';
                marker.bindPopup(popupContent);
            });

            if (stations.length > 0) {
                var bounds = L.latLngBounds(stations.map(function(s) {
                    return [s.latitude, s.longitude];
                }));
                map.fitBounds(bounds);
            }
        })
        .catch(function(error) {
            console.error('Error loading station data:', error);
        });
});
