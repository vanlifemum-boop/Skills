/* =========================================================
   MAL WIEDER NORMAL SEIN — Die Zahlen der Seite
   =========================================================
   Das hier ist die einzige Datei, die regelmäßig angefasst wird.
   Einmal im Monat: Zahlen prüfen, STAND ändern, fertig. Sonst nichts.

   Feste Regeln aus dem Konzept — bitte einhalten:
   · Hier steht niemals eine Person, ein Name, eine Adresse.
     Sichtbar sind nur Zahlen, Regionen und Termine.
   · Jede Zahl braucht ein Datum. Veraltete Zahlen sind schlimmer
     als gar keine — deshalb STAND immer mitändern.
   · Jeder Termin trägt "kinder": true oder false. Kein Termin
     ohne diese Angabe.
   · Der genaue Ort steht NIE hier. Er steht in der Bestätigungsmail.
   ========================================================= */

/* Stand der Zahlen — erscheint sichtbar über dem Regionen-Raster. */
var STAND = "23.08.2026";

/* Die zehn Postleitzonen.
   z  = erste Ziffer der Postleitzahl
   n  = wie die Gegend hier genannt wird
   m  = wie viele Mamis dort unterwegs sind
   st = wie viele Stammtische es dort gibt (0 = noch keiner) */
var ZONEN = [
  { z: "0", n: "Sachsen, Ostthüringen",              m:  6, st: 1 },
  { z: "1", n: "Berlin, Brandenburg",                m: 11, st: 1 },
  { z: "2", n: "Hamburg, Schleswig-Holstein",        m:  4, st: 0 },
  { z: "3", n: "Niedersachsen, Nordhessen",          m:  7, st: 1 },
  { z: "4", n: "Nordrhein-Westfalen",                m: 14, st: 2 },
  { z: "5", n: "Köln, Bonn, Rheinland-Pfalz Nord",   m:  5, st: 0 },
  { z: "6", n: "Hessen, Rheinhessen, Saarland",      m:  3, st: 0 },
  { z: "7", n: "Baden-Württemberg",                  m:  8, st: 1 },
  { z: "8", n: "Südbayern, Schwaben",                m:  5, st: 0 },
  { z: "9", n: "Nordbayern, Oberpfalz, Franken",     m: 13, st: 2 }
];

/* Die Termine.
   tag/monat  = wie es auf dem Kalenderblatt steht
   iso        = Sortierung und <time datetime="…">
   titel      = kurz, ohne Ortsangabe
   wo         = Region, mehr nicht
   kinder     = true / false — Pflichtangabe, siehe oben
   platz      = freie Plätze oder Hinweis, als Text
   art        = "stammtisch" | "ausflug" | "auszeit"
   knopf      = Beschriftung des Anmeldeknopfs
   text       = ein bis zwei Sätze für die ausführliche Terminliste */
var TERMINE = [
  {
    iso: "2026-09-12", tag: "12", monat: "Sep",
    titel: "Eltern-Stammtisch, Frühstück",
    wo: "Region 9 · Oberpfalz", kinder: true,
    platz: "4 von 10 Plätzen frei", art: "stammtisch",
    knopf: "Anmelden",
    text: "Ein langer Vormittag am großen Tisch. Du kannst um zehn kommen und um halb zwölf wieder gehen, du kannst auch bleiben. Niemand fragt dich, warum du da bist."
  },
  {
    iso: "2026-10-04", tag: "04", monat: "Okt",
    titel: "Bowling und Pizza",
    wo: "Region 9 · Franken", kinder: true,
    platz: "3 Einladungen frei", art: "ausflug",
    knopf: "Anmelden",
    text: "Zwei Bahnen, danach Pizza. Laut, unkompliziert, gut für alle, denen ein Café zu viel Gespräch ist. Die Kinder spielen mit."
  },
  {
    iso: "2026-12-28", tag: "28", monat: "Dez",
    titel: "Silvester gemeinsam — fünf Tage nahe der polnischen Grenze",
    wo: "Anreise in Fahrgemeinschaften", kinder: true,
    platz: "Interesse sammeln", art: "auszeit",
    knopf: "Interesse anmelden",
    text: "Fünf Tage über den Jahreswechsel. Unterkunft und Anreise buchst du selbst — wir organisieren die Gruppe und das Programm drumherum. Wie das genau läuft, steht auf der Seite zur Auszeit."
  }
];

/* Der Einladungs-Zähler.
   gesamt    = wie viele Einladungen für die nächsten Termine gedacht sind
   vergeben  = schon an jemanden gegangen
   offen     = finanziert und noch frei
   Der Rest (gesamt − vergeben − offen) gilt als noch nicht finanziert. */
var EINLADUNGEN = { gesamt: 24, vergeben: 8, offen: 11 };
