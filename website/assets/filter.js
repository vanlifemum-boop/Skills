/* =========================================================================
   Kleine Füße, große Welt — Reise-Archiv mit Filter-System
   ---------------------------------------------------------------------------
   Kernfeature: Reisen werden nach drei Dimensionen gefiltert
   (Jahreszeit, Fahrzeug, Region) — UND-Verknüpfung, ohne Seiten-Neuladen.

   ERWEITERBARKEIT: Eine vierte Dimension (z. B. "Thema") lässt sich hinzufügen,
   indem man EINEN Eintrag in FILTER_DIMENSIONS ergänzt und den Reisen das
   passende Feld gibt. Der restliche Code passt sich automatisch an.
   ========================================================================= */
(function () {
  "use strict";

  /* ---------- 1) Filter-Dimensionen (Konfiguration, nicht hartcodiert) ----------
     Jede Dimension hat:
       key    – Feldname im Reise-Datensatz
       label  – Überschrift der Filtergruppe
       tagCls – CSS-Klasse für die farbliche Chip-Kennzeichnung
       values – auswählbare Werte
     Neue Dimension = einfach hier ein Objekt anhängen (+ Feld in DATA setzen).
  */
  var FILTER_DIMENSIONS = [
    { key: "jahreszeit", label: "Jahreszeit", tagCls: "tag--jahreszeit",
      values: ["Herbst", "Winter", "Frühling", "Sommer"] },
    { key: "fahrzeug",   label: "Fahrzeug",   tagCls: "tag--fahrzeug",
      values: ["Zug", "Camper", "Flugzeug", "Auto"] },
    { key: "region",     label: "Region",     tagCls: "tag--region",
      values: ["Deutschland", "Europa", "Fernreise"] }
    // Beispiel für eine 4. Dimension – bei Bedarf einkommentieren:
    // ,{ key: "thema", label: "Thema", tagCls: "tag--thema",
    //    values: ["Natur", "Stadt", "Meer", "Berge"] }
  ];

  /* ---------- 2) Demo-Reisen ----------
     Jede Reise trägt für jede Dimension genau einen Wert (Demo-Datensatz).
     Illustration = Beschriftung des Comic-Platzhalters.
  */
  var DATA = [
    {
      titel: "Herbstzauber in der Toskana",
      kurz: "Mit dem Camper durch goldene Weinberge — Thadeo zählt Zypressen und Traktoren.",
      illu: "Comic: Thadeo winkt aus dem Camper vor Toskana-Hügeln",
      jahreszeit: "Herbst", fahrzeug: "Camper", region: "Europa"
    },
    {
      titel: "Weihnachtsmarkt Nürnberg",
      kurz: "Mit dem Zug zu Lebkuchenduft und Lichterglanz — die erste Traumreise im Schnee.",
      illu: "Comic: Mama & Thadeo am Glühwein-Stand mit Lichtern",
      jahreszeit: "Winter", fahrzeug: "Zug", region: "Deutschland"
    },
    {
      titel: "Frühling an der Nordsee",
      kurz: "Mit dem Auto zu Wattwürmern, Wind und den ersten nackten Kinderfüßen im Sand.",
      illu: "Comic: Thadeo mit Eimer und Schaufel im Watt",
      jahreszeit: "Frühling", fahrzeug: "Auto", region: "Deutschland"
    },
    {
      titel: "Sommerinsel Kreta",
      kurz: "Mit dem Flugzeug ans türkise Meer — Thadeos erster Flug und ganz viele Ziegen.",
      illu: "Comic: Flugzeugfenster, darunter blaues Meer und Insel",
      jahreszeit: "Sommer", fahrzeug: "Flugzeug", region: "Europa"
    },
    {
      titel: "Winterwald im Allgäu",
      kurz: "Mit dem Auto zur verschneiten Berghütte — Schlittenfahren und heiße Milch.",
      illu: "Comic: Thadeo auf dem Schlitten, Mama zieht bergauf",
      jahreszeit: "Winter", fahrzeug: "Auto", region: "Deutschland"
    },
    {
      titel: "Sommer-Fernreise nach Bali",
      kurz: "Eine große Traumreise mit dem Flugzeug — Reisfelder, Affen und warmer Regen.",
      illu: "Comic: Thadeo zwischen grünen Reisterrassen, Palmen",
      jahreszeit: "Sommer", fahrzeug: "Flugzeug", region: "Fernreise"
    },
    {
      titel: "Frühlingsfahrt nach Amsterdam",
      kurz: "Mit dem Zug zu Grachten und Tulpen — Thadeo entdeckt Boote und Fahrräder.",
      illu: "Comic: Grachtenhäuser, Tulpen, Thadeo im Tragetuch",
      jahreszeit: "Frühling", fahrzeug: "Zug", region: "Europa"
    },
    {
      titel: "Herbstcamping im Schwarzwald",
      kurz: "Mit dem Camper durch bunte Wälder — Kastanien sammeln und Lagerfeuer-Geschichten.",
      illu: "Comic: Camper am Waldrand, Thadeo mit Kastanien",
      jahreszeit: "Herbst", fahrzeug: "Camper", region: "Deutschland",
      href: "ratgeber-herbstcamping.html"
    },
    {
      titel: "Der schiefe Turm von Pisa",
      kurz: "Mit dem Auto in die Toskana: Thadeo & Bobo besuchen den schiefen Turm und die Piazza dei Miracoli.",
      illu: "Comic: Thadeo hält scheinbar den schiefen Turm von Pisa",
      jahreszeit: "Sommer", fahrzeug: "Auto", region: "Europa",
      href: "buch-pisa.html"
    }
  ];

  /* ---------- 3) Zustand: aktive Auswahl je Dimension ---------- */
  var activeFilters = {};
  FILTER_DIMENSIONS.forEach(function (dim) { activeFilters[dim.key] = null; });

  /* ---------- 4) Elemente ---------- */
  var barEl   = document.getElementById("filterbar");
  var gridEl  = document.getElementById("reise-grid");
  var countEl = document.getElementById("filter-count");
  if (!barEl || !gridEl) return; // nur auf der Archiv-Seite aktiv

  /* ---------- 5) Filterleiste aufbauen ---------- */
  function buildFilterbar() {
    FILTER_DIMENSIONS.forEach(function (dim) {
      var group = document.createElement("div");
      group.className = "filter-group";

      var label = document.createElement("span");
      label.className = "filter-group__label";
      label.textContent = dim.label;
      group.appendChild(label);

      var row = document.createElement("div");
      row.className = "chip-row";

      dim.values.forEach(function (val) {
        var chip = document.createElement("button");
        chip.type = "button";
        chip.className = "chip";
        chip.textContent = val;
        chip.setAttribute("aria-pressed", "false");
        chip.addEventListener("click", function () {
          // Toggle: nochmaliges Klicken hebt die Auswahl auf
          activeFilters[dim.key] = (activeFilters[dim.key] === val) ? null : val;
          syncChips(row, dim.key);
          render();
        });
        row.appendChild(chip);
      });

      group.appendChild(row);
      barEl.appendChild(group);
    });

    // "Alle zurücksetzen"
    var meta = document.createElement("div");
    meta.className = "filter-meta";
    var reset = document.createElement("button");
    reset.type = "button";
    reset.className = "btn btn--ghost";
    reset.textContent = "Alle Filter zurücksetzen";
    reset.addEventListener("click", resetAll);
    meta.appendChild(reset);
    barEl.appendChild(meta);
  }

  function syncChips(row, key) {
    Array.prototype.forEach.call(row.children, function (chip) {
      chip.setAttribute("aria-pressed",
        String(activeFilters[key] === chip.textContent));
    });
  }

  function resetAll() {
    FILTER_DIMENSIONS.forEach(function (dim) { activeFilters[dim.key] = null; });
    barEl.querySelectorAll(".chip").forEach(function (chip) {
      chip.setAttribute("aria-pressed", "false");
    });
    render();
  }

  /* ---------- 6) Filtern (UND-Verknüpfung über alle Dimensionen) ---------- */
  function matches(reise) {
    return FILTER_DIMENSIONS.every(function (dim) {
      var sel = activeFilters[dim.key];
      return sel === null || reise[dim.key] === sel;
    });
  }

  /* ---------- 7) Rendern der Karten ---------- */
  function render() {
    var visible = DATA.filter(matches);
    gridEl.innerHTML = "";

    if (!visible.length) {
      var empty = document.createElement("div");
      empty.className = "filter-empty";
      empty.textContent = "Für diese Kombination gibt es noch keine Reise — probier eine andere aus! 🧭";
      gridEl.appendChild(empty);
    } else {
      visible.forEach(function (reise) {
        gridEl.appendChild(buildCard(reise));
      });
    }

    if (countEl) {
      countEl.textContent = visible.length === 1
        ? "1 Reise gefunden"
        : visible.length + " Reisen gefunden";
    }
  }

  function buildCard(reise) {
    var card = document.createElement("article");
    card.className = "card";

    var ph = document.createElement("div");
    ph.className = "ph";
    ph.setAttribute("role", "img");
    ph.setAttribute("aria-label", reise.illu);
    var phSpan = document.createElement("span");
    phSpan.textContent = "[" + reise.illu + "]";
    ph.appendChild(phSpan);
    card.appendChild(ph);

    var body = document.createElement("div");
    body.className = "card__body";

    var h3 = document.createElement("h3");
    h3.className = "card__title";
    h3.textContent = reise.titel;
    body.appendChild(h3);

    var p = document.createElement("p");
    p.className = "card__text";
    p.textContent = reise.kurz;
    body.appendChild(p);

    // Tags farblich je Dimension
    var tags = document.createElement("div");
    tags.className = "tags";
    FILTER_DIMENSIONS.forEach(function (dim) {
      var t = document.createElement("span");
      t.className = "tag " + dim.tagCls;
      t.textContent = reise[dim.key];
      tags.appendChild(t);
    });
    body.appendChild(tags);

    var foot = document.createElement("div");
    foot.className = "card__foot";
    var link = document.createElement("a");
    link.className = "btn btn--primary";
    link.href = reise.href || "reise-beispiel.html"; // eigener Link, sonst Musterreise
    link.textContent = "Reise lesen";
    foot.appendChild(link);
    body.appendChild(foot);

    card.appendChild(body);
    return card;
  }

  /* ---------- 8) Start ---------- */
  buildFilterbar();
  render();
})();
