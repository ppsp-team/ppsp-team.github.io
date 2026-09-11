// Build the publication badge master in Illustrator and export PNGs at 1x and 2x.
// Geometry (in pt, 1pt = 1px at 1x) replicates the original PPSP badges:
// height 30, 3pt inside border, 5pt outer corner radius, Arial 12pt, 10.5pt side padding.
//
// Usage: replace __OUT_DIR__ / __AI_PATH__ below, then run from Illustrator (File > Scripts)
// or: osascript -e 'tell application id "com.adobe.illustrator" to do javascript (POSIX file "/abs/path/publication_badges.jsx")'
// Illustrator replaces spaces with hyphens in exported names: rename "Journal-Paper*" and
// "Social-Cognitive-and-Affective-Neuroscience*" back to their spaced names before copying
// them to assets/img/icons/. To add a badge, append an entry to BADGES.
#target illustrator

var OUT_DIR = "__OUT_DIR__";
var AI_PATH = "__AI_PATH__";

var HEIGHT = 30;
var BORDER = 3;
var RADIUS = 5;
var PAD = 10.5;          // ink-to-edge side padding measured on the originals (21px @2x)
var FONT_SIZE = 12;
var BASELINE = 19;       // baseline offset from top (38px @2x, matches the originals' cap top at 20px)
var FONT_SIZE_2L = 10;   // two-line badges
var BASELINES_2L = [14.15, 24.15];
var GAP = 20;            // vertical gap between artboards

function rgb(hex) {
    var c = new RGBColor();
    c.red = parseInt(hex.substr(0, 2), 16);
    c.green = parseInt(hex.substr(2, 2), 16);
    c.blue = parseInt(hex.substr(4, 2), 16);
    return c;
}

var STYLES = {
    category: { border: rgb("065896"), fill: rgb("0B67AC"), text: rgb("DEE6EB") },
    type: { border: rgb("BCE0FD"), fill: rgb("F1F9FF"), text: rgb("2699FB") }
};

var BADGES = [
    { file: "Computational", lines: ["Computational"], style: "category" },
    { file: "Experimental", lines: ["Experimental"], style: "category" },
    { file: "Review", lines: ["Review"], style: "category" },
    { file: "Opinion_Perspectives", lines: ["Opinion/Perspectives"], style: "category" },
    { file: "Social Cognitive and Affective Neuroscience", lines: ["Social Cognitive &", "Affective Neuroscience"], style: "category" },
    { file: "Methods_Tools", lines: ["Methods/Tools"], style: "category" },
    { file: "NeuroAI_ML", lines: ["NeuroAI/ML"], style: "category" },
    { file: "Journal Paper", lines: ["Journal Paper"], style: "type" },
    { file: "Preprint", lines: ["Preprint"], style: "type" },
    { file: "Comment", lines: ["Comment"], style: "type" },
    { file: "Book_Chapter", lines: ["Book/Chapter"], style: "type" },
    { file: "Poster_Conference", lines: ["Poster/Conference"], style: "type" }
];

var font = app.textFonts.getByName("ArialMT");
var doc = app.documents.add(DocumentColorSpace.RGB, 400, HEIGHT);
doc.rulerOrigin = [0, 0];

function makeText(layer, str, size, color) {
    var t = layer.textFrames.add();
    t.contents = str;
    var attrs = t.textRange.characterAttributes;
    attrs.textFont = font;
    attrs.size = size;
    attrs.fillColor = color;
    return t;
}

// Ink extent of a string relative to its baseline anchor: outline a throwaway copy.
// Returns {left, width}: ink left edge offset from the anchor x, and ink width.
function inkBounds(layer, str, size) {
    var t = makeText(layer, str, size, rgb("000000"));
    var ax = t.anchor[0];
    var g = t.createOutline();
    var b = g.geometricBounds; // [left, top, right, bottom]
    g.remove();
    return { left: b[0] - ax, width: b[2] - b[0] };
}

var layer = doc.layers[0];
var top = 0;
for (var i = 0; i < BADGES.length; i++) {
    var badge = BADGES[i];
    var st = STYLES[badge.style];
    var twoLines = badge.lines.length > 1;
    var size = twoLines ? FONT_SIZE_2L : FONT_SIZE;

    var inkW = 0;
    for (var k = 0; k < badge.lines.length; k++) {
        inkW = Math.max(inkW, inkBounds(layer, badge.lines[k], size).width);
    }
    var width = Math.ceil(inkW + 2 * PAD);

    var rect = [0, top, width, top - HEIGHT];
    var ab;
    if (i === 0) {
        ab = doc.artboards[0];
        ab.artboardRect = rect;
    } else {
        ab = doc.artboards.add(rect);
    }
    ab.name = badge.file;

    var grp = layer.groupItems.add();
    grp.name = badge.file;

    var outer = grp.pathItems.roundedRectangle(top, 0, width, HEIGHT, RADIUS, RADIUS);
    outer.filled = true; outer.fillColor = st.border; outer.stroked = false;
    var inner = grp.pathItems.roundedRectangle(top - BORDER, BORDER, width - 2 * BORDER, HEIGHT - 2 * BORDER, RADIUS - BORDER, RADIUS - BORDER);
    inner.filled = true; inner.fillColor = st.fill; inner.stroked = false;

    var baselines = twoLines ? BASELINES_2L : [BASELINE];
    for (var k = 0; k < badge.lines.length; k++) {
        var t = makeText(grp, badge.lines[k], size, st.text);
        var ink = inkBounds(layer, badge.lines[k], size);
        // Single line: center the ink box. Two lines: left-align at the padding, like the original.
        var inkX = twoLines ? PAD : (width - ink.width) / 2;
        var targetX = inkX - ink.left;
        var targetY = top - baselines[k];
        t.translate(targetX - t.anchor[0], targetY - t.anchor[1]);
    }
    top -= HEIGHT + GAP;
}

// Export every artboard at 100% and 200%.
function exportAll(scale, suffix) {
    for (var i = 0; i < doc.artboards.length; i++) {
        doc.artboards.setActiveArtboardIndex(i);
        var opts = new ExportOptionsPNG24();
        opts.antiAliasing = true;
        opts.transparency = true;
        opts.artBoardClipping = true;
        opts.horizontalScale = scale;
        opts.verticalScale = scale;
        var f = new File(OUT_DIR + "/" + doc.artboards[i].name + suffix + ".png");
        doc.exportFile(f, ExportType.PNG24, opts);
    }
}
exportAll(100, "");
exportAll(200, "@2x");

doc.saveAs(new File(AI_PATH));
"exported " + doc.artboards.length + " artboards";
