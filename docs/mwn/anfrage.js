/* =========================================================
   MAL WIEDER NORMAL SEIN — Der Anfrage-Baukasten
   =========================================================
   Kein Formular, das irgendwohin abgeschickt wird. Die Seite baut im
   Browser einen fertigen Mailtext zusammen. Die Frau sieht ihn Wort für
   Wort, kann alles ändern und entscheidet selbst, ob sie ihn abschickt
   oder kopiert. Es verlässt nichts den Rechner, bevor sie sendet.

   Deshalb gibt es hier auch kein fetch(), kein XHR und keinen Server.
   Wer das je ändert, muss die Datenschutzerklärung mitändern.
   ========================================================= */
(function () {
  "use strict";

  var f = document.getElementById("baukasten");
  if (!f) return;

  /* ⚠ PLATZHALTER — vor dem Livegang ersetzen. Siehe PLATZHALTER.md. */
  var MAIL = "hallo@beispiel-domain-bitte-ersetzen.de";

  var KAT = {
    suche: ["Begleitung zum Jugendamt", "Begleitung zu einer anderen Behörde",
            "Begleitung zum Gericht", "Begleitung zu Arzt oder Klinik",
            "Jemanden zum Reden", "Austausch mit anderen Müttern",
            "Hilfe beim Sortieren von Unterlagen", "Kinderbetreuung während eines Termins",
            "Mitfahrgelegenheit", "Stammtisch in meiner Nähe",
            "Einladung zu einem Termin", "Ich fühle mich allein", "Etwas anderes"],
    biete: ["Begleitung zu Behörden", "Begleitung zum Gericht",
            "Zuhören und telefonieren", "Unterlagen sortieren", "Kinderbetreuung",
            "Fahrgemeinschaft", "Übernachtung", "Sachen und Kleidung",
            "Kochen und backen", "Stammtisch bei mir gründen",
            "Ich lade jemanden mit ein", "Etwas anderes"]
  };

  /* Unterseiten dürfen mit ?thema=… hierher verlinken und damit eine
     Auswahl vorbelegen — z. B. "Starterkit anfragen" auf der
     Stammtischseite. Mehr macht der Parameter nicht. */
  var THEMEN = {
    stammtisch:   { rolle: "suche", kat: "Stammtisch in meiner Nähe" },
    gruenden:     { rolle: "biete", kat: "Stammtisch bei mir gründen" },
    begleitung:   { rolle: "suche", kat: "Begleitung zum Jugendamt" },
    einladung:    { rolle: "suche", kat: "Einladung zu einem Termin" },
    mitgehen:     { rolle: "biete", kat: "Begleitung zu Behörden" },
    miteinladen:  { rolle: "biete", kat: "Ich lade jemanden mit ein" },
    auszeit:      { rolle: "suche", kat: "Etwas anderes" }
  };

  var katBox   = document.getElementById("kategorien"),
      katLabel = document.getElementById("katLabel"),
      zone     = document.getElementById("zone"),
      ausgabe  = document.getElementById("text"),
      kinderJa = document.getElementById("kinderJa"),
      frei     = document.getElementById("frei"),
      nameFeld = document.getElementById("name");

  if (typeof ZONEN !== "undefined" && zone) {
    ZONEN.forEach(function (o) {
      var opt = document.createElement("option");
      opt.value = o.z;
      opt.textContent = "Region " + o.z + " — " + o.n;
      zone.appendChild(opt);
    });
  }

  function rolle() {
    var gewaehlt = f.querySelector('input[name="rolle"]:checked');
    return gewaehlt ? gewaehlt.value : "suche";
  }

  function katZeichnen(vorauswahl) {
    katBox.textContent = "";
    katLabel.textContent = rolle() === "suche"
      ? "Worum geht es? (mehrere möglich)"
      : "Was kannst du anbieten? (mehrere möglich)";
    KAT[rolle()].forEach(function (k) {
      var l = document.createElement("label");
      var i = document.createElement("input");
      i.type = "checkbox";
      i.value = k;
      if (vorauswahl && vorauswahl === k) i.checked = true;
      var s = document.createElement("span");
      s.textContent = k;
      l.appendChild(i);
      l.appendChild(s);
      katBox.appendChild(l);
    });
    bauen();
  }

  function bauen() {
    var r = rolle(),
        gewaehlt = Array.prototype.slice.call(katBox.querySelectorAll("input:checked"))
                     .map(function (i) { return i.value; }),
        z = zone ? zone.value : "",
        kinder = kinderJa ? kinderJa.checked : false,
        freitext = frei ? frei.value.trim() : "",
        name = nameFeld ? nameFeld.value.trim() : "";

    var t = r === "suche"
      ? "Hallo,\n\nich brauche gerade jemanden.\n"
      : "Hallo,\n\nich möchte für andere da sein.\n";
    if (gewaehlt.length) {
      t += "\nDarum geht es:\n" + gewaehlt.map(function (k) { return "- " + k; }).join("\n") + "\n";
    }
    if (z) t += "\nIch bin in Region " + z + ".\n";
    if (kinder) t += r === "suche" ? "Meine Kinder sind dabei.\n" : "Kinder dürfen bei mir mitkommen.\n";
    if (freitext) t += "\n" + freitext + "\n";
    t += "\nViele Grüße\n" + (name || "(ohne Namen)");

    ausgabe.textContent = t;
    return t;
  }

  f.addEventListener("change", function (e) {
    if (e.target.name === "rolle") katZeichnen(); else bauen();
  });
  f.addEventListener("input", bauen);
  /* Absenden per Enter würde die Seite neu laden und alles verwerfen. */
  f.addEventListener("submit", function (e) { e.preventDefault(); });

  var senden = document.getElementById("senden");
  if (senden) senden.addEventListener("click", function () {
    var betreff = rolle() === "suche" ? "Ich brauche jemanden" : "Ich möchte da sein";
    location.href = "mailto:" + MAIL +
      "?subject=" + encodeURIComponent(betreff) +
      "&body=" + encodeURIComponent(bauen());
  });

  var kopieren = document.getElementById("kopieren");
  if (kopieren) kopieren.addEventListener("click", function () {
    var b = this, t = bauen();
    var fertig = function () {
      b.textContent = "Kopiert";
      setTimeout(function () { b.textContent = "Text kopieren"; }, 1800);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(t).then(fertig, fertig);
    } else {
      var ta = document.createElement("textarea");
      ta.value = t;
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta);
      fertig();
    }
  });

  /* Vorauswahl aus ?thema=… */
  var thema = null;
  try {
    thema = new URLSearchParams(location.search).get("thema");
  } catch (e) {}
  if (thema && Object.prototype.hasOwnProperty.call(THEMEN, thema)) {
    var wahl = THEMEN[thema];
    var knopf = f.querySelector('input[name="rolle"][value="' + wahl.rolle + '"]');
    if (knopf) knopf.checked = true;
    katZeichnen(wahl.kat);
  } else {
    katZeichnen();
  }
})();
