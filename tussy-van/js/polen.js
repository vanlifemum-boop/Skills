/* Polen-Serie: animierte Polen-Karte + Regionen-/Kategorie-Filter + Suche + Legende.
   Neue Orte einfach in POLEN_DATA ergänzen — Karte, Filter, Suche und Legende
   aktualisieren sich automatisch.
   Felder je Ort:
     id, name, short, region (Schlüssel aus POLEN_REGIONS),
     kat  = Kategorie-Schlüssel aus POLEN_KATEGORIEN (Emoji-Icon auf dem Marker),
     status = "bericht" (💛 eigener Reisebericht) | "sehenswert" (🔵 neutrale Info) | "ziel" (⚪ Reiseziel),
     x, y (Koordinaten der Europakarte 0..820/0..940), lx/ly = Label-Versatz,
     url, blurb, meta.
   Koordinaten neuer Orte per Formel aus realer lon/lat:
     x = 13.758*lon − 0.761*lat + 311.25 ;  y = −1.117*lon − 22.948*lat + 1625.66 */
window.POLEN_DATA = [
  {
    id: "danzig", name: "Danzig / Gdańsk", short: "Danzig", region: "norden",
    kat: "stadt", status: "bericht",
    x: 528, y: 358, lx: 9, ly: -1,
    url: "blog/danzig-ehrlich-dreistadt-bernstein.html", meta: "Norden & Ostsee · 7 Min.",
    blurb: "Traumhafte Altstadt, viel grauer Beton, die Dreistadt mit Sopot & Gdynia — plus Bernstein- und WWII-Museum."
  },
  {
    id: "kolberg", name: "Kołobrzeg", short: "Kolberg", region: "norden",
    kat: "stadt", status: "ziel",
    x: 483.8, y: 365.1, lx: 9, ly: -1,
    url: "reiseziele.html#kolberg", meta: "Norden & Ostsee",
    blurb: "Weiße Ostseestrände, Kiefernwälder und der beste Sonnenuntergang direkt vor der Schiebetür."
  },
  {
    id: "posen", name: "Posen / Poznań", short: "Posen", region: "westen",
    kat: "stadt", status: "ziel",
    x: 503.9, y: 403.3, lx: -9, ly: -1,
    url: "reiseziele.html#posen", meta: "Westen",
    blurb: "Prachtvoller Marktplatz mit den kämpfenden Ziegenböckchen am Rathaus — Charme-Zwischenstopp."
  },
  {
    id: "breslau", name: "Breslau / Wrocław", short: "Breslau", region: "westen",
    kat: "stadt", status: "ziel",
    x: 507.4, y: 431.9, lx: -9, ly: 3,
    url: "reiseziele.html#breslau", meta: "Westen",
    blurb: "Bunte Altstadt, romantische Dominsel und über 300 versteckte Bronze-Zwerge zum Suchen."
  },
  {
    id: "warschau", name: "Warschau", short: "Warschau", region: "zentral",
    kat: "stadt", status: "bericht",
    x: 559.3, y: 402.1, lx: 9, ly: -1,
    url: "blog/warschau-goldene-gans-museumsnacht.html", meta: "Zentralpolen · 7 Min.",
    blurb: "Die Legende der Goldenen Gans, Stalins Kulturpalast mit 360-Grad-Blick, die Nacht der Museen & der BUW-Dachgarten."
  },
  {
    id: "tschenstochau", name: "Częstochowa", short: "Tschenstochau", region: "sueden",
    kat: "stadt", status: "bericht",
    x: 533, y: 445, lx: -9, ly: -1,
    url: "blog/tschenstochau-schwarze-madonna.html", meta: "Süden · 6 Min.",
    blurb: "Die Schwarze Madonna auf dem Klosterberg Jasna Góra und die charmante Altstadt gleich nebenan."
  },
  {
    id: "krakau", name: "Kraków", short: "Krakau", region: "sueden",
    kat: "stadt", status: "bericht",
    x: 550, y: 451.5, lx: 9, ly: 4,
    url: "blog/krakau-tuchhallen-drache.html", meta: "Süden · 6 Min.",
    blurb: "Tuchhallen, süße Markt-Sünden einer älteren Dame und der feuerspuckende Wawel-Drache samt Legende."
  },
  {
    id: "masuren", name: "Masuren / Mazury", short: "Masuren", region: "masuren",
    kat: "natur", status: "sehenswert",
    x: 567.1, y: 367, lx: 9, ly: -1,
    url: "reiseziele.html#masuren", meta: "Masuren · Natur & Aussicht",
    blurb: "Polens großes Seenland im Nordosten: über 2.000 Seen, Wälder und Kanäle — ein Traum zum Segeln, Kanufahren und für Natur pur. Eines der beliebtesten Reiseziele des Landes."
  }
];

window.POLEN_REGIONS = [
  { key: "alle", label: "Alle Regionen" },
  { key: "norden", label: "Norden & Ostsee" },
  { key: "masuren", label: "Masuren" },
  { key: "zentral", label: "Zentralpolen" },
  { key: "westen", label: "Westen" },
  { key: "sueden", label: "Süden" }
];

/* Kategorien-Legende (Icon + Label), zwei Gruppen — an wyprawomaniak.pl angelehnt. */
window.POLEN_KATEGORIEN = [
  { group: "🔎 Sehenswertes", items: [
    { key: "stadt",    icon: "🏙️", label: "Städte & Regionen" },
    { key: "sehens",   icon: "ℹ️", label: "Sehenswürdigkeiten" },
    { key: "museum",   icon: "🏛️", label: "Museen & Gedenkstätten" },
    { key: "burg",     icon: "🏰", label: "Burgen & Schlösser" },
    { key: "sakral",   icon: "⛪", label: "Kirchen, Klöster & Wallfahrt" },
    { key: "natur",    icon: "🏞️", label: "Natur & Aussicht" },
    { key: "sonstige", icon: "⭐", label: "Sonstige Highlights" }
  ]},
  { group: "🚐 Für Camper", items: [
    { key: "camping",       icon: "⛺", label: "Campingplatz" },
    { key: "biwak",         icon: "🏕️", label: "Wildes Biwak / Naturplatz" },
    { key: "waldpark",      icon: "🅿️", label: "Waldparkplatz" },
    { key: "rastplatz",     icon: "🛣️", label: "Rastplatz (MOP)" },
    { key: "dusche",        icon: "🚿", label: "Dusche" },
    { key: "entsorgung",    icon: "🚽", label: "Ver-/Entsorgung" },
    { key: "werkstatt",     icon: "🔧", label: "Camper-Werkstatt" },
    { key: "waschsalon",    icon: "🧺", label: "Waschsalon" },
    { key: "camperservice", icon: "🆑", label: "Camper-Service (CS)" }
  ]}
];

window.POLEN_STATUS = {
  bericht:    { label: "Mein Reisebericht", tag: "terra" },
  sehenswert: { label: "Sehenswertes",      tag: "blue" },
  ziel:       { label: "Reiseziel",         tag: "" }
};

(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var data = window.POLEN_DATA || [];
  var STATUS = window.POLEN_STATUS;

  // Kategorie-Lookup key -> {icon,label}
  var KAT = {};
  (window.POLEN_KATEGORIEN || []).forEach(function (grp) {
    grp.items.forEach(function (it) { KAT[it.key] = it; });
  });

  var state = { region: "alle", kats: {}, query: "" }; // kats: Set als Objekt, leer = alle

  var mapStage = document.querySelector("[data-pl-map]");
  var grid = document.querySelector("[data-pl-grid]");
  var regRow = document.querySelector("[data-pl-filter]");
  var katRow = document.querySelector("[data-pl-catfilter]");
  var legendBox = document.querySelector("[data-pl-legende]");
  var search = document.querySelector("[data-pl-search]");
  var count = document.querySelector("[data-pl-count]");
  if (!grid) return;

  function katMeta(k) { return KAT[k] || { icon: "📍", label: k || "Ort" }; }
  function noKatFilter() { return Object.keys(state.kats).length === 0; }

  /* --- Kacheln (Beiträge / Ziele) rendern --- */
  data.forEach(function (d) {
    var km = katMeta(d.kat);
    var st = STATUS[d.status] || STATUS.ziel;
    var a = document.createElement("a");
    a.className = "post-card";
    a.id = "pl-card-" + d.id;
    a.href = d.url;
    a.setAttribute("data-region", d.region);
    a.setAttribute("data-kat", d.kat || "");
    a.setAttribute("data-text", (d.name + " " + d.blurb + " " + d.meta + " " + km.label).toLowerCase());
    var badge = d.status === "ziel" ? " · bald mehr" : "";
    a.innerHTML =
      '<span class="cat sticker ' + st.tag + '">' + km.icon + " " + st.label + badge + "</span>" +
      "<h3>" + d.name + "</h3>" +
      "<p>" + d.blurb + "</p>" +
      '<span class="meta">' + d.meta + "</span>";
    grid.appendChild(a);
  });

  /* --- Regionen-Chips (Einfachauswahl) --- */
  if (regRow) {
    (window.POLEN_REGIONS || []).forEach(function (r) {
      var has = r.key === "alle" || data.some(function (d) { return d.region === r.key; });
      if (!has) return;
      var b = document.createElement("button");
      b.className = "chip" + (r.key === "alle" ? " active" : "");
      b.textContent = r.label;
      b.setAttribute("data-region", r.key);
      b.addEventListener("click", function () {
        state.region = r.key;
        regRow.querySelectorAll(".chip").forEach(function (c) { c.classList.remove("active"); });
        b.classList.add("active");
        apply();
      });
      regRow.appendChild(b);
    });
  }

  /* --- Kategorie-Chips (Mehrfachauswahl, nur vorhandene Kategorien) --- */
  if (katRow) {
    var present = [];
    (window.POLEN_KATEGORIEN || []).forEach(function (grp) {
      grp.items.forEach(function (it) {
        if (data.some(function (d) { return d.kat === it.key; })) present.push(it);
      });
    });
    present.forEach(function (it) {
      var b = document.createElement("button");
      b.className = "chip chip-kat";
      b.innerHTML = it.icon + " " + it.label;
      b.setAttribute("data-kat", it.key);
      b.addEventListener("click", function () {
        if (state.kats[it.key]) { delete state.kats[it.key]; b.classList.remove("active"); }
        else { state.kats[it.key] = true; b.classList.add("active"); }
        apply();
      });
      katRow.appendChild(b);
    });
  }

  /* --- Legende rendern --- */
  if (legendBox) {
    var html = '<div class="pl-legende-status">' +
      '<span><i class="pl-dot bericht"></i> 💛 mein Reisebericht</span>' +
      '<span><i class="pl-dot sehenswert"></i> Sehenswertes</span>' +
      '<span><i class="pl-dot ziel"></i> Reiseziel</span>' +
      '</div>';
    (window.POLEN_KATEGORIEN || []).forEach(function (grp) {
      html += '<div class="pl-legende-grp"><b>' + grp.group + '</b><ul>';
      grp.items.forEach(function (it) {
        html += '<li><span class="pl-lg-icon">' + it.icon + '</span>' + it.label + "</li>";
      });
      html += "</ul></div>";
    });
    legendBox.innerHTML = html;
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
      var okKat = noKatFilter() || !!state.kats[d.kat];
      var okQuery = !state.query || card.getAttribute("data-text").indexOf(state.query) !== -1;
      var show = okRegion && okKat && okQuery;
      card.classList.toggle("hide", !show);
      if (show) visible++;
      var pin = document.getElementById("pl-pin-" + d.id);
      if (pin) pin.classList.toggle("dim", !show);
    });
    if (count) count.textContent = visible + (visible === 1 ? " Ort" : " Orte") + " gefunden";
    var empty = document.querySelector(".pl-empty");
    if (empty) empty.style.display = visible ? "none" : "block";
  }

  function resetFilters() {
    state.region = "alle"; state.kats = {}; state.query = "";
    if (search) search.value = "";
    if (regRow) regRow.querySelectorAll(".chip").forEach(function (x) {
      x.classList.toggle("active", x.getAttribute("data-region") === "alle");
    });
    if (katRow) katRow.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("active"); });
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
        var km = katMeta(d.kat);
        var g = document.createElementNS(NS, "g");
        g.setAttribute("class", "pl-pin " + (d.status || "ziel"));
        g.setAttribute("id", "pl-pin-" + d.id);
        g.setAttribute("transform", "translate(" + d.x + "," + d.y + ")");

        var c = document.createElementNS(NS, "circle");
        c.setAttribute("class", "pl-pin-bg");
        c.setAttribute("r", "8.5");
        g.appendChild(c);

        var icon = document.createElementNS(NS, "text");
        icon.setAttribute("class", "pl-icon");
        icon.setAttribute("text-anchor", "middle");
        icon.setAttribute("y", "3.4");
        icon.textContent = km.icon;
        g.appendChild(icon);

        var title = document.createElementNS(NS, "title");
        var stLabel = (STATUS[d.status] || STATUS.ziel).label;
        title.textContent = d.name + " — " + km.label + " (" + stLabel + ")";
        g.appendChild(title);

        var right = (d.lx || 9) > 0;
        var t = document.createElementNS(NS, "text");
        t.setAttribute("class", "pl-lbl");
        t.setAttribute("x", right ? 11 : -11);
        t.setAttribute("y", (d.ly || 0) + 2.2);
        t.setAttribute("text-anchor", right ? "start" : "end");
        t.textContent = d.short || d.name;
        g.appendChild(t);

        g.style.cursor = "pointer";
        g.addEventListener("click", function () {
          var card = document.getElementById("pl-card-" + d.id);
          if (!card) return;
          resetFilters();
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
