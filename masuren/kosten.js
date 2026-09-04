/* Neues Leben Masuren — Kostenrechner für kosten.html.
 *
 * ACHTUNG, WICHTIG: Sämtliche Preise in PREISE sind BEISPIELWERTE und noch
 * keine Angebote. Jeder Wert mit "platzhalter: true" wird auf der Seite
 * sichtbar als Platzhalter markiert. Ersetze die Zahlen, sobald deine
 * echten Preise feststehen — siehe PLATZHALTER.md.
 *
 * Belegt und nicht erfunden sind nur:
 *   - PCC (Steuer auf zivilrechtliche Handlungen): 2 % des Kaufpreises
 *   - Grundbuch: 200 PLN Eigentumseintragung + 100 PLN Anlegen des Grundbuchs
 * Alles andere (Notarhonorar, Modulpreise, Grundstückspreise) ist Platzhalter.
 */
(function () {
  "use strict";

  var PREISE = {
    /* --------------------------------------------------------- Grundstücke */
    grundstuecke: [
      { id: "g-klein",  label: "Seegrundstück, ca. 1.500 m²", preis: 39000, platzhalter: true },
      { id: "g-mittel", label: "Seegrundstück, ca. 2.500 m²", preis: 59000, platzhalter: true },
      { id: "g-gross",  label: "Seegrundstück, ca. 4.000 m²", preis: 85000, platzhalter: true }
    ],

    /* ------------------------------------------------------------- Module */
    /* selbst: true  = das Modul kann man auch in Eigenleistung machen
       selbst: false = geht nur über uns bzw. über eine Fachfirma           */
    module: [
      {
        id: "m-tiny", gruppe: "Haus", label: "Tiny House, schlüsselfertig",
        info: "Kompaktes Haus ab ca. 35 m², gedämmt, ganzjährig bewohnbar.",
        preis: 62000, selbst: true, platzhalter: true
      },
      {
        id: "m-fertig", gruppe: "Haus", label: "Fertighaus, schlüsselfertig",
        info: "Größeres Fertighaus ab ca. 80 m² für Familien.",
        preis: 128000, selbst: true, platzhalter: true
      },
      {
        id: "m-brunnen", gruppe: "Autarkie", label: "Eigener Brunnen",
        info: "Bohrung, Pumpe, Filter und Hauswasserwerk — eigene Wasserversorgung.",
        preis: 7800, selbst: true, platzhalter: true
      },
      {
        id: "m-solar", gruppe: "Autarkie", label: "Solaranlage mit Speicher",
        info: "PV-Module, Wechselrichter und Batteriespeicher für netzfernen Betrieb.",
        preis: 14500, selbst: true, platzhalter: true
      },
      {
        id: "m-abwasser", gruppe: "Autarkie", label: "Kleinkläranlage",
        info: "Biologische Kläranlage statt Kanalanschluss.",
        preis: 6200, selbst: true, platzhalter: true
      },
      {
        id: "m-strom", gruppe: "Erschließung", label: "Netzanschluss Strom",
        info: "Anschluss an das öffentliche Netz, falls du nicht rein autark leben willst.",
        preis: 4500, selbst: false, platzhalter: true
      },
      {
        id: "m-zufahrt", gruppe: "Erschließung", label: "Befestigte Zufahrt & Stellplatz",
        info: "Schotterzufahrt vom Weg bis zum Haus.",
        preis: 5400, selbst: true, platzhalter: true
      }
    ],

    /* -------------------------------------------------------- Nebenkosten */
    nebenkosten: {
      pccSatz: 0.02,              /* belegt: 2 % PCC auf den Kaufpreis */
      notarSatz: 0.012,           /* PLATZHALTER — gesetzliche Staffel, vom Notar bestätigen lassen */
      grundbuchEur: 75,           /* belegt: 200 PLN + 100 PLN Gerichtsgebühren, grob umgerechnet */
      uebersetzerEur: 450         /* PLATZHALTER — vereidigter Übersetzer beim Notartermin */
    }
  };

  var euro = new Intl.NumberFormat("de-DE", {
    style: "currency", currency: "EUR", maximumFractionDigits: 0
  });

  function el(tag, klasse, text) {
    var n = document.createElement(tag);
    if (klasse) n.className = klasse;
    if (text != null) n.textContent = text;
    return n;
  }

  /* Kennzeichnet einen Preis sichtbar als Beispielwert. */
  function preisSpanne(betrag, platzhalter) {
    var s = el("span", "preis", euro.format(betrag));
    if (platzhalter) {
      s.setAttribute("data-platzhalter", "preis");
      s.title = "Beispielwert — noch kein verbindlicher Preis";
    }
    return s;
  }

  function baueGrundstuecke(ziel) {
    PREISE.grundstuecke.forEach(function (g, i) {
      var zeile = el("div", "option");
      var input = el("input");
      input.type = "radio";
      input.name = "grundstueck";
      input.id = g.id;
      input.value = g.id;
      if (i === 0) input.checked = true;

      var label = el("label");
      label.setAttribute("for", g.id);
      label.appendChild(document.createTextNode(g.label + " "));
      label.appendChild(preisSpanne(g.preis, g.platzhalter));

      zeile.appendChild(input);
      zeile.appendChild(label);
      ziel.appendChild(zeile);
    });
  }

  function baueModule(ziel) {
    var gruppen = {};
    PREISE.module.forEach(function (m) {
      (gruppen[m.gruppe] = gruppen[m.gruppe] || []).push(m);
    });

    Object.keys(gruppen).forEach(function (name) {
      var fs = el("fieldset");
      fs.appendChild(el("legend", null, name));

      gruppen[name].forEach(function (m) {
        var zeile = el("div", "option");

        var input = el("input");
        input.type = "checkbox";
        input.id = m.id;
        input.value = m.id;
        input.setAttribute("data-modul", m.id);

        var label = el("label");
        label.setAttribute("for", m.id);
        label.appendChild(document.createTextNode(m.label + " "));
        label.appendChild(preisSpanne(m.preis, m.platzhalter));
        label.appendChild(el("small", null, m.info));

        zeile.appendChild(input);
        zeile.appendChild(label);

        /* Eigenleistung: dasselbe Modul selbst machen — kostet über uns 0 €. */
        if (m.selbst) {
          var wahl = el("div", "option");
          var eigen = el("input");
          eigen.type = "checkbox";
          eigen.id = m.id + "-selbst";
          eigen.setAttribute("data-selbst", m.id);
          eigen.disabled = true;

          var eigenLabel = el("label");
          eigenLabel.setAttribute("for", m.id + "-selbst");
          eigenLabel.appendChild(document.createTextNode("… stattdessen selbst machen"));
          eigenLabel.appendChild(el("small", null,
            "Wir planen mit dir und du baust selbst — in dieser Rechnung mit 0 € angesetzt."));

          wahl.appendChild(eigen);
          wahl.appendChild(eigenLabel);
          zeile.appendChild(document.createTextNode(""));
          fs.appendChild(zeile);
          fs.appendChild(wahl);
        } else {
          fs.appendChild(zeile);
        }
      });

      ziel.appendChild(fs);
    });
  }

  /* Ein Modul ist entweder "von uns" (kostet), "selbst" (0 €) oder gar nicht. */
  function gewaehlteModule() {
    var raus = [];
    PREISE.module.forEach(function (m) {
      var vonUns = document.querySelector('[data-modul="' + m.id + '"]');
      var selbst = document.querySelector('[data-selbst="' + m.id + '"]');
      if (vonUns && vonUns.checked) {
        raus.push({ modul: m, eigen: false });
      } else if (selbst && selbst.checked) {
        raus.push({ modul: m, eigen: true });
      }
    });
    return raus;
  }

  function rechnen() {
    var gewaehltId = (document.querySelector('input[name="grundstueck"]:checked') || {}).value;
    var grundstueck = PREISE.grundstuecke.filter(function (g) { return g.id === gewaehltId; })[0]
      || PREISE.grundstuecke[0];

    var module = gewaehlteModule();
    var nk = PREISE.nebenkosten;

    var zeilen = [];
    zeilen.push({ text: grundstueck.label, betrag: grundstueck.preis, platzhalter: grundstueck.platzhalter });

    module.forEach(function (eintrag) {
      zeilen.push({
        text: eintrag.modul.label + (eintrag.eigen ? " (Eigenleistung)" : ""),
        betrag: eintrag.eigen ? 0 : eintrag.modul.preis,
        platzhalter: eintrag.eigen ? false : eintrag.modul.platzhalter
      });
    });

    /* Nebenkosten hängen am Grundstückspreis, nicht an den Modulen —
       gekauft wird das Grundstück, die Module sind Werkleistungen. */
    var pcc = Math.round(grundstueck.preis * nk.pccSatz);
    var notar = Math.round(grundstueck.preis * nk.notarSatz);

    var nebenzeilen = [
      { text: "Steuer PCC (2 % vom Kaufpreis)", betrag: pcc, platzhalter: false },
      { text: "Notarhonorar (geschätzt)", betrag: notar, platzhalter: true },
      { text: "Grundbuch / Gerichtsgebühren", betrag: nk.grundbuchEur, platzhalter: false },
      { text: "Vereidigter Übersetzer", betrag: nk.uebersetzerEur, platzhalter: true }
    ];

    var summe = zeilen.concat(nebenzeilen).reduce(function (s, z) { return s + z.betrag; }, 0);
    return { zeilen: zeilen, nebenzeilen: nebenzeilen, summe: summe };
  }

  function zeileMalen(z) {
    var tr = el("tr");
    tr.appendChild(el("th", null, z.text));
    var td = el("td", "zahl");
    if (z.platzhalter) {
      var s = el("span", null, euro.format(z.betrag));
      s.setAttribute("data-platzhalter", "preis");
      td.appendChild(s);
    } else {
      td.textContent = euro.format(z.betrag);
    }
    tr.appendChild(td);
    return tr;
  }

  function malen() {
    var body = document.getElementById("ergebnis-zeilen");
    var summeFeld = document.getElementById("ergebnis-summe");
    if (!body || !summeFeld) return;

    var r = rechnen();
    body.textContent = "";

    r.zeilen.forEach(function (z) { body.appendChild(zeileMalen(z)); });

    var trenner = el("tr");
    var th = el("th", null, "Kaufnebenkosten");
    th.colSpan = 2;
    th.style.paddingTop = "18px";
    trenner.appendChild(th);
    body.appendChild(trenner);

    r.nebenzeilen.forEach(function (z) { body.appendChild(zeileMalen(z)); });

    summeFeld.textContent = euro.format(r.summe);
  }

  /* Eigenleistungs-Kästchen nur aktivieren, wenn das Modul nicht bei uns
     gebucht ist — und umgekehrt. */
  function verriegeln(e) {
    var ziel = e.target;
    var modulId = ziel.getAttribute("data-modul");
    var selbstId = ziel.getAttribute("data-selbst");

    if (modulId) {
      var selbstFeld = document.querySelector('[data-selbst="' + modulId + '"]');
      if (selbstFeld) {
        selbstFeld.disabled = ziel.checked;
        if (ziel.checked) selbstFeld.checked = false;
      }
    }
    if (selbstId) {
      var modulFeld = document.querySelector('[data-modul="' + selbstId + '"]');
      if (modulFeld && ziel.checked) modulFeld.checked = false;
    }
  }

  function start() {
    var gField = document.getElementById("feld-grundstueck");
    var mZiel = document.getElementById("feld-module");
    var form = document.getElementById("konfigurator");
    if (!gField || !mZiel || !form) return;

    baueGrundstuecke(gField);
    baueModule(mZiel);

    /* Eigenleistung ist erst wählbar, wenn das Modul nicht gebucht ist. */
    Array.prototype.forEach.call(form.querySelectorAll("[data-selbst]"), function (f) {
      f.disabled = false;
    });

    form.addEventListener("change", function (e) {
      verriegeln(e);
      malen();
    });
    malen();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
