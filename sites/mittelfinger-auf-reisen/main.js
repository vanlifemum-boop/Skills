/* Mittelfinger auf Reisen — gemeinsames Seiten-JS.
 * Reveals (respektiert prefers-reduced-motion), mobiles Menü, aktiver
 * Navigationslink, Ortslisten aus orte.js, Reisekarte mit Einwilligung,
 * Formulare, Jahreszahl.
 */
(function () {
  "use strict";

  var LEAFLET_CSS = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css";
  var LEAFLET_JS = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js";

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function orte() {
    return Array.isArray(window.ORTE) ? window.ORTE : [];
  }

  function datumDe(iso) {
    if (!iso) return "";
    var d = new Date(iso + "T12:00:00");
    if (isNaN(d.getTime())) return iso;
    return d.toLocaleDateString("de-DE", { day: "2-digit", month: "long", year: "numeric" });
  }

  function koordText(o) {
    var ns = o.lat >= 0 ? "N" : "S";
    var ew = o.lng >= 0 ? "O" : "W";
    return Math.abs(o.lat).toFixed(4) + "° " + ns + "  " + Math.abs(o.lng).toFixed(4) + "° " + ew;
  }

  function el(tag, klasse, text) {
    var n = document.createElement(tag);
    if (klasse) n.className = klasse;
    if (text != null) n.textContent = text;
    return n;
  }

  /* ------------------------------- Reveals ------------------------------ */
  function reveals() {
    var els = document.querySelectorAll("[data-reveal]");
    var reduziert = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduziert || !("IntersectionObserver" in window) || !els.length) {
      Array.prototype.forEach.call(els, function (e) { e.classList.add("sichtbar"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("sichtbar");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    Array.prototype.forEach.call(els, function (e) { io.observe(e); });
  }

  /* ----------------------------- Mobiles Menü --------------------------- */
  function menue() {
    var burger = document.querySelector(".burger");
    var nav = document.querySelector(".nav");
    if (!burger || !nav) return;
    burger.addEventListener("click", function () {
      var offen = nav.classList.toggle("offen");
      burger.setAttribute("aria-expanded", offen ? "true" : "false");
      burger.textContent = offen ? "✕" : "☰";
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.classList.remove("offen");
        burger.setAttribute("aria-expanded", "false");
        burger.textContent = "☰";
      }
    });
  }

  /* -------------------------- Aktiven Link setzen ----------------------- */
  function aktiverLink() {
    var datei = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    Array.prototype.forEach.call(document.querySelectorAll(".nav a:not(.btn)"), function (a) {
      var ziel = (a.getAttribute("href") || "").split("#")[0].toLowerCase();
      if (ziel && ziel === datei) a.classList.add("aktiv");
    });
  }

  /* --------------------------- Ortsliste ausgeben ----------------------- */
  /* Steht in [data-orte]. Zugleich die Fassung, die bleibt, wenn jemand die
     Karte nicht lädt — die Orte sind also immer lesbar. */
  function ortsliste() {
    var ziele = document.querySelectorAll("[data-orte]");
    if (!ziele.length) return;
    Array.prototype.forEach.call(ziele, function (ziel) {
      var limit = parseInt(ziel.getAttribute("data-orte-limit") || "0", 10);
      var liste = orte().filter(function (o) { return !o.geplant; });
      liste.sort(function (a, b) { return (b.datum || "").localeCompare(a.datum || ""); });
      if (limit > 0) liste = liste.slice(0, limit);

      ziel.innerHTML = "";
      liste.forEach(function (o) {
        var li = el("li", "ort");
        var h = el("h3");
        h.textContent = o.name + " — " + o.land;
        li.appendChild(h);
        li.appendChild(el("p", "koord", koordText(o) + (o.datum ? "  ·  " + datumDe(o.datum) : "")));
        if (o.kurz) li.appendChild(el("p", null, o.kurz));
        if (o.scheissdrauf) {
          var sd = el("p");
          sd.appendChild(el("strong", null, "Scheiß-drauf-Moment: "));
          sd.appendChild(document.createTextNode(o.scheissdrauf));
          li.appendChild(sd);
        }
        if (o.camper) {
          var ct = el("p");
          ct.appendChild(el("strong", null, "Camper-Tipp: "));
          ct.appendChild(document.createTextNode(o.camper));
          li.appendChild(ct);
        }
        if (o.link) {
          var p = el("p");
          var a = el("a", null, "Ganzer Reisebericht →");
          a.href = o.link;
          p.appendChild(a);
          li.appendChild(p);
        }
        ziel.appendChild(li);
      });
    });
  }

  /* -------------------------- Nächster Stopp ---------------------------- */
  function naechsterStopp() {
    var ziele = document.querySelectorAll("[data-naechster-stopp]");
    if (!ziele.length) return;
    var o = orte().filter(function (x) { return x.geplant; })[0];
    Array.prototype.forEach.call(ziele, function (ziel) {
      ziel.textContent = o ? o.name + ", " + o.land : "steht noch nicht fest";
    });
  }

  /* ------------------------------- Karte -------------------------------- */
  /* Die Kartenkacheln kommen von OpenStreetMap, Leaflet von einem CDN.
     Beides sind fremde Server, die dabei die IP-Adresse sehen. Deshalb lädt
     die Karte erst nach einem Klick — und die Entscheidung wird lokal
     gemerkt, nicht an irgendwen gesendet. */
  var SPEICHER = "mar-karte-ok";

  function ladeDatei(tag, attrs) {
    return new Promise(function (aufloesen, ablehnen) {
      var n = document.createElement(tag);
      Object.keys(attrs).forEach(function (k) { n.setAttribute(k, attrs[k]); });
      n.onload = function () { aufloesen(); };
      n.onerror = function () { ablehnen(new Error("laden fehlgeschlagen")); };
      document.head.appendChild(n);
    });
  }

  function karteZeichnen(box) {
    var liste = orte().filter(function (o) { return typeof o.lat === "number" && typeof o.lng === "number"; });
    if (!liste.length) return;

    var karte = L.map(box, { scrollWheelZoom: false });
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: "Karte: &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a>-Mitwirkende"
    }).addTo(karte);

    var pins = liste.map(function (o) {
      var icon = L.divIcon({
        className: "",
        html:
          '<svg width="30" height="40" viewBox="0 0 30 40" aria-hidden="true">' +
          '<path d="M15 39C15 39 28 23.5 28 14A13 13 0 1 0 2 14c0 9.5 13 25 13 25Z" ' +
          'fill="' + (o.geplant ? "#f2c14e" : "#ff6a13") + '" stroke="#14161a" stroke-width="2.5"/>' +
          '<circle cx="15" cy="14" r="4.5" fill="#14161a"/></svg>',
        iconSize: [30, 40],
        iconAnchor: [15, 39],
        popupAnchor: [0, -34]
      });

      var m = L.marker([o.lat, o.lng], { icon: icon, title: o.name + ", " + o.land }).addTo(karte);

      var inhalt = document.createElement("div");
      var h = el("h3");
      h.textContent = o.name + " — " + o.land;
      inhalt.appendChild(h);
      inhalt.appendChild(el("p", "koord", koordText(o) + (o.datum ? "  ·  " + datumDe(o.datum) : "")));
      if (o.foto) {
        var bild = new Image();
        bild.src = o.foto;
        bild.alt = o.alt || (o.name + ", " + o.land);
        bild.loading = "lazy";
        bild.style.cssText = "border-radius:8px;margin:8px 0;max-height:170px;object-fit:cover;width:100%";
        inhalt.appendChild(bild);
      }
      if (o.kurz) inhalt.appendChild(el("p", null, o.kurz));
      if (o.scheissdrauf) {
        var sd = el("p");
        sd.appendChild(el("strong", null, "Scheiß-drauf-Moment: "));
        sd.appendChild(document.createTextNode(o.scheissdrauf));
        inhalt.appendChild(sd);
      }
      if (o.camper) {
        var ct = el("p");
        ct.appendChild(el("strong", null, "Camper-Tipp: "));
        ct.appendChild(document.createTextNode(o.camper));
        inhalt.appendChild(ct);
      }
      if (o.link) {
        var a = el("a", null, "Ganzer Reisebericht →");
        a.href = o.link;
        inhalt.appendChild(a);
      }
      m.bindPopup(inhalt, { maxWidth: 300 });
      return m;
    });

    karte.fitBounds(L.featureGroup(pins).getBounds().pad(0.25));
    karte.once("focus", function () { karte.scrollWheelZoom.enable(); });
  }

  function karteLaden(wrap) {
    var box = wrap.querySelector("#karte");
    var gate = wrap.querySelector(".karte-consent");
    if (!box) return;
    if (gate) gate.innerHTML = '<p role="status">Karte wird geladen …</p>';

    Promise.all([
      ladeDatei("link", { rel: "stylesheet", href: LEAFLET_CSS }),
      ladeDatei("script", { src: LEAFLET_JS })
    ]).then(function () {
      if (gate) gate.remove();
      karteZeichnen(box);
    }).catch(function () {
      if (gate) {
        gate.innerHTML = "";
        gate.appendChild(el("p", "karte-fehler",
          "Die Karte konnte nicht geladen werden — vermutlich blockiert etwas die Verbindung. " +
          "Alle Orte stehen als Liste direkt darunter."));
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

  /* ------------------------------ Formulare ----------------------------- */
  /* POSTet an data-endpoint (z. B. Formspree). Solange dort noch
     [PLATZHALTER] steht, wird das ehrlich gesagt statt Erfolg vorzutäuschen. */
  function formulare() {
    Array.prototype.forEach.call(document.querySelectorAll("form[data-endpoint]"), function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!form.reportValidity()) return;

        var endpoint = form.getAttribute("data-endpoint") || "";
        var echt = endpoint && endpoint.indexOf("PLATZHALTER") === -1;
        var fertig = function (ok) {
          var p = el("p", "form-hinweis");
          p.setAttribute("role", "status");
          p.textContent = ok
            ? "Angekommen. Ich melde mich — kann dauern, ich bin unterwegs."
            : echt
              ? "Das hat gerade nicht geklappt. Versuch es später noch einmal oder schreib mir direkt."
              : "Danke! Der Versand ist noch nicht eingerichtet — schreib mir so lange bitte direkt per E-Mail.";
          form.replaceWith(p);
          p.focus && p.focus();
        };

        if (!echt) { fertig(false); return; }

        fetch(endpoint, {
          method: "POST",
          headers: { Accept: "application/json" },
          body: new FormData(form)
        }).then(function (r) { fertig(r.ok); }).catch(function () { fertig(false); });
      });
    });
  }

  /* ---------------------------- Jahr im Footer -------------------------- */
  function jahr() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-jahr]"), function (n) {
      n.textContent = new Date().getFullYear();
    });
  }

  ready(function () {
    reveals();
    menue();
    aktiverLink();
    ortsliste();
    naechsterStopp();
    karte();
    formulare();
    jahr();
  });
})();
