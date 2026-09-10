/* Mittelfinger auf Reisen — Seiten-JS.
 *
 * Vier Aufgaben:
 *   1. die Orbit-Szene im Auftakt aufbauen (drei gegenläufige Icon-Ringe),
 *   2. die Karte auf Klick laden und den Ort markieren,
 *   3. Ortsliste und Blogübersicht aus daten.js ausgeben,
 *   4. Kleinkram: Jahreszahl, sanftes Einblenden.
 *
 * Die Orbit-Mechanik stammt aus der Waitlist-Hero-Vorlage. Dort baut React
 * das DOM auf, hier tut es diese Datei — die CSS-Variablen heißen gleich.
 */
(function () {
  "use strict";

  var LEAFLET_CSS = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css";
  var LEAFLET_JS = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js";
  var SPEICHER = "mar-karte-ok";

  /* ============================ Bausteine ============================== */

  /* Zwölf selbst gezeichnete Reise-Icons. Bewusst einfach gehalten: bei
     28 bis 36 Pixeln Kantenlänge zählt die Silhouette, nicht das Detail. */
  var ICONS = [
    '<path d="M12 3 3 20h18Z"/><path d="M12 3v17"/>',                                    /* Zelt */
    '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2.2 4.8-4.8 2.2 2.2-4.8Z"/>',      /* Kompass */
    '<path d="M2 19 9 7l3.6 5.4L15 9l7 10Z"/>',                                           /* Berg */
    '<path d="M2 9c2.5-3 5.5-3 8 0s5.5 3 8 0"/><path d="M2 15c2.5-3 5.5-3 8 0s5.5 3 8 0"/>', /* Welle */
    '<circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.6M12 19.4V22M2 12h2.6M19.4 12H22M4.9 4.9l1.9 1.9M17.2 17.2l1.9 1.9M19.1 4.9l-1.9 1.9M6.8 17.2l-1.9 1.9"/>', /* Sonne */
    '<circle cx="6" cy="18" r="2.6"/><circle cx="18" cy="6" r="2.6"/><path d="M8.6 18H13a4 4 0 0 0 0-8h-2a4 4 0 0 1 0-8h4.4"/>', /* Route */
    '<path d="M4 8h12v6a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4Z"/><path d="M16 10h1.6a2.6 2.6 0 0 1 0 5.2H16"/><path d="M7.5 2.5v2M11.5 2.5v2"/>', /* Kaffee */
    '<rect x="2" y="7" width="16" height="9" rx="2.2"/><path d="M18 10h2.2l1.8 3v3H18"/><circle cx="7" cy="18" r="1.9"/><circle cx="17" cy="18" r="1.9"/>', /* Camper */
    '<path d="M12 3 7 11h10Z"/><path d="M12 8.5 6 17h12Z"/><path d="M12 17v4"/>',         /* Baum */
    '<path d="M9 3 3 6v15l6-3 6 3 6-3V3l-6 3Z"/><path d="M9 3v15M15 6v15"/>',             /* Landkarte */
    '<ellipse cx="8" cy="8" rx="2.7" ry="4.2"/><ellipse cx="16" cy="15.5" rx="2.7" ry="4.2"/>', /* Fußspuren */
    '<rect x="2.5" y="7" width="19" height="12" rx="2.6"/><circle cx="12" cy="13" r="3.4"/><path d="m9 7 1.2-2.6h3.6L15 7"/>' /* Kamera */
  ];

  /* Kachelfarben: Türkis, Mint, Lavendel, Flieder, Violett, Weiß. */
  var TOENE = [
    { flaeche: "#5eead4", tinte: "#04302c" },
    { flaeche: "#ddd6fe", tinte: "#2e1065" },
    { flaeche: "#2dd4bf", tinte: "#042f2e" },
    { flaeche: "#c4b5fd", tinte: "#2e1065" },
    { flaeche: "#ffffff", tinte: "#18122b" },
    { flaeche: "#a78bfa", tinte: "#1e1b4b" }
  ];

  /* Ringe wie in der Vorlage: außen groß, langsam, unscharf und blass. */
  var RINGE = [
    { durchmesser: 1060, dauer: 72, unschaerfe: 5, deckkraft: 0.3,  anzahl: 9, versatz: 0,  kachel: 74 },
    { durchmesser: 760,  dauer: 54, unschaerfe: 2, deckkraft: 0.55, anzahl: 8, versatz: 6,  kachel: 66 },
    { durchmesser: 470,  dauer: 38, unschaerfe: 0, deckkraft: 0.88, anzahl: 7, versatz: 13, kachel: 58 }
  ];

  /* Der Mittelfinger — Markenzeichen, Kartenmarkierung, Fußzeile. */
  function fingerSvg(groesse, farbe) {
    return (
      '<svg viewBox="0 0 40 52" width="' + groesse + '" height="' + groesse +
      '" fill="' + (farbe || "currentColor") + '" aria-hidden="true">' +
      '<rect x="16" y="2" width="8" height="26" rx="4"/>' +
      '<rect x="7" y="15" width="7.5" height="14" rx="3.75"/>' +
      '<rect x="25.5" y="15" width="7.5" height="14" rx="3.75"/>' +
      '<rect x="5" y="26" width="30" height="23" rx="9"/>' +
      "</svg>"
    );
  }

  /* ============================== Helfer =============================== */

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }
  function orte() { return Array.isArray(window.ORTE) ? window.ORTE : []; }
  function beitraege() { return Array.isArray(window.BEITRAEGE) ? window.BEITRAEGE : []; }

  function datumDe(iso) {
    if (!iso) return "";
    var d = new Date(iso + "T12:00:00");
    if (isNaN(d.getTime())) return iso;
    return d.toLocaleDateString("de-DE", { day: "2-digit", month: "long", year: "numeric" });
  }

  function koordText(o) {
    return Math.abs(o.lat).toFixed(4) + "° " + (o.lat >= 0 ? "N" : "S") + "   " +
           Math.abs(o.lng).toFixed(4) + "° " + (o.lng >= 0 ? "O" : "W");
  }

  function el(tag, klasse, text) {
    var n = document.createElement(tag);
    if (klasse) n.className = klasse;
    if (text != null) n.textContent = text;
    return n;
  }

  /* ============================ Orbit-Szene ============================ */
  function orbit() {
    var szene = document.querySelector(".orbit-plane");
    if (!szene) return;

    RINGE.forEach(function (ring, ringIndex) {
      var ringEl = el("div", "orbit-ring");
      ringEl.style.setProperty("--diameter", ring.durchmesser + "px");
      ringEl.style.setProperty("--duration", ring.dauer + "s");
      ringEl.style.setProperty("--ring-blur", ring.unschaerfe + "px");
      ringEl.style.setProperty("--ring-opacity", ring.deckkraft);

      for (var i = 0; i < ring.anzahl; i++) {
        var winkel = (360 / ring.anzahl) * i + ringIndex * 14;
        var icon = ICONS[(ring.versatz + i) % ICONS.length];
        var ton = TOENE[(ring.versatz + i) % TOENE.length];

        var anker = el("div", "orbit-anchor");
        anker.style.setProperty("--angle", winkel + "deg");
        anker.style.setProperty("--counter-angle", -winkel + "deg");
        anker.style.setProperty("--radius", ring.durchmesser / 2 + "px");
        anker.style.setProperty("--tile-size", ring.kachel + "px");
        anker.style.setProperty("--float-delay", -(i * 0.37) + "s");

        var kachel = el("span", "orbit-tile");
        kachel.style.background = ton.flaeche;
        kachel.style.color = ton.tinte;
        kachel.innerHTML =
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" ' +
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + icon + "</svg>";

        anker.appendChild(kachel);
        ringEl.appendChild(anker);
      }
      szene.appendChild(ringEl);
    });
  }

  /* ============================= Fingermarken ========================== */
  function fingermarken() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-finger]"), function (n) {
      n.innerHTML = fingerSvg(n.getAttribute("data-finger") || 32);
    });
  }

  /* ============================== Ortsliste ============================ */
  function ortsliste() {
    var ziel = document.querySelector("[data-orte]");
    if (!ziel) return;
    ziel.innerHTML = "";

    orte().forEach(function (o) {
      var li = el("li", "ort");

      var marke = el("div", "ort__marke");
      marke.innerHTML = fingerSvg(24, "#ffffff");
      li.appendChild(marke);

      var text = el("div");
      var h = el("h3");
      h.appendChild(document.createTextNode(o.name + " — " + o.land));
      if (o.start) h.appendChild(el("span", "ort__start", "Start"));
      text.appendChild(h);
      text.appendChild(el("p", "koord", koordText(o) + (o.datum ? "   ·   " + datumDe(o.datum) : "")));
      if (o.kurz) text.appendChild(el("p", null, o.kurz));
      li.appendChild(text);

      ziel.appendChild(li);
    });
  }

  /* ============================ Blogübersicht ========================== */
  function blogliste() {
    var ziel = document.querySelector("[data-beitraege]");
    if (!ziel) return;
    ziel.innerHTML = "";

    var liste = beitraege().slice().sort(function (a, b) {
      return (b.datum || "").localeCompare(a.datum || "");
    });

    if (!liste.length) {
      var leer = el("li");
      leer.appendChild(el("p", "leer", "Noch kein Beitrag. Der erste kommt, sobald der Camper rollt."));
      ziel.appendChild(leer);
      return;
    }

    liste.forEach(function (b) {
      var li = el("li");
      var a = el("a", "beitrag-karte");
      a.href = b.datei;

      var meta = el("div", "beitrag-karte__meta");
      if (b.ort) meta.appendChild(el("span", null, b.ort));
      if (b.datum) meta.appendChild(el("span", null, datumDe(b.datum)));
      a.appendChild(meta);

      a.appendChild(el("h3", null, b.titel));
      if (b.teaser) a.appendChild(el("p", null, b.teaser));
      a.appendChild(el("span", "beitrag-karte__mehr", "Weiterlesen →"));

      li.appendChild(a);
      ziel.appendChild(li);
    });
  }

  /* ================================ Karte ============================== */
  /* Kartenkacheln kommen von OpenStreetMap, Leaflet von einem CDN. Beides
     sind fremde Server, die dabei die IP-Adresse sehen — deshalb lädt die
     Karte erst nach einem Klick. Die Entscheidung bleibt lokal im Browser. */

  function ladeDatei(tag, attrs) {
    return new Promise(function (fertig, fehler) {
      var n = document.createElement(tag);
      Object.keys(attrs).forEach(function (k) { n.setAttribute(k, attrs[k]); });
      n.onload = function () { fertig(); };
      n.onerror = function () { fehler(new Error("laden fehlgeschlagen")); };
      document.head.appendChild(n);
    });
  }

  function karteZeichnen(box) {
    var liste = orte().filter(function (o) {
      return typeof o.lat === "number" && typeof o.lng === "number";
    });
    if (!liste.length) return;

    var karte = L.map(box, { scrollWheelZoom: false });
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: "Karte: &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a>-Mitwirkende"
    }).addTo(karte);

    var marker = liste.map(function (o) {
      /* Die Markierung ist der Finger selbst, kein Standard-Pin. */
      var icon = L.divIcon({
        className: "",
        html:
          '<span style="display:grid;place-items:center;width:44px;height:44px;' +
          'border-radius:14px;background:#5b21b6;border:2px solid #14b8a6;' +
          'box-shadow:0 10px 24px rgba(24,18,43,.45)">' +
          fingerSvg(24, "#ffffff") + "</span>",
        iconSize: [44, 44],
        iconAnchor: [22, 44],
        popupAnchor: [0, -40]
      });

      var m = L.marker([o.lat, o.lng], { icon: icon, title: o.name + ", " + o.land }).addTo(karte);

      var inhalt = document.createElement("div");
      inhalt.appendChild(el("h3", null, o.name + " — " + o.land));
      inhalt.appendChild(el("p", null, o.kurz || koordText(o)));
      m.bindPopup(inhalt, { maxWidth: 280 });
      return m;
    });

    if (marker.length === 1) {
      karte.setView(marker[0].getLatLng(), 11);
      marker[0].openPopup();
    } else {
      karte.fitBounds(L.featureGroup(marker).getBounds().pad(0.25));
    }
    karte.once("focus", function () { karte.scrollWheelZoom.enable(); });
  }

  function karteLaden(wrap) {
    var box = wrap.querySelector("#karte-flaeche");
    var tor = wrap.querySelector(".karte-consent");
    if (!box) return;
    if (tor) tor.innerHTML = '<p role="status">Karte wird geladen …</p>';

    Promise.all([
      ladeDatei("link", { rel: "stylesheet", href: LEAFLET_CSS }),
      ladeDatei("script", { src: LEAFLET_JS })
    ]).then(function () {
      if (tor) tor.remove();
      karteZeichnen(box);
    }).catch(function () {
      if (tor) {
        tor.innerHTML = "";
        tor.appendChild(el("p", "karte-fehler",
          "Die Karte lässt sich gerade nicht laden — vermutlich blockiert etwas die Verbindung. " +
          "Der Ort steht direkt darunter."));
      }
    });
  }

  function karte() {
    var wrap = document.querySelector(".karte-wrap");
    if (!wrap) return;
    var knopf = wrap.querySelector("[data-karte-laden]");
    var schonOk = false;
    try { schonOk = localStorage.getItem(SPEICHER) === "1"; } catch (e) { /* privater Modus */ }

    if (schonOk) { karteLaden(wrap); return; }
    if (!knopf) return;
    knopf.addEventListener("click", function () {
      try { localStorage.setItem(SPEICHER, "1"); } catch (e) { /* egal */ }
      karteLaden(wrap);
    });
  }

  /* =============================== Kleinkram =========================== */
  function jahr() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-jahr]"), function (n) {
      n.textContent = new Date().getFullYear();
    });
  }

  ready(function () {
    orbit();
    fingermarken();
    ortsliste();
    blogliste();
    karte();
    jahr();
  });
})();
