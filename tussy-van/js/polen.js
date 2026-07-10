/* Polen-Serie: animierte Polen-Karte + Regionen-Filter + Suche.
   Neue Orte/Beiträge einfach in POLEN_DATA ergänzen — Karte, Filter und Suche
   aktualisieren sich automatisch. x/y sind die Koordinaten aus der Europakarte
   (img/europe-map.svg, viewBox 0 0 820 940). lx/ly = optionaler Label-Versatz. */
window.POLEN_DATA = [
  {
    id: "danzig", name: "Danzig / Gdańsk", short: "Danzig", region: "norden",
    x: 528, y: 358, lx: 9, ly: -1,
    url: "blog/danzig-ehrlich-dreistadt-bernstein.html", hasPost: true,
    cat: "Reisebericht", meta: "Norden & Ostsee · 7 Min.",
    blurb: "Traumhafte Altstadt, viel grauer Beton, die Dreistadt mit Sopot & Gdynia — plus Bernstein- und WWII-Museum."
  },
  {
    id: "kolberg", name: "Kołobrzeg", short: "Kolberg", region: "norden",
    x: 483.8, y: 365.1, lx: 9, ly: -1,
    url: "reiseziele.html#kolberg", hasPost: false,
    cat: "Reiseziel", meta: "Norden & Ostsee",
    blurb: "Weiße Ostseestrände, Kiefernwälder und der beste Sonnenuntergang direkt vor der Schiebetür."
  },
  {
    id: "posen", name: "Posen / Poznań", short: "Posen", region: "westen",
    x: 503.9, y: 403.3, lx: -9, ly: -1,
    url: "reiseziele.html#posen", hasPost: false,
    cat: "Reiseziel", meta: "Westen",
    blurb: "Prachtvoller Marktplatz mit den kämpfenden Ziegenböckchen am Rathaus — Charme-Zwischenstopp."
  },
  {
    id: "breslau", name: "Breslau / Wrocław", short: "Breslau", region: "westen",
    x: 507.4, y: 431.9, lx: -9, ly: 3,
    url: "reiseziele.html#breslau", hasPost: false,
    cat: "Reiseziel", meta: "Westen",
    blurb: "Bunte Altstadt, romantische Dominsel und über 300 versteckte Bronze-Zwerge zum Suchen."
  },
  {
    id: "warschau", name: "Warschau", short: "Warschau", region: "zentral",
    x: 559.3, y: 402.1, lx: 9, ly: -1,
    url: "blog/warschau-goldene-gans-museumsnacht.html", hasPost: true,
    cat: "Reisebericht", meta: "Zentralpolen · 7 Min.",
    blurb: "Die Legende der Goldenen Gans, Stalins Kulturpalast mit 360-Grad-Blick, die Nacht der Museen & der BUW-Dachgarten."
  },
  {
    id: "tschenstochau", name: "Częstochowa", short: "Tschenstochau", region: "sueden",
    x: 533, y: 445, lx: -9, ly: -1,
    url: "blog/tschenstochau-schwarze-madonna.html", hasPost: true,
    cat: "Reisebericht", meta: "Süden · 6 Min.",
    blurb: "Die Schwarze Madonna auf dem Klosterberg Jasna Góra und die charmante Altstadt gleich nebenan."
  },
  {
    id: "krakau", name: "Kraków", short: "Krakau", region: "sueden",
    x: 550, y: 451.5, lx: 9, ly: 4,
    url: "blog/krakau-tuchhallen-drache.html", hasPost: true,
    cat: "Reisebericht", meta: "Süden · 6 Min.",
    blurb: "Tuchhallen, süße Markt-Sünden einer älteren Dame und der feuerspuckende Wawel-Drache samt Legende."
  }
];

window.POLEN_REGIONS = [
  { key: "alle", label: "Alle Regionen" },
  { key: "norden", label: "Norden & Ostsee" },
  { key: "zentral", label: "Zentralpolen" },
  { key: "westen", label: "Westen" },
  { key: "sueden", label: "Süden" }
];

(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var data = window.POLEN_DATA || [];
  var state = { region: "alle", query: "" };

  var mapStage = document.querySelector("[data-pl-map]");
  var grid = document.querySelector("[data-pl-grid]");
  var chipRow = document.querySelector("[data-pl-filter]");
  var search = document.querySelector("[data-pl-search]");
  var count = document.querySelector("[data-pl-count]");
  if (!grid) return;

  /* --- Karten (Beiträge/Reiseziele) rendern --- */
  data.forEach(function (d) {
    var a = document.createElement("a");
    a.className = "post-card";
    a.id = "pl-card-" + d.id;
    a.href = d.url;
    a.setAttribute("data-region", d.region);
    a.setAttribute("data-text", (d.name + " " + d.blurb + " " + d.meta).toLowerCase());
    var catClass = d.hasPost ? "cat sticker terra" : "cat sticker blue";
    a.innerHTML =
      '<span class="' + catClass + '">' + d.cat + (d.hasPost ? "" : " · bald mehr") + "</span>" +
      "<h3>" + d.name + "</h3>" +
      "<p>" + d.blurb + "</p>" +
      '<span class="meta">' + d.meta + "</span>";
    grid.appendChild(a);
  });

  /* --- Regionen-Chips rendern --- */
  if (chipRow) {
    (window.POLEN_REGIONS || []).forEach(function (r) {
      var has = r.key === "alle" || data.some(function (d) { return d.region === r.key; });
      if (!has) return;
      var b = document.createElement("button");
      b.className = "chip" + (r.key === "alle" ? " active" : "");
      b.textContent = r.label;
      b.setAttribute("data-region", r.key);
      b.addEventListener("click", function () {
        state.region = r.key;
        chipRow.querySelectorAll(".chip").forEach(function (c) { c.classList.remove("active"); });
        b.classList.add("active");
        apply();
      });
      chipRow.appendChild(b);
    });
  }

  /* --- Suche --- */
  if (search) {
    search.addEventListener("input", function () {
      state.query = search.value.trim().toLowerCase();
      apply();
    });
  }

  function apply() {
    var visible = 0;
    data.forEach(function (d) {
      var card = document.getElementById("pl-card-" + d.id);
      var okRegion = state.region === "alle" || d.region === state.region;
      var okQuery = !state.query || card.getAttribute("data-text").indexOf(state.query) !== -1;
      var show = okRegion && okQuery;
      card.classList.toggle("hide", !show);
      if (show) visible++;
      var pin = document.getElementById("pl-pin-" + d.id);
      if (pin) pin.classList.toggle("dim", !show);
    });
    if (count) {
      count.textContent = visible + (visible === 1 ? " Ort" : " Orte") + " gefunden";
    }
    var empty = document.querySelector(".pl-empty");
    if (empty) empty.style.display = visible ? "none" : "block";
  }

  /* --- Animierte Polen-Karte aus der Europakarte ableiten --- */
  if (mapStage) {
    fetch(mapStage.getAttribute("data-pl-map")).then(function (r) { return r.text(); }).then(function (svgText) {
      var holder = document.createElement("div");
      holder.innerHTML = svgText;
      var svg = holder.querySelector("svg");
      svg.setAttribute("class", "pl-map");
      svg.setAttribute("viewBox", "450 332 182 162"); // auf Polen zugeschnitten (mit Rand für Beschriftung)
      var pl = svg.querySelector("#c-PL");
      if (pl) pl.classList.add("pl");
      mapStage.appendChild(svg);

      data.forEach(function (d) {
        var g = document.createElementNS(NS, "g");
        g.setAttribute("class", "pl-pin " + (d.hasPost ? "has-post" : "no-post"));
        g.setAttribute("id", "pl-pin-" + d.id);
        g.setAttribute("transform", "translate(" + d.x + "," + d.y + ")");
        var c = document.createElementNS(NS, "circle");
        c.setAttribute("r", "5.5");
        g.appendChild(c);
        var title = document.createElementNS(NS, "title");
        title.textContent = d.name + (d.hasPost ? " — Beitrag lesen" : " — Reiseziel");
        g.appendChild(title);
        var right = (d.lx || 9) > 0;
        var t = document.createElementNS(NS, "text");
        t.setAttribute("class", "pl-lbl");
        t.setAttribute("x", right ? 8 : -8);
        t.setAttribute("y", (d.ly || 0) + 2.2);
        t.setAttribute("text-anchor", right ? "start" : "end");
        t.textContent = d.short || d.name;
        g.appendChild(t);
        g.style.cursor = "pointer";
        g.addEventListener("click", function () {
          var card = document.getElementById("pl-card-" + d.id);
          if (!card) return;
          // Filter zurücksetzen, damit die Karte sichtbar ist
          state.region = "alle"; state.query = "";
          if (search) search.value = "";
          if (chipRow) {
            chipRow.querySelectorAll(".chip").forEach(function (x) { x.classList.toggle("active", x.getAttribute("data-region") === "alle"); });
          }
          apply();
          svg.querySelectorAll(".pl-pin.active").forEach(function (p) { p.classList.remove("active"); });
          g.classList.add("active");
          card.classList.remove("flash");
          void card.offsetWidth;
          card.classList.add("flash");
          card.scrollIntoView({ behavior: "smooth", block: "center" });
        });
        svg.appendChild(g);
      });
    }).catch(function (err) { console.error("Polen-Karte konnte nicht geladen werden:", err); });
  }

  apply();
})();
