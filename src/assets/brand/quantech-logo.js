/*!
 * Quantech Graphics animated logo: "Crystal iso assembly"
 * Drop-in, no dependencies. Draws the exact logo geometry and Futura glyph outlines
 * from the brand .ai file; the effects only change surface and timing.
 *
 * Usage:
 *   <div id="brand" style="width:180px"></div>
 *   <script src="quantech-logo.js"><\/script>
 *   <script>QuantechLogo.mount(document.getElementById('brand'), { wordmark: true });<\/script>
 *
 * Options (all optional):
 *   intro:      'first-visit' (default) | 'always' | 'never'
 *               first-visit plays the assembly once per browser, then shows the resting logo.
 *   idle:       true   periodic crystal + lightning pulse while the logo rests
 *   idleEvery:  9000   ms between pulses (+/- 20% jitter)
 *   hoverPulse: true   a pulse on hover/focus (throttled)
 *   wordmark:   true   include "QUANTECH GRAPHICS"; false = mark only
 *   label:      'Quantech Graphics'  accessible name
 *   onIntroEnd: function called when the intro finishes
 * Returns { replay(), pulse(), destroy() }.
 * Respects prefers-reduced-motion (static logo, no motion).
 */
(function (global) {
  "use strict";
  var L = {"top":"M 838.339844 471.957031 L 815.257812 458.570312 L 952.042969 379.226562 L 1088.832031 458.570312 L 997.355469 511.628906 L 1042.929688 538.0625 L 1019.847656 551.453125 L 974.269531 525.015625 L 928.695312 551.453125 L 860.570312 511.628906 L 928.960938 471.957031 L 952.042969 485.34375 L 906.734375 511.628906 L 929.742188 524.972656 L 1043.445312 459.019531 L 952.042969 406.003906 Z M 838.339844 471.957031","sides":["M 952.042969 485.34375 L 952.042969 512.035156 L 929.742188 524.972656 L 906.734375 511.628906 Z M 952.042969 485.34375","M 838.339844 471.957031 L 838.339844 498.734375 L 952.042969 432.78125 L 952.042969 406.003906 Z M 838.339844 471.957031","M 1088.832031 458.570312 L 1088.832031 485.34375 L 1020.4375 525.015625 L 997.355469 511.628906 Z M 1088.832031 458.570312","M 1042.929688 564.835938 L 1019.847656 578.230469 L 1019.847656 551.453125 L 1042.929688 538.0625 Z M 1042.929688 564.835938","M 928.695312 578.226562 L 928.695312 551.453125 L 974.269531 525.015625 L 974.269531 551.792969 Z M 928.695312 578.226562"],"glyphs":{"glyph-0-7":"M 6.04 -17.21 L 19.79 -17.21 L 19.79 -28.85 L 23.39 -28.85 L 23.39 0 L 19.79 0 L 19.79 -13.85 L 6.04 -13.85 L 6.04 0 L 2.45 0 L 2.45 -28.85 L 6.04 -28.85 Z M 6.04 -17.21","glyph-0-12":"M 6.23 -28.85 L 6.23 0 L 2.64 0 L 2.64 -28.85 Z M 6.23 -28.85","glyph-0-4":"M 10.53 -25.57 L 10.53 0 L 6.92 0 L 6.92 -25.57 L 0.07 -25.57 L 0.07 -28.85 L 17.37 -28.85 L 17.37 -25.57 Z M 10.53 -25.57","glyph-0-5":"M 2.75 0 L 2.75 -28.85 L 18.26 -28.85 L 18.26 -25.57 L 6.35 -25.57 L 6.35 -17.5 L 17.92 -17.5 L 17.92 -14.20 L 6.35 -14.20 L 6.35 -3.29 L 18.26 -3.29 L 18.26 0 Z M 2.75 0","glyph-0-13":"M 18.45 -25.10 L 15.57 -23.39 C 14.50 -25.20 12.96 -26.10 10.95 -26.10 C 9.72 -26.10 8.60 -25.72 7.60 -24.95 C 6.61 -24.19 6.12 -23.21 6.12 -22.01 C 6.12 -20.27 7.46 -18.89 10.14 -17.87 L 12.21 -17.07 C 14.50 -16.17 16.27 -15.06 17.51 -13.73 C 18.75 -12.41 19.37 -10.62 19.37 -8.39 C 19.37 -5.78 18.48 -3.63 16.70 -1.93 C 14.92 -0.23 12.74 0.60 10.14 0.60 C 7.81 0.60 5.82 -0.14 4.17 -1.65 C 2.51 -3.17 1.53 -5.11 1.21 -7.46 L 4.85 -8.23 C 4.83 -6.67 5.36 -5.36 6.45 -4.31 C 7.53 -3.26 8.86 -2.75 10.45 -2.75 C 11.98 -2.75 13.25 -3.30 14.25 -4.42 C 15.25 -5.53 15.76 -6.85 15.76 -8.39 C 15.76 -9.78 15.32 -10.88 14.43 -11.68 C 13.56 -12.5 12.34 -13.22 10.79 -13.85 L 8.79 -14.70 C 6.83 -15.54 5.30 -16.51 4.18 -17.60 C 3.08 -18.70 2.53 -20.17 2.53 -22.01 C 2.53 -24.25 3.36 -26.05 5.04 -27.42 C 6.73 -28.78 8.72 -29.46 11.03 -29.46 C 14.34 -29.46 16.81 -28.01 18.45 -25.10 Z M 18.45 -25.10","glyph-0-1":"M 2.26 -28.85 L 5.85 -28.85 L 5.85 -11.82 C 5.85 -5.77 8.17 -2.75 12.82 -2.75 C 17.47 -2.75 19.79 -5.77 19.79 -11.82 L 19.79 -28.85 L 23.39 -28.85 L 23.39 -10.60 C 23.39 -7.33 22.43 -4.64 20.53 -2.54 C 18.63 -0.44 16.06 0.60 12.82 0.60 C 9.58 0.60 7.01 -0.44 5.10 -2.54 C 3.21 -4.64 2.26 -7.33 2.26 -10.60 Z M 2.26 -28.85","glyph-0-11":"M 6.35 -12.09 L 6.35 0 L 2.75 0 L 2.75 -28.85 L 6.89 -28.85 C 11.14 -28.85 14.15 -28.16 15.90 -26.76 C 17.65 -25.37 18.53 -23.29 18.53 -20.51 C 18.53 -17.66 17.59 -15.53 15.71 -14.15 C 13.84 -12.78 11.41 -12.09 8.42 -12.09 Z M 6.35 -25.64 L 6.35 -15.31 L 7.5 -15.31 C 8.55 -15.31 9.47 -15.37 10.28 -15.5 C 11.08 -15.62 11.87 -15.85 12.67 -16.20 C 13.46 -16.55 14.07 -17.10 14.5 -17.84 C 14.93 -18.58 15.15 -19.5 15.15 -20.59 C 15.15 -21.66 14.92 -22.55 14.46 -23.26 C 14.00 -23.98 13.35 -24.5 12.51 -24.81 C 11.67 -25.13 10.85 -25.35 10.06 -25.46 C 9.26 -25.58 8.35 -25.64 7.31 -25.64 Z M 6.35 -25.64","glyph-0-3":"M 2.40 0 L 2.40 -30.23 L 24.07 -7.54 L 24.07 -28.85 L 27.67 -28.85 L 27.67 1.18 L 6.01 -21.51 L 6.01 0 Z M 2.40 0","glyph-0-9":"M 17.60 -14.54 L 29.06 -14.54 L 29.06 -13.39 C 29.06 -9.39 27.78 -6.05 25.23 -3.39 C 22.67 -0.72 19.39 0.60 15.39 0.60 C 11.37 0.60 7.94 -0.87 5.07 -3.84 C 2.22 -6.82 0.79 -10.32 0.79 -14.35 C 0.79 -18.51 2.25 -22.07 5.17 -25.03 C 8.09 -27.98 11.62 -29.46 15.76 -29.46 C 18.03 -29.46 20.21 -28.97 22.29 -28 C 24.37 -27.01 26.12 -25.64 27.53 -23.89 L 25 -21.46 C 23.94 -22.90 22.60 -24.05 20.96 -24.90 C 19.34 -25.75 17.66 -26.18 15.92 -26.18 C 12.70 -26.18 9.97 -25.03 7.75 -22.75 C 5.51 -20.46 4.40 -17.70 4.40 -14.46 C 4.40 -11.38 5.50 -8.64 7.71 -6.25 C 9.92 -3.86 12.56 -2.67 15.62 -2.67 C 17.91 -2.67 20.03 -3.52 22 -5.23 C 23.96 -6.95 24.99 -8.95 25.07 -11.25 L 17.60 -11.25 Z M 17.60 -14.54","glyph-0-0":"M 30.93 0.60 L 26.56 0.60 L 24.07 -1.95 C 21.59 -0.24 18.85 0.60 15.84 0.60 C 11.63 0.60 8.06 -0.82 5.12 -3.70 C 2.19 -6.58 0.73 -10.16 0.73 -14.43 C 0.73 -18.57 2.21 -22.10 5.18 -25.04 C 8.15 -27.99 11.70 -29.46 15.84 -29.46 C 19.97 -29.46 23.53 -27.99 26.5 -25.04 C 29.47 -22.10 30.96 -18.57 30.96 -14.43 C 30.96 -12.39 30.57 -10.44 29.78 -8.59 C 28.98 -6.73 27.87 -5.14 26.45 -3.79 Z M 19.45 -10.87 L 24 -6.35 C 25.07 -7.29 25.89 -8.50 26.48 -10 C 27.07 -11.5 27.37 -12.97 27.37 -14.43 C 27.37 -17.67 26.28 -20.42 24.09 -22.70 C 21.91 -24.97 19.16 -26.10 15.84 -26.10 C 12.53 -26.10 9.78 -24.97 7.59 -22.70 C 5.41 -20.42 4.32 -17.67 4.32 -14.43 C 4.32 -11.16 5.46 -8.39 7.73 -6.14 C 10.00 -3.87 12.70 -2.75 15.84 -2.75 C 17.93 -2.75 19.85 -3.30 21.59 -4.40 L 14.96 -10.87 Z M 19.45 -10.87","glyph-0-10":"M 11.59 -12.56 L 20.70 0 L 16.34 0 L 7.84 -12.21 L 6.35 -12.21 L 6.35 0 L 2.75 0 L 2.75 -28.85 L 7.12 -28.85 C 8.21 -28.85 9.10 -28.83 9.78 -28.79 C 10.45 -28.76 11.27 -28.64 12.23 -28.43 C 13.19 -28.23 14.02 -27.93 14.73 -27.53 C 15.91 -26.83 16.83 -25.85 17.51 -24.60 C 18.19 -23.35 18.53 -22.03 18.53 -20.64 C 18.53 -18.54 17.89 -16.73 16.60 -15.21 C 15.33 -13.69 13.66 -12.81 11.59 -12.56 Z M 6.35 -25.64 L 6.35 -15.20 L 7.5 -15.20 C 8.55 -15.20 9.47 -15.26 10.28 -15.39 C 11.08 -15.51 11.87 -15.75 12.67 -16.09 C 13.46 -16.43 14.07 -16.97 14.5 -17.71 C 14.93 -18.45 15.15 -19.37 15.15 -20.48 C 15.15 -23.92 12.53 -25.64 7.31 -25.64 Z M 6.35 -25.64","glyph-0-6":"M 23.76 -27.53 L 23.76 -23.34 C 21.64 -25.23 19.11 -26.18 16.15 -26.18 C 12.96 -26.18 10.26 -25.03 8.06 -22.71 C 5.85 -20.40 4.75 -17.62 4.75 -14.39 C 4.75 -11.20 5.83 -8.45 8.01 -6.14 C 10.20 -3.82 12.89 -2.67 16.07 -2.67 C 18.98 -2.67 21.54 -3.67 23.76 -5.67 L 23.76 -1.42 C 21.47 -0.06 18.94 0.60 16.18 0.60 C 12.05 0.60 8.50 -0.82 5.56 -3.70 C 2.61 -6.58 1.14 -10.11 1.14 -14.28 C 1.14 -18.53 2.63 -22.13 5.62 -25.06 C 8.61 -28 12.23 -29.46 16.5 -29.46 C 19.22 -29.46 21.64 -28.82 23.76 -27.53 Z M 23.76 -27.53","glyph-0-2":"M 20.09 -7.23 L 6.85 -7.23 L 3.56 0 L -0.31 0 L 13.46 -30.09 L 27.25 0 L 23.39 0 Z M 18.60 -10.53 L 13.46 -22.20 L 8.34 -10.53 Z M 18.60 -10.53"},"uses":[["glyph-0-0",639.7832,690.5117],["glyph-0-1",686.512939,690.5117],["glyph-0-2",725.349115,690.5117],["glyph-0-3",767.006608,690.5117],["glyph-0-4",811.62323,690.5117],["glyph-0-5",843.446308,690.5117],["glyph-0-6",877.577737,690.5117],["glyph-0-7",917.156566,690.5117],["glyph-0-9",984.684427,690.5117],["glyph-0-10",1029.128784,690.5117],["glyph-0-2",1065.863327,690.5117],["glyph-0-11",1107.337071,690.5117],["glyph-0-7",1140.633972,690.5117],["glyph-0-12",1181.204282,690.5117],["glyph-0-6",1204.758642,690.5117],["glyph-0-13",1244.352784,690.5117]]};
  var NS = "http://www.w3.org/2000/svg";
  var COL = { top: "#E6E7E5", side: "#536465", word: "#E6E7E5" };
  var AX = [Math.cos(-Math.PI / 6), Math.sin(-Math.PI / 6)], NRM = [0.5, Math.sqrt(3) / 2];
  var SIDES_D = L.sides.join(" "), MARK_D = L.top + " " + SIDES_D;
  var X0 = 815, XW = 274; // left tip x and width of the mark, for the left-to-right waves
  var uidN = 0;

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function polyPts(d) {
    var n = d.split(/Z/i)[0].match(/-?\d+\.?\d*/g).map(Number), p = [];
    for (var i = 0; i + 1 < n.length; i += 2) p.push([n[i], n[i + 1]]);
    return p;
  }
  function clipToTri(subject, tri) { // Sutherland-Hodgman with the triangle as the convex window
    function cr(a, b, p) { return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]); }
    var sgn = Math.sign(cr(tri[0], tri[1], tri[2])) || 1, out = subject;
    for (var i = 0; i < 3 && out.length; i++) {
      var a = tri[i], b = tri[(i + 1) % 3], inp = out; out = [];
      for (var j = 0; j < inp.length; j++) {
        var P = inp[j], Q = inp[(j + 1) % inp.length], c1 = cr(a, b, P) * sgn, c2 = cr(a, b, Q) * sgn;
        if (c1 >= 0) out.push(P);
        if ((c1 >= 0) !== (c2 >= 0)) { var t = c1 / (c1 - c2); out.push([P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t]); }
      }
    }
    return out;
  }
  function polyArea(p) {
    var s = 0; for (var i = 0; i < p.length; i++) { var v = p[i], w = p[(i + 1) % p.length]; s += v[0] * w[1] - w[0] * v[1]; }
    return Math.abs(s) / 2;
  }
  // shards: the mark's faces cut along a triangle lattice rotated 30deg (edges follow the iso axes)
  var SHARDS = null;
  function shardGeometry() {
    if (SHARDS) return SHARDS;
    var seed = 19; function rnd() { return (seed = (seed * 16807) % 2147483647) / 2147483647; }
    var TOP = polyPts(L.top), SIDES = L.sides.map(polyPts);
    var cx = 952, cy = 478, sp = 13, h = sp * Math.sqrt(3) / 2, R = 200, c30 = Math.cos(Math.PI / 6), s30 = 0.5;
    var nr = Math.ceil(2 * R / h), nc = Math.ceil(2 * R / sp) + 1, rows = [], r, c;
    for (r = 0; r <= nr; r++) { var row = []; for (c = 0; c <= nc; c++) {
      var lx = -R + c * sp + (r % 2 ? sp / 2 : 0) + (rnd() - 0.5) * sp * 0.28, ly = -R + r * h + (rnd() - 0.5) * h * 0.28;
      row.push([cx + lx * c30 - ly * s30, cy + lx * s30 + ly * c30]); } rows.push(row); }
    var tris = [];
    for (r = 0; r < nr; r++) for (c = 0; c < nc; c++) {
      var A = rows[r], B = rows[r + 1];
      if (r % 2 === 0) tris.push([A[c], A[c + 1], B[c]], [A[c + 1], B[c + 1], B[c]]);
      else tris.push([A[c], A[c + 1], B[c + 1]], [A[c], B[c + 1], B[c]]);
    }
    var out = [];
    function add(p, top, band) {
      var m = [0, 0]; p.forEach(function (v) { m[0] += v[0] / p.length; m[1] += v[1] / p.length; });
      out.push({
        pts: p.map(function (v) { return v[0].toFixed(2) + "," + v[1].toFixed(2); }).join(" "), top: top, m: m, k: rnd(), band: band,
        crystal: top ? "hsl(186," + (10 + rnd() * 22).toFixed(1) + "%," + (80 + rnd() * 15 - (m[0] - X0) / XW * 6).toFixed(1) + "%)"
                     : "hsl(186," + (10 + rnd() * 16).toFixed(1) + "%," + (27 + rnd() * 12).toFixed(1) + "%)",
        glass: top ? "hsla(188,70%,88%," + (0.12 + rnd() * 0.16).toFixed(2) + ")" : "hsla(188,55%,60%," + (0.12 + rnd() * 0.14).toFixed(2) + ")",
        edge: top ? "rgba(255,255,255,.4)" : "rgba(127,233,242,.28)"
      });
    }
    tris.forEach(function (t) {
      var p = clipToTri(TOP, t);
      if (p.length >= 3 && polyArea(p) >= 0.4) {
        var mx = 0, my = 0; p.forEach(function (v) { mx += v[0] / p.length; my += v[1] / p.length; });
        var proj = mx * NRM[0] + my * NRM[1];
        add(p, true, proj < 866 ? 0 : proj < 928 ? 1 : 2);
      }
      SIDES.forEach(function (f) { var q = clipToTri(f, t); if (q.length >= 3 && polyArea(q) >= 0.4) add(q, false, -1); });
    });
    return (SHARDS = out);
  }

  function mount(host, opts) {
    var o = Object.assign({ intro: "first-visit", idle: true, idleEvery: 9000, hoverPulse: true, wordmark: true,
      label: "Quantech Graphics", storageKey: "qg-logo-intro-seen", onIntroEnd: null }, opts || {});
    var reduced = global.matchMedia && global.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var id = "qgl" + (++uidN);
    var vb = o.wordmark ? "600 350 720 370" : "800 365 304 228";
    var svg = el("svg", { viewBox: vb, role: "img", "aria-label": o.label, style: "display:block;width:100%;height:auto;overflow:visible" });
    host.appendChild(svg);
    var defs = el("defs", {}, svg);
    el("path", { d: SIDES_D }, el("clipPath", { id: id + "s" }, defs));
    el("path", { d: MARK_D }, el("clipPath", { id: id + "m" }, defs));
    var solid = el("g", {}, svg);
    el("path", { d: L.top, fill: COL.top }, solid);
    el("path", { d: SIDES_D, fill: COL.side }, solid);
    var sideG = el("g", {}, el("g", { "clip-path": "url(#" + id + "s)" }, svg));
    var slabs = [0, 1, 2].map(function () { return el("g", {}, svg); });
    var flash = el("path", { d: MARK_D, fill: "#ffffff", opacity: 0, style: "mix-blend-mode:screen" }, svg);
    var uses = [];
    if (o.wordmark) {
      var g = el("g", { fill: COL.word }, svg);
      L.uses.forEach(function (u) { var gg = el("g", {}, g); el("path", { d: L.glyphs[u[0]], transform: "translate(" + u[1] + "," + u[2] + ")" }, gg); uses.push(gg); }); // animate the wrapper so the glyph keeps its own transform
    }
    var shards = shardGeometry().map(function (s) {
      var poly = el("polygon", { points: s.pts, "stroke-linejoin": "round" }, s.band >= 0 ? slabs[s.band] : sideG);
      poly.style.fill = s.crystal; poly.style.stroke = s.edge; poly.style.strokeWidth = ".45px"; poly.style.opacity = 0;
      return Object.assign({ poly: poly }, s);
    });
    var anims = [], timers = [], busy = false, lastPulse = 0, dead = false, visible = true;
    function A(node, kf, op) { var a = node.animate(kf, op); anims.push(a); return a; }
    function clear() { anims.forEach(function (a) { a.cancel(); }); anims = []; timers.forEach(clearTimeout); timers = []; }
    function later(fn, ms) { timers.push(setTimeout(fn, ms)); }
    function rest() { // the resting logo: solid, shards hidden
      clear(); busy = false; solid.style.opacity = 1; uses.forEach(function (u) { u.style.opacity = 1; });
      shards.forEach(function (s) { s.poly.style.opacity = 0; });
    }
    var WHITE = "rgba(255,255,255,.95)";

    // ---- intro: glass slabs slide in, walls extrude, glass frosts to crystal,
    //      then one quick left-to-right lightning wave turns crystal to solid, ending in a flash
    function intro() {
      clear(); busy = true;
      solid.style.opacity = 0;
      shards.forEach(function (s) { s.poly.style.opacity = 1; });
      var land = [];
      slabs.forEach(function (g, i) {
        var dir = i % 2 ? -1 : 1, delay = 150 + i * 280, dur = 950;
        A(g, [{ transform: "translate(" + AX[0] * 150 * dir + "px," + AX[1] * 150 * dir + "px)", opacity: 0 }, { offset: 0.25, opacity: 1 }, { transform: "translate(0,0)", opacity: 1 }],
          { duration: dur, delay: delay, easing: "cubic-bezier(.16,1,.3,1)", fill: "both" });
        land[i] = delay + dur * 0.55;
      });
      A(sideG, [{ transform: "translateY(-26.8px)", opacity: 0 }, { offset: 0.15, opacity: 1 }, { transform: "translateY(0)", opacity: 1 }],
        { duration: 700, delay: 1350, easing: "cubic-bezier(.3,0,.2,1)", fill: "both" });
      shards.forEach(function (s) {
        var x = (s.m[0] - X0) / XW;
        var hit = s.band >= 0 ? land[s.band] + s.k * 110 : 1700 + (s.m[1] - 400) * 1.6 + s.k * 90;
        var frost = Math.max(hit + 200, 2150 + x * 380);
        // material lerp glass -> crystal (created first so its backwards fill gives the glass look)
        A(s.poly, [{ fill: s.glass, stroke: "rgba(200,250,255,.85)" }, { fill: s.crystal, stroke: s.edge }], { duration: 380, delay: frost, easing: "ease-in-out", fill: "both" });
        A(s.poly, [{ fill: WHITE, stroke: "#fff" }, { fill: s.glass, stroke: "rgba(200,250,255,.85)" }], { duration: 300, delay: hit, easing: "ease-out" });
        // lightning wave: crystal flashes white and dissolves to the solid underneath, left to right
        A(s.poly, [{ fill: s.crystal, stroke: s.edge, opacity: 1 }, { offset: 0.3, fill: WHITE, stroke: "#fff", opacity: 1 }, { fill: WHITE, stroke: "#fff", opacity: 0 }],
          { duration: 340, delay: 2650 + x * 520 + s.k * 90, easing: "ease-out", fill: "forwards" });
      });
      A(solid, [{ opacity: 0 }, { opacity: 1 }], { duration: 1, delay: 2640, fill: "both" });
      A(flash, [{ opacity: 0 }, { opacity: 0.55, offset: 0.18 }, { opacity: 0 }], { duration: 520, delay: 3330, easing: "ease-out" });
      uses.forEach(function (u, i) {
        A(u, [{ opacity: 0, transform: "translateY(8px)" }, { opacity: 1, transform: "translateY(0)" }], { duration: 550, delay: 1850 + i * 45, easing: "cubic-bezier(.2,.8,.2,1)", fill: "both" });
      });
      later(function () { rest(); if (o.onIntroEnd) o.onIntroEnd(); schedule(); }, 3950);
    }

    // ---- idle pulse: a left-to-right lightning wave crystallizes the logo, then flashes back to solid
    function pulse() {
      if (busy || reduced || dead) return;
      busy = true; lastPulse = Date.now();
      shards.forEach(function (s) {
        var x = (s.m[0] - X0) / XW, d = x * 520 + s.k * 90;
        A(s.poly, [
          { opacity: 0, fill: s.crystal, stroke: s.edge },
          { offset: 0.14, opacity: 1, fill: WHITE, stroke: "#fff" },
          { offset: 0.34, opacity: 1, fill: s.crystal, stroke: s.edge },
          { offset: 0.66, opacity: 1, fill: s.crystal, stroke: s.edge },
          { offset: 0.8, opacity: 1, fill: WHITE, stroke: "#fff" },
          { opacity: 0, fill: WHITE, stroke: "#fff" }],
          { duration: 1150, delay: d, easing: "linear" });
      });
      A(flash, [{ opacity: 0 }, { opacity: 0.35, offset: 0.2 }, { opacity: 0 }], { duration: 480, delay: 1400, easing: "ease-out" });
      later(function () { busy = false; anims = []; schedule(); }, 1900);
    }
    function schedule() {
      if (!o.idle || reduced || dead) return;
      later(function tick() {
        if (dead) return;
        if (document.hidden || !visible) { later(tick, 1500); return; }
        pulse();
      }, o.idleEvery * (0.8 + Math.random() * 0.4));
    }
    if (o.hoverPulse && !reduced) {
      var hp = function () { if (Date.now() - lastPulse > 2500) pulse(); };
      host.addEventListener("pointerenter", hp); host.addEventListener("focusin", hp);
    }
    if ("IntersectionObserver" in global) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(host);

    var seen = false;
    try { seen = global.localStorage.getItem(o.storageKey) === "1"; } catch (e) {}
    var play = !reduced && (o.intro === "always" || (o.intro === "first-visit" && !seen));
    if (play) { try { global.localStorage.setItem(o.storageKey, "1"); } catch (e) {} intro(); }
    else { rest(); schedule(); }

    return {
      replay: function () { if (!reduced) intro(); },
      pulse: pulse,
      destroy: function () { dead = true; clear(); svg.remove(); }
    };
  }
  global.QuantechLogo = { mount: mount };
})(window);
