/* Mittelfinger auf Reisen — alle Inhalte an einer Stelle.
 *
 * Zwei Listen: Orte für die Karte, Beiträge für den Reise-Blog.
 * Karte, Ortsliste und Blogübersicht lesen ausschließlich hier heraus.
 */

/* ------------------------------- Orte ------------------------------------
 * Neuen Ort ergänzen: Block kopieren, Werte ersetzen.
 *
 *   name    Ortsname
 *   land    Land
 *   lat/lng Koordinaten in Dezimalgrad (aus jeder Karten-App kopierbar)
 *   datum   ISO-Datum "2026-09-10" — wird automatisch deutsch formatiert
 *   start   true nur beim allerersten Ort
 *   kurz    ein, zwei Sätze
 * ------------------------------------------------------------------------ */
window.ORTE = [
  {
    name: "Wiesbaden",
    land: "Deutschland",
    lat: 50.0826,
    lng: 8.2400,
    datum: "2026-09-10",
    start: true,
    kurz: "Wo alles losgeht. Noch steht der Camper in der Einfahrt, der Finger ist schon montiert."
  }
];

/* ----------------------------- Blogbeiträge ------------------------------
 * Neuen Beitrag ergänzen: Block kopieren, HTML-Datei nach dem Muster von
 * blog-start-wiesbaden.html anlegen und hier eintragen.
 *
 *   titel   Überschrift
 *   ort     Ortsname, passend zu einem Eintrag oben
 *   datum   ISO-Datum
 *   teaser  zwei, drei Zeilen für die Übersicht
 *   datei   Dateiname der Beitragsseite
 * ------------------------------------------------------------------------ */
window.BEITRAEGE = [
  {
    titel: "Kilometerstand null",
    ort: "Wiesbaden",
    datum: "2026-09-10",
    teaser: "Der Camper steht noch in der Einfahrt, die Route ist ein leeres Blatt und der Finger klebt schon am Armaturenbrett. Wie das hier anfängt.",
    datei: "blog-start-wiesbaden.html"
  }
];
