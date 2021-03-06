//var mymap = L.map('mapid').setView([47.751307, 11.588271], 8);
/*L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoicGh1aG5ndXllbiIsImEiOiJjanY1YWk4NXIyejU2NGNqd2x6MnRpYmlpIn0.n3xBZDj-jH1QeCWxq85H8g'
}).addTo(mymap);*/
/*L.tileLayer('http://{s}.tile.stamen.com/terrain-background/{z}/{x}/{y}.png', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
}).addTo(mymap);*/

var colorCount = 256;
var names = ["Diverging", "Rainbow", "GreyRainbow", "RainbowInv", "SeisSol", "Kaikoura", "PGA", "PGV", "PGD"];
var scales = {
    [names[0]]: ['#3a4cc1', '#3c4dc1', '#3e4ec2', '#404fc2', '#4250c2', '#4451c2', '#4652c3', '#4853c3', '#4a54c3', '#4c55c3', '#4e56c4', '#4f57c4', '#5158c4', '#5359c4', '#545bc5', '#565cc5', '#585dc5', '#595ec5', '#5b5fc6', '#5c60c6', '#5e61c6', '#5f62c7', '#6163c7', '#6264c7', '#6465c7', '#6566c8', '#6767c8', '#6868c8', '#6a69c8', '#6b6bc9', '#6c6cc9', '#6e6dc9', '#6f6ec9', '#706fca', '#7270ca', '#7371ca', '#7572ca', '#7673cb', '#7774cb', '#7875cb', '#7a77cb', '#7b78cc', '#7c79cc', '#7e7acc', '#7f7bcc', '#807ccc', '#817dcd', '#837ecd', '#8480cd', '#8581cd', '#8682ce', '#8883ce', '#8984ce', '#8a85ce', '#8b86cf', '#8c87cf', '#8e89cf', '#8f8acf', '#908bd0', '#918cd0', '#928dd0', '#948ed0', '#958fd0', '#9691d1', '#9792d1', '#9893d1', '#9994d1', '#9b95d2', '#9c96d2', '#9d97d2', '#9e99d2', '#9f9ad3', '#a09bd3', '#a19cd3', '#a39dd3', '#a49ed3', '#a5a0d4', '#a6a1d4', '#a7a2d4', '#a8a3d4', '#a9a4d5', '#aba5d5', '#aca7d5', '#ada8d5', '#aea9d5', '#afaad6', '#b0abd6', '#b1acd6', '#b2aed6', '#b3afd6', '#b4b0d7', '#b6b1d7', '#b7b2d7', '#b8b4d7', '#b9b5d7', '#bab6d8', '#bbb7d8', '#bcb8d8', '#bdbad8', '#bebbd8', '#bfbcd9', '#c0bdd9', '#c1bed9', '#c3c0d9', '#c4c1d9', '#c5c2da', '#c6c3da', '#c7c4da', '#c8c6da', '#c9c7da', '#cac8db', '#cbc9db', '#cccadb', '#cdccdb', '#cecddb', '#cfcedc', '#d0cfdc', '#d1d0dc', '#d3d2dc', '#d4d3dc', '#d5d4dd', '#d6d5dd', '#d7d7dd', '#d8d8dd', '#d9d9dd', '#dadadd', '#dbdcde', '#dcddde', '#dddddc', '#dddbdb', '#dddad9', '#ddd8d8', '#ddd7d6', '#ddd5d4', '#ded4d3', '#ded3d1', '#ded1d0', '#ded0ce', '#dececc', '#decdcb', '#decbc9', '#decac8', '#dec9c6', '#dec7c5', '#dec6c3', '#dec4c1', '#dec3c0', '#ddc1be', '#ddc0bd', '#ddbfbb', '#ddbdba', '#ddbcb8', '#ddbab7', '#ddb9b5', '#ddb8b3', '#ddb6b2', '#ddb5b0', '#ddb3af', '#dcb2ad', '#dcb0ac', '#dcafaa', '#dcaea9', '#dcaca7', '#dcaba6', '#dca9a4', '#dba8a3', '#dba6a1', '#dba5a0', '#dba49e', '#dba29d', '#daa19b', '#da9f9a', '#da9e98', '#da9c97', '#d99b95', '#d99a94', '#d99892', '#d99791', '#d8958f', '#d8948e', '#d8928c', '#d8918b', '#d79089', '#d78e88', '#d78d86', '#d68b85', '#d68a83', '#d68882', '#d58780', '#d5857f', '#d5847e', '#d5837c', '#d4817b', '#d48079', '#d37e78', '#d37d76', '#d37b75', '#d27a73', '#d27872', '#d27771', '#d1756f', '#d1746e', '#d0726c', '#d0716b', '#d07069', '#cf6e68', '#cf6d67', '#ce6b65', '#ce6a64', '#cd6862', '#cd6761', '#cd6560', '#cc635e', '#cc625d', '#cb605c', '#cb5f5a', '#ca5d59', '#ca5c57', '#c95a56', '#c95955', '#c85753', '#c85552', '#c75451', '#c7524f', '#c6514e', '#c64f4d', '#c54d4b', '#c54c4a', '#c44a49', '#c44847', '#c34646', '#c34545', '#c24343', '#c14142', '#c13f41', '#c03d3f', '#c03c3e', '#bf3a3d', '#bf383b', '#be363a', '#bd3439', '#bd3238', '#bc3036', '#bc2d35', '#bb2b34', '#ba2932', '#ba2631', '#b92430', '#b9212f', '#b81e2d', '#b71b2c', '#b7182b', '#b6142a', '#b51028', '#b50a27', '#b40426'], // TODO: generate colors programmatically. Currently hard code gotten from https://gka.github.io/palettes/
    [names[1]]: ['0000ff', '00ffff', '00ff00', 'ffff00', 'ff0000'],
    [names[2]]: ['ffffff', 'ffffff', '00ffff', '00ff00', 'ffff00', 'ff0000'],
    [names[3]]: ['ff0000', 'ffff00', '00ff00', '00ffff', '0000ff'],
    [names[4]]: ['ffffff', '00ffff', '0000ff', 'ff5100', 'ff0000'],
    [names[5]]: ['ffffff', '5bbed7', 'c47757']
};
var domains = {
    [names[0]]: Array.from(Array(256).keys()).map(x => x/255),
    [names[1]]: [0, 0.25, 0.5, 0.75, 1],
    [names[2]]: [0, 0.005, 0.25, 0.5, 0.75, 1],
    [names[3]]: [0, 0.25, 0.5, 0.75, 1],
    [names[4]]: [0, 0.25, 0.5, 0.75, 1],
    [names[5]]: [0, 0.01, 1]
};
var mapName = names[0];
var colorScaleName = mapName;
var colorFunc = chroma.scale(scales[colorScaleName]);
var isMapPga = mapName.localeCompare(names[6]) == 0, isMapPgv = mapName.localeCompare(names[7]) == 0,
    isMapPgd = mapName.localeCompare(names[8]) == 0;

var baseMaps = {
    [names[0]]: L.tileLayer('http://localhost/d/{z}/{x}/{y}.png', {maxZoom: 18}),
    [names[1]]: L.tileLayer('http://localhost/r/{z}/{x}/{y}.png', {maxZoom: 18}),
    [names[2]]: L.tileLayer('http://localhost/gr/{z}/{x}/{y}.png', {maxZoom: 18}),
    [names[3]]: L.tileLayer('http://localhost/ri/{z}/{x}/{y}.png', {maxZoom: 18}),
    [names[4]]: L.tileLayer('http://localhost/ss/{z}/{x}/{y}.png', {maxZoom: 18}),
    [names[5]]: L.tileLayer('http://localhost/k/{z}/{x}/{y}.png', {maxZoom: 18}),
    [names[6]]: L.tileLayer('http://localhost/pga/{z}/{x}/{y}.png', {maxZoom: 18}),
    [names[7]]: L.tileLayer('http://localhost/pgv/{z}/{x}/{y}.png', {maxZoom: 18}),
    [names[8]]: L.tileLayer('http://localhost/pgd/{z}/{x}/{y}.png', {maxZoom: 18})
};
var map = L.map('mapid', {
    center: [47.751307, 11.588271],
    zoom: 8,
    layers: [baseMaps[mapName]]
});
var baseTree = [
    {
        label: 'Surface',
        children: []
    }
];
for (i = 0; i < 6; i++)
    baseTree[0].children.push({label: names[i], layer: baseMaps[names[i]]});
for (i = 6; i < 9; i++)
    baseTree.push({label: names[i], layer: baseMaps[names[i]]});
L.control.layers.tree(baseTree).addTo(map);
//L.control.layers(baseMaps).addTo(map);
map.on('baselayerchange', function(e) {
    map.closePopup();
    mapName = names[e.name];
    isMapPga = mapName.localeCompare(names[6]) == 0;
    isMapPgv = mapName.localeCompare(names[7]) == 0;
    isMapPgd = mapName.localeCompare(names[8]) == 0;
    
    if (isMapPga || isMapPgv || isMapPgd) colorScaleName = names[0];
    else colorScaleName = mapName;
    colorFunc = chroma.scale(scales[colorScaleName]);
    for (var i = 0; i < sets.length; i++)
        processColor(sets[i], i);
});
map.on('zoomend', function() {
    for (var i = 0; i < sets.length; i++) {
        isSetPga = sets[i].name.indexOf(names[6]) == 0;
        isSetPgv = sets[i].name.indexOf(names[7]) == 0;
        isSetPgd = sets[i].name.indexOf(names[8]) == 0;
        if (isMapPga == isSetPga && isMapPgv == isSetPgv && isMapPgd == isSetPgd)
            processZoom(sets[i], i, map.getZoom());
    }
});

L.control.scale().addTo(map);

function processZoom(set, index, zoom) {
    if (zoom >= set.minZoom && zoom <= set.maxZoom) {
        if (!map.hasLayer(markers[index]))
            markers[index].addTo(map);
    } else
        map.removeLayer(markers[index]);
}

function prettify(num) {
    if (num > 1e3 || num < -1e3 || (num > -1e-3 && num < 1e-3)) return num.toExponential(3);
    else return num.toFixed(3);
}

function processColor(set, index) {
    colorFunc = colorFunc.domain(domains[colorScaleName].map(x => set.minVal+x*(set.maxVal-set.minVal)));
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML += set.name + '<br>';
    for (var i = 0; i < colorCount; i++)
        div.innerHTML += '<span class="grad-step" style="background:' + colorFunc(set.minVal+i/(colorCount-1)*(set.maxVal-set.minVal)) + '"></span>';
    div.innerHTML += '<span class="domain-min">' + prettify(set.minVal) + '</span>' +
                    '<span class="domain-med">' + prettify(set.minVal/2 + set.maxVal/2) + '</span>' +
                    '<span class="domain-max">' + prettify(set.maxVal) + '</span>';
    var wrap = document.createElement('div');
    wrap.appendChild(div.cloneNode(true));
    var markerOptions = {
        title: set.name,
        clickable: true,
        draggable: true,
        icon: colorDataIcon
    }
    isSetPga = set.name.indexOf(names[6]) == 0;
    isSetPgv = set.name.indexOf(names[7]) == 0;
    isSetPgd = set.name.indexOf(names[8]) == 0;
    if (!markers[index]) {
        var marker = L.marker([(set.maxLat+set.minLat)/2, (set.maxLon+set.minLon)/2], markerOptions);
        marker.on('move', function(e) {
            var newLon = e.latlng.lng, newLat = e.latlng.lat;
            var needsSet = false;
            if (newLon > set.maxLon || newLon < set.minLon || newLat > set.maxLat || newLat < set.minLat) {
                needsSet = true;
                if (newLon > set.maxLon) newLon = set.maxLon;
                else if (newLon < set.minLon) newLon = set.minLon;
                if (newLat > set.maxLat) newLat = set.maxLat;
                else if (newLat < set.minLat) newLat = set.minLat;
            }
            if (needsSet)
                this.setLatLng([newLat, newLon]);
        });
        marker.bindPopup(wrap.innerHTML);
        markers.push(marker);
        
        if (isMapPga == isSetPga && isMapPgv == isSetPgv && isMapPgd == isSetPgd)
            marker.addTo(map);
    } else {
        markers[index].unbindPopup();
        markers[index].bindPopup(wrap.innerHTML);
        
        if (isMapPga == isSetPga && isMapPgv == isSetPgv && isMapPgd == isSetPgd)
            markers[index].addTo(map);
        else
            map.removeLayer(markers[index]);
    }
    
    
}
var sets = [];
var markers = [];
var colorDataIcon = L.icon({
    iconUrl: 'images/color-data.png',
    iconSize: [20, 20]
});
let xhr = new XMLHttpRequest();
xhr.open('GET', 'http://localhost/data/oseism.json');
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.responseType = 'json';
xhr.onload = function() {
    if (xhr.status !== 200) return;
    sets = xhr.response.sets;
    for (var i = 0; i < sets.length; i++)
        processColor(sets[i], i);
};
xhr.send();

/*L.tileLayer('http://localhost/hot/{z}/{x}/{y}.png', {
    maxZoom: 18
}).addTo(mymap);*/

/*var maxData = Number.MIN_VALUE, minData = Number.MAX_VALUE;
layer = L.shapefile("../data/seis_cells", {
    onEachFeature: function(feature, layer) {
        var d = feature.properties.Data;
        if (d > maxData) maxData = d;
        if (d < minData) minData = d;
    }
});
layer.once("data:loaded", function() {
    var f = chroma.scale(['0000ff', '00ffff', '00ff00', 'ffff00', 'ff0000']).domain([minData, maxData]);
    layer.setStyle(function(feature) {
        var d = feature.properties.Data;
        return {
            stroke: false,
            fill: true,
            fillColor: f(d),
            fillOpacity: (d-minData)/(maxData-minData)
        };
    });
});
layer.addTo(mymap);*/
