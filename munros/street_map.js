markers = []

window.onload = function(event) {
    init()
};

icon_colors = ["green", "blue", "red", "orange", "black", "violet"]
rotations = [0, 35, 70]

// Create a dictionary of icons for all combinations of colors and rotations
const icons = {};
for (const color of icon_colors) {
    icons[color] = {};
    for (const rotation of rotations) {
        icons[color][rotation] = new L.Icon({
            iconUrl: `rotated_markers/marker-icon-${color}-r${rotation}.png`,
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: rotation === 0 ? [25, 41] : rotation === 35 ? [45, 49] : [48, 39],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });
    }
}

bicycle = new L.Icon({
    iconUrl: `bicycle.png`,
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [60, 60],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

function annotate_data(fdata) {
    const easy = new Set(
        fdata
            .filter(v => v["Effort"] < 5 && v["Terrain"] < 5)
            .map(v => v["id"])
    );

    const hard_effort_and_terrain = new Set(
        fdata
            .filter(v => v["Effort"] > 5 && v["Terrain"] > 5)
            .map(v => v["id"])
    );

    const hard_effort_only = new Set(
        fdata
            .filter(v => v["Effort"] > 5 && v["Terrain"] <= 5)
            .map(v => v["id"])
    );

    const hard_terrain_only = new Set(
        fdata
            .filter(v => v["Terrain"] > 5 && v["Effort"] <= 5)
            .map(v => v["id"])
    );

    const medium = new Set(
        fdata
            .filter(v =>
                !easy.has(v["id"]) &&
                !hard_effort_and_terrain.has(v["id"]) &&
                !hard_effort_only.has(v["id"]) &&
                !hard_terrain_only.has(v["id"]))
            .map(v => v["id"])
    );


    return {
        easy,
        hard_effort_and_terrain,
        hard_effort_only,
        hard_terrain_only,
        medium
    };
}

function add_marker(munro, map, seen, oms) {
    lat_lon_str = munro.lat_lon.toString()
    let marker;

    // Set color based on category
    let color;
    switch(munro.category) {
        case 'easy':
            color = 'green';
            break;
        case 'medium':
            color = 'blue';
            break;
        case 'hard_effort_and_terrain':
            color = 'violet';
            break;
        case 'hard_effort_only':
            color = 'orange';
            break;
        case 'hard_terrain_only':
            color = 'black';
            break;
    }

    if ("Bike time" in munro) {
        marker = new L.marker(munro.lat_lon, {icon: bicycle});
    }
    else if (seen.has(lat_lon_str + "again")) {
        console.log("seen again")
        seen.add(lat_lon_str + "againagain")
        marker = new L.marker(munro.lat_lon, {icon: icons[color][70]});  // Using 80 degree rotation
    }
    else if (seen.has(lat_lon_str)) {
        console.log("seen")
        seen.add(lat_lon_str + "again")
        marker = new L.marker(munro.lat_lon, {icon: icons[color][35]});  // Using 40 degree rotation
    } else {
        seen.add(lat_lon_str)
        marker = new L.marker(munro.lat_lon, {icon: icons[color][0]});  // Using default 0 degree rotation
    }

    marker.data = munro
    marker.addTo(map);
    markers.push(marker);
    oms.addMarker(marker);
}

function init_json(munro_json, map, oms) {
    markers = []
    seen = new Set()
    window.seen = seen
    console.log(`There are ${munro_json.length} routes`)

    // Add categorization
    const categories = annotate_data(munro_json);
    window.categories = categories;

    // Add category field to each munro object
    for (const munro of munro_json) {
        if (categories.easy.has(munro.id)) {
            munro.category = 'easy';
        } else if (categories.hard_effort_and_terrain.has(munro.id)) {
            munro.category = 'hard_effort_and_terrain';
        } else if (categories.hard_effort_only.has(munro.id)) {
            munro.category = 'hard_effort_only';
        } else if (categories.hard_terrain_only.has(munro.id)) {
            munro.category = 'hard_terrain_only';
        } else if (categories.medium.has(munro.id)) {
            munro.category = 'medium';
        }

        if ("lat_lon" in munro) {
            add_marker(munro, map, seen, oms);
        }
        else {
            console.log(`no lat long for ${munro}`)
        }
    }
    //gr = L.featureGroup(markers)
    //var group = gr.addTo(map);
    //map.fitBounds(group.getBounds());
}

function init() {
    var map = L.map('map').setView([56.841, -5.043], 7);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    var oms = new OverlappingMarkerSpiderfier(map, {keepSpiderfied: true, circleFootSeparation: 60});

    // Check URL parameters for corbetts
    const urlParams = new URLSearchParams(window.location.search);
    const corbetts_only = urlParams.has('corbetts')

    fetch("fallon_data.json")
        .then((response) => response.json())
        .then((routes_json) => init_json(routes_json, map, oms));

    var popup = new L.Popup();

    oms.addListener('click', function(marker) {
        data = marker.data
        url = `https://www.stevenfallon.co.uk/${data.file}`;
        let content = `<a href="${url}" target="_blank">View on stevenfallon.co.uk</a>`;

        if (data.Munros) {
            content += '<br><br>Munros:<br>' +
                            data.Munros.join('<br>');
        }
        if (data.Corbetts) {
            content += '<br><br>Corbetts:<br>' + data.Corbetts.join('<br>');
        }

        popup.setContent(content);
        popup.setLatLng(marker.getLatLng());
        map.openPopup(popup);
    });
}

// function test() {
//     for (marker in markers) {
//         if marker.di
//     }
// }