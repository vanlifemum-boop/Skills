/* =========================================================
   MAL WIEDER NORMAL SEIN — gemeinsames Verhalten aller Seiten
   =========================================================
   Braucht daten.js davor. Alles hier ist eine Zugabe: Fällt das
   Skript aus, bleibt jede Seite lesbar und bedienbar. Jeder Block
   prüft zuerst, ob es sein Element auf dieser Seite überhaupt gibt.
   ========================================================= */
(function () {
  "use strict";

  /* ---- Seite schnell verlassen ---------------------------------------
     Knopf im Kopf, zusätzlich zweimal Escape. location.replace ersetzt
     den Verlaufseintrag — der Zurück-Knopf führt dann nicht hierher. */
  var raus = function () {
    try { location.replace("https://www.wetter.com/"); }
    catch (e) { location.href = "https://www.wetter.com/"; }
  };
  var exitKnopf = document.getElementById("exit");
  if (exitKnopf) exitKnopf.addEventListener("click", raus);
  var letzteEsc = 0;
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var jetzt = Date.now();
    if (jetzt - letzteEsc < 700) raus();
    letzteEsc = jetzt;
  });

  /* ---- Navigation aufklappen -----------------------------------------
     Den Knopf baut erst das Skript. Ohne JavaScript sieht niemand einen
     Knopf, der nichts tut — die Navigation bleibt dann eine umbrechende
     Zeile und damit benutzbar. */
  var nav = document.querySelector("nav.haupt");
  if (nav && nav.parentNode) {
    nav.setAttribute("data-klappbar", "");
    if (!nav.id) nav.id = "hauptmenue";

    var schalter = document.createElement("button");
    schalter.type = "button";
    schalter.className = "nav-schalter";
    schalter.setAttribute("aria-expanded", "false");
    schalter.setAttribute("aria-controls", nav.id);
    schalter.innerHTML = '<span class="balken" aria-hidden="true"></span><span>Menü</span>';
    nav.parentNode.insertBefore(schalter, nav);

    var umschalten = function (offen) {
      nav.classList.toggle("offen", offen);
      schalter.setAttribute("aria-expanded", offen ? "true" : "false");
    };
    schalter.addEventListener("click", function () {
      umschalten(schalter.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("offen")) {
        umschalten(false);
        schalter.focus();
      }
    });
    /* Auf einen Link tippen schließt das Menü — sonst verdeckt es das Ziel. */
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) umschalten(false);
    });
  }

  /* ---- Standdatum ----------------------------------------------------
     Jedes Element mit data-stand bekommt das Datum aus daten.js. So steht
     es nur an einer Stelle und kann nicht auf einer Seite veralten. */
  if (typeof STAND === "string") {
    Array.prototype.forEach.call(document.querySelectorAll("[data-stand]"), function (el) {
      el.textContent = "Stand: " + STAND;
    });
  }

  /* ---- Regionen-Raster ------------------------------------------------
     Zeigt Zahlen, nie Personen. Bedienbar mit Maus UND Tastatur. */
  var raster = document.getElementById("raster");
  if (raster && typeof ZONEN !== "undefined") {
    var info = document.getElementById("zoneinfo");
    var standardText = info ? info.textContent : "";

    ZONEN.forEach(function (o) {
      var b = document.createElement("button");
      b.className = "zone";
      b.type = "button";
      b.dataset.aktiv = o.m > 10 ? "2" : (o.m > 4 ? "1" : "0");

      var zahl = document.createElement("b");
      zahl.textContent = o.z;
      var wieViele = document.createElement("i");
      wieViele.textContent = o.m + " Mamis";
      b.appendChild(zahl);
      b.appendChild(wieViele);
      if (o.st) {
        var punkt = document.createElement("span");
        punkt.className = "punkt";
        b.appendChild(punkt);
      }
      b.setAttribute("aria-label",
        "Leitzone " + o.z + ", " + o.n + ", " + o.m + " Mamis, " +
        (o.st ? o.st + (o.st > 1 ? " Stammtische" : " Stammtisch") : "noch kein Stammtisch"));

      if (info) {
        var zeigen = function () {
          info.textContent = "";
          var kopf = document.createElement("strong");
          kopf.textContent = "Leitzone " + o.z + " — " + o.n;
          info.appendChild(kopf);
          info.appendChild(document.createElement("br"));
          info.appendChild(document.createTextNode(
            o.m + " Mamis sind hier unterwegs · " +
            (o.st ? o.st + (o.st > 1 ? " Stammtische" : " Stammtisch")
                  : "noch kein Stammtisch — fangen wir dort an?")));
        };
        ["mouseenter", "focus", "click"].forEach(function (e) { b.addEventListener(e, zeigen); });
        ["mouseleave", "blur"].forEach(function (e) {
          b.addEventListener(e, function () { info.textContent = standardText; });
        });
      }
      raster.appendChild(b);
    });
  }

  /* ---- Termine --------------------------------------------------------
     Ein Container mit data-termine. Die Zahl darin begrenzt, wie viele
     gezeigt werden ("3" auf der Startseite, "alle" auf der Terminseite).
     Mit data-ausfuehrlich kommt der Beschreibungstext dazu. */
  var terminBox = document.querySelector("[data-termine]");
  if (terminBox && typeof TERMINE !== "undefined") {
    var wunsch = terminBox.getAttribute("data-termine");
    var ausfuehrlich = terminBox.hasAttribute("data-ausfuehrlich");
    var liste = TERMINE.slice().sort(function (a, b) { return a.iso < b.iso ? -1 : 1; });
    if (wunsch !== "alle") liste = liste.slice(0, parseInt(wunsch, 10) || 3);

    liste.forEach(function (t) {
      var art = document.createElement("article");
      art.className = "termin";

      var datum = document.createElement("div");
      datum.className = "datum";
      var zeit = document.createElement("time");
      zeit.setAttribute("datetime", t.iso);
      var tag = document.createElement("b"); tag.textContent = t.tag;
      var monat = document.createElement("i"); monat.textContent = t.monat;
      zeit.appendChild(tag); zeit.appendChild(monat);
      datum.appendChild(zeit);

      var mitte = document.createElement("div");
      var h3 = document.createElement("h3"); h3.textContent = t.titel;
      var meta = document.createElement("p"); meta.className = "meta";

      var wo = document.createElement("span"); wo.textContent = t.wo;
      var kinder = document.createElement("span");
      kinder.className = "tag kinder";
      kinder.textContent = t.kinder ? "Kinder willkommen" : "Ohne Kinder";
      if (!t.kinder) kinder.className = "tag still";
      var platz = document.createElement("span");
      platz.className = "tag still"; platz.textContent = t.platz;
      meta.appendChild(wo); meta.appendChild(kinder); meta.appendChild(platz);

      mitte.appendChild(h3);
      mitte.appendChild(meta);
      if (ausfuehrlich && t.text) {
        var p = document.createElement("p");
        p.style.marginTop = ".6rem";
        p.style.color = "var(--pflaume-weich)";
        p.style.fontSize = "var(--step--1)";
        p.textContent = t.text;
        mitte.appendChild(p);
      }

      var knopf = document.createElement("a");
      knopf.className = "btn " + (t.art === "auszeit" ? "btn-primar" : "btn-zweit") + " btn-klein";
      knopf.href = terminBox.getAttribute("data-ziel") || "index.html#anfrage";
      knopf.textContent = t.knopf;

      art.appendChild(datum); art.appendChild(mitte); art.appendChild(knopf);
      terminBox.appendChild(art);
    });
  }

  /* ---- Einladungs-Zähler ---------------------------------------------- */
  var plaetze = document.getElementById("plaetze");
  if (plaetze && typeof EINLADUNGEN !== "undefined") {
    var e = EINLADUNGEN;
    var nichtFinanziert = e.gesamt - e.vergeben - e.offen;
    plaetze.setAttribute("aria-label",
      e.gesamt + " Einladungen: " + e.offen + " offen und verfügbar, " +
      e.vergeben + " bereits vergeben, " + nichtFinanziert + " noch nicht finanziert");
    for (var i = 0; i < e.gesamt; i++) {
      var d = document.createElement("div");
      d.className = "platz" + (i < e.vergeben ? " vergeben" : (i < e.vergeben + e.offen ? " offen" : ""));
      plaetze.appendChild(d);
    }
    Array.prototype.forEach.call(document.querySelectorAll("[data-einladungen-offen]"), function (el) {
      el.textContent = e.offen;
    });
  }

  /* ---- Einblenden beim Scrollen --------------------------------------- */
  var zuZeigen = document.querySelectorAll("[data-reveal]");
  if (!("IntersectionObserver" in window) ||
      window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    Array.prototype.forEach.call(zuZeigen, function (el) { el.classList.add("sichtbar"); });
  } else {
    var beobachter = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (eintrag) {
        if (eintrag.isIntersecting) {
          eintrag.target.classList.add("sichtbar");
          beobachter.unobserve(eintrag.target);
        }
      });
    }, { threshold: .12, rootMargin: "0px 0px -8% 0px" });
    Array.prototype.forEach.call(zuZeigen, function (el) { beobachter.observe(el); });
  }
})();
