markers = []

window.onload = function(event) {
    init()
};

function init_json(wiggles_json, map) {
    const coordinatePairs = wiggles_json.map(wiggle => ({
        points: [
            [wiggle.start_lat, wiggle.start_lon],
            [wiggle.lat, wiggle.lon]
        ],
        color: wiggle.speed_kmh < 1 ? 'blue' : wiggle.speed_kmh > 8 ? 'red' : 'green'
    }));

    // Create polylines for each pair of coordinates with appropriate color
    coordinatePairs.forEach(pair => {
        console.log(pair)
        var polyline = L.polyline(pair.points, {color: pair.color}).addTo(map);
    });

    // Fit map bounds to include all coordinates
    if (wiggles_json.length > 0) {
        let allPoints = wiggles_json.map(w => [w.start_lat, w.start_lon]);
        let bounds = L.latLngBounds(allPoints);
        map.fitBounds(bounds);
    }
}

function init() {
    var map = L.map('map').setView([56.841, -5.043], 7);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const urlParams = new URLSearchParams(window.location.search);
    const json_file = urlParams.get('file')


    fetch(`wiggles_json/${json_file}`)
        .then((response) => response.json())
        .then((routes_json) => init_json(routes_json, map));
}

// function test() {
//     for (marker in markers) {
//         if marker.di
//     }
// }