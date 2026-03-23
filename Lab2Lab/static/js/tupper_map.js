L.mapquest.key = '8fL7LBlhS4awllFpiNbMf4uXQw5vQP2k';

// 'map' refers to a <div> element with the ID map
var map = L.mapquest.map('map', {
  center: [45.49037373354115, -73.58235745766375],
  layers: L.mapquest.tileLayer('map'),
  zoom: 16
});

//map.addControl(L.mapquest.control());
