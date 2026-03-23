const rowh = 20;    // Row height
const mpx = 5   // Minutes per pixel
const hours_size = 16;
const hours_font = 'Helvetica';

const dataElement = document.getElementById("data-container");
const moon_json = dataElement.getAttribute("data-label");
const moon_data = JSON.parse(moon_json);
console.log(moon_data)  // Todo: Remove later

createBox(svg_moon, -12*60/mpx, -2*rowh, 24*60/mpx, 5*rowh, '#48c78e');    // Day box
createBox(svg_moon, -24*60/mpx, -2*rowh, 12*60/mpx, 5*rowh, 'lightgrey');    // Yesterday box
createBox(svg_moon, 12*60/mpx, -2*rowh, 12*60/mpx, 5*rowh, 'lightgrey');    // Tomorrow box
createText(svg_moon, 0, -2.5*rowh, 'black', moon_data.date);   // Date text
createText(svg_moon, -18*60/mpx, -2.5*rowh, 'black', 'Yesterday');
createText(svg_moon, 18*60/mpx, -2.5*rowh, 'black', 'Tomorrow');

let now_x = moon_data.delta_noon/5
createTicker(svg_moon, now_x, -2*rowh, 3*rowh, 'red', '2');
createText(svg_moon, now_x, 4*rowh, 'black', 'NOW');   // NOW text
createText(svg_moon, now_x, 5*rowh, 'black', moon_data.hour);   // Hours now text
createMoonBar(svg_moon, moon_data.rise1, moon_data.dr1, moon_data.transit1, moon_data.dt1, moon_data.set1, moon_data.ds1)
createMoonBar(svg_moon, moon_data.rise2, moon_data.dr2, moon_data.transit2, moon_data.dt2, moon_data.set2, moon_data.ds2)

function createBox(obj, x, y, w, h, f) {
    let box = document.createElementNS(SVG_NS, 'rect');
    box.setAttributeNS(null, 'x', x.toString());
    box.setAttributeNS(null, 'y', y.toString());
    box.setAttributeNS(null, 'width', w.toString());
    box.setAttributeNS(null, 'height', h.toString());
    box.setAttributeNS(null, 'rx', '5');
    box.setAttributeNS(null, 'fill', f);
    obj.appendChild(box);
}

function createText(obj, x, y, color, content) {
    let t = document.createElementNS(SVG_NS, 'text');
    t.setAttributeNS(null, 'x', x.toString());
    t.setAttributeNS(null, 'y', y.toString());
    t.setAttributeNS(null, 'alignment-baseline', 'middle');
    t.setAttributeNS(null, 'text-anchor', 'middle');
    t.setAttributeNS(null, "font-family", hours_font);
    t.setAttributeNS(null, 'fill', color);
    t.setAttributeNS(null, 'font-size', hours_size);

    let texte = document.createTextNode(content);
    t.appendChild(texte);
    obj.appendChild(t);
}

function createTicker(obj, x, y1, y2, content) {
    let ticker = document.createElementNS(SVG_NS, 'line');
    ticker.setAttributeNS(null, 'x1', x.toString());
    ticker.setAttributeNS(null, 'y1', y1.toString());
    ticker.setAttributeNS(null, 'x2', x.toString());
    ticker.setAttributeNS(null, 'y2', y2.toString());
    ticker.setAttributeNS(null, 'stroke', 'red');
    ticker.setAttributeNS(null, 'stroke-width', '2');
    obj.appendChild(ticker);
}

function createMoonBar(obj, rise, drise, transit, dtransit, set, dset) {
    createBox(svg_moon, drise/5, 0, (dset-drise)/5, rowh);
    createDot(svg_moon, dtransit/5, rowh/2)
    createText(svg_moon, dtransit/5, -rowh/2, 'black', 'Transit');
    createText(svg_moon, dtransit/5, -2.5*rowh/2, 'black', transit);
    createText(svg_moon, drise/5, 3*rowh/2, 'black', 'Rise');
    createText(svg_moon, drise/5, 4.5*rowh/2, 'black', rise);
    createText(svg_moon, dset/5, 3*rowh/2, 'black', 'Set');
    createText(svg_moon, dset/5, 4.5*rowh/2, 'black', set);
}

function createDot(obj, x, y) {
    let dot = document.createElementNS(SVG_NS, 'circle');
    dot.setAttributeNS(null, 'cx', x.toString());
    dot.setAttributeNS(null, 'cy', y.toString());
    dot.setAttributeNS(null, 'r', (rowh/4).toString());
    dot.setAttributeNS(null, 'fill', 'white');
    obj.appendChild(dot);
}