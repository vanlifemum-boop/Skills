/* Europa-Entsorgungskarte: zeichnet die kuratierten Stationen aus
   entsorgung-europa-daten.js als Pins auf die Europakarte.
   Länder-Chips filtern die Pins und zoomen auf das Land. */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var stage = document.querySelector("[data-eu-map]");
  var chipRow = document.querySelector("[data-eu-filter]");
  var countEl = document.querySelector("[data-eu-count]");
  var data = window.EU_STATIONEN || [];
  var NAMEN = window.EU_LAENDER || {};
  if (!stage || !data.length) return;

  var VIEW_ALL = "55 120 530 610";
  var state = { cc: "alle" };

  fetch(stage.getAttribute("data-eu-map")).then(function (r) { return r.text(); }).then(function (svgText) {
    var holder = document.createElement("div");
    holder.innerHTML = svgText;
    var svg = holder.querySelector("svg");
    svg.setAttribute("class", "pl-map eu-map");
    svg.setAttribute("viewBox", VIEW_ALL);
    stage.appendChild(svg);

    // Länder mit Stationen hervorheben
    var laender = {};
    data.forEach(function (s) { laender[s.cc] = (laender[s.cc] || 0) + 1; });
    Object.keys(laender).forEach(function (cc) {
      var p = svg.querySelector("#c-" + cc);
      if (p) p.classList.add("eu-land");
    });

    // Pins
    data.forEach(function (s, i) {
      var g = document.createElementNS(NS, "g");
      g.setAttribute("class", "eu-pin");
      g.setAttribute("data-cc", s.cc);
      g.setAttribute("transform", "translate(" + s.x + "," + s.y + ")");
      var c = document.createElementNS(NS, "circle");
      c.setAttribute("r", "5");
      g.appendChild(c);
      var t = document.createElementNS(NS, "text");
      t.setAttribute("text-anchor", "middle");
      t.setAttribute("y", "2");
      t.textContent = "🚽";
      g.appendChild(t);
      var title = document.createElementNS(NS, "title");
      title.textContent = s.name + " — " + s.city + " (in Google Maps öffnen)";
      g.appendChild(title);
      g.addEventListener("click", function () {
        window.open("https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(s.q), "_blank", "noopener");
      });
      svg.appendChild(g);
    });

    // sanfter viewBox-Zoom
    var anim = null;
    function zoomTo(vb) {
      var from = svg.getAttribute("viewBox").split(" ").map(Number);
      var to = vb.split(" ").map(Number);
      var t0 = null;
      if (anim) cancelAnimationFrame(anim);
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / 350, 1);
        var e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
        svg.setAttribute("viewBox", from.map(function (f, i) { return f + (to[i] - f) * e; }).join(" "));
        if (p < 1) anim = requestAnimationFrame(step);
      }
      anim = requestAnimationFrame(step);
    }

    function landBox(cc) {
      var pins = data.filter(function (s) { return s.cc === cc; });
      var p = svg.querySelector("#c-" + cc);
      var b = p ? p.getBBox() : null;
      var x1 = b ? b.x : Infinity, y1 = b ? b.y : Infinity,
          x2 = b ? b.x + b.width : -Infinity, y2 = b ? b.y + b.height : -Infinity;
      pins.forEach(function (s) {
        x1 = Math.min(x1, s.x - 8); y1 = Math.min(y1, s.y - 8);
        x2 = Math.max(x2, s.x + 8); y2 = Math.max(y2, s.y + 8);
      });
      var m = 14, w = x2 - x1 + 2 * m, h = y2 - y1 + 2 * m;
      // Mindestgröße, damit kleine Länder nicht in Riesen-Pins ertrinken
      if (w < 90) { x1 -= (90 - w) / 2; w = 90; }
      if (h < 90) { y1 -= (90 - h) / 2; h = 90; }
      return (x1 - m) + " " + (y1 - m) + " " + w + " " + h;
    }

    function apply() {
      var visible = 0;
      svg.querySelectorAll(".eu-pin").forEach(function (g) {
        var show = state.cc === "alle" || g.getAttribute("data-cc") === state.cc;
        g.classList.toggle("off", !show);
        if (show) visible++;
      });
      if (countEl) {
        countEl.textContent = state.cc === "alle"
          ? data.length + " Stationen in " + Object.keys(laender).length + " Ländern — klick einen Pin, um ihn in Google Maps zu öffnen"
          : visible + (visible === 1 ? " Station" : " Stationen") + " · " + (NAMEN[state.cc] || state.cc);
      }
      zoomTo(state.cc === "alle" ? VIEW_ALL : landBox(state.cc));
    }

    // Chips
    if (chipRow) {
      var alle = document.createElement("button");
      alle.className = "chip active";
      alle.textContent = "Ganz Europa";
      alle.addEventListener("click", function () { setCC("alle", alle); });
      chipRow.appendChild(alle);
      Object.keys(NAMEN).forEach(function (cc) {
        if (!laender[cc]) return;
        var b = document.createElement("button");
        b.className = "chip";
        b.textContent = NAMEN[cc];
        b.addEventListener("click", function () { setCC(cc, b); });
        chipRow.appendChild(b);
      });
    }
    function setCC(cc, btn) {
      state.cc = cc;
      chipRow.querySelectorAll(".chip").forEach(function (c) { c.classList.remove("active"); });
      btn.classList.add("active");
      apply();
    }

    apply();
  }).catch(function (err) { console.error("Europakarte konnte nicht geladen werden:", err); });
})();
