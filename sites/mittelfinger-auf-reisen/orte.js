/* Mittelfinger auf Reisen — alle Orte an einer Stelle.
 *
 * Diese Datei ist die einzige Stelle, an der Orte gepflegt werden.
 * Karte („karte.html"), die Ortsliste darunter und die Teaser auf der
 * Startseite lesen alle hier heraus.
 *
 * Neuen Ort ergänzen: Block kopieren, Werte ersetzen, fertig.
 *
 *   name         Ortsname, so wie du ihn nennst
 *   land         Land
 *   lat / lng    Koordinaten (Dezimalgrad). Aus einer Karten-App kopierbar.
 *   datum        ISO-Datum, "2026-06-14" — wird automatisch deutsch formatiert
 *   foto         Pfad zum Bild in bilder/, z. B. "bilder/lofoten.jpg".
 *                Leer lassen ("") -> es erscheint ein sichtbarer Platzhalter.
 *   alt          Bildbeschreibung für Screenreader (Pflicht, sobald foto gesetzt)
 *   kurz         zwei, drei Sätze — die Geschichte in Kurzform
 *   scheissdrauf der Scheiß-drauf-Moment an diesem Ort
 *   camper       ehrlicher Camper-Tipp
 *   link         Datei des vollständigen Reiseberichts, sonst ""
 *   geplant      true = noch nicht gefahren, erscheint als nächster Stopp
 *
 * ACHTUNG: Die Texte unten sind Beispieltexte aus dem Konzept, damit die
 * Seite von Anfang an nicht leer aussieht. Ersetze sie durch deine eigenen.
 */
window.ORTE = [
  {
    name: "Reine, Lofoten",
    land: "Norwegen",
    lat: 67.9333,
    lng: 13.0833,
    datum: "2026-06-14",
    foto: "",
    alt: "",
    kurz: "Sechs Grad, nasse Schuhe und Wind aus allen Richtungen. Trotzdem besser als ein perfekter Tag am falschen Ort.",
    scheissdrauf: "Die Fähre war weg, der Plan auch. Also blieb ich einfach.",
    camper: "Der schöne Stellplatz am Wasser ist eine Windschneise. Zwei Reihen weiter hinten schläfst du.",
    link: "beitrag-lofoten.html",
    geplant: false
  },
  {
    name: "Cabo da Roca",
    land: "Portugal",
    lat: 38.7803,
    lng: -9.4989,
    datum: "2026-03-02",
    foto: "",
    alt: "",
    kurz: "Westlichster Punkt des Festlands, dreißig Reisebusse und ich mittendrin mit ausgestrecktem Finger. Der Atlantik hat nicht gelacht.",
    scheissdrauf: "Ich hatte mir vorgenommen, Touristenorte zu meiden. Und stand dann doch da. War großartig.",
    camper: "Übernachten ist dort verboten und wird kontrolliert. Zehn Kilometer weiter im Landesinneren stehst du legal und ruhig.",
    link: "beitrag-cabo-da-roca.html",
    geplant: false
  },
  {
    name: "Transfăgărășan",
    land: "Rumänien",
    lat: 45.6019,
    lng: 24.6172,
    datum: "2025-09-08",
    foto: "",
    alt: "",
    kurz: "Serpentinen, Nebel und ein Camper, der bei jeder Kurve etwas anderes zu sagen hatte. Oben angekommen: nichts gesehen. Trotzdem alles gehabt.",
    scheissdrauf: "Alle sagten, das Ding sei zu eng für meinen Kasten. War es auch. Bin trotzdem hoch.",
    camper: "Vor der Passhöhe tanken. Danach kommt sehr lange gar nichts.",
    link: "beitrag-transfagarasan.html",
    geplant: false
  },
  {
    name: "Vík í Mýrdal",
    land: "Island",
    lat: 63.4187,
    lng: -19.0060,
    datum: "2025-07-21",
    foto: "",
    alt: "",
    kurz: "Schwarzer Sand, waagerechter Regen, ein Finger, der kaum stillhalten wollte.",
    scheissdrauf: "Regenjacke im Van gelassen. Bewusst. Kurz danach bereut, lange danach nicht mehr.",
    camper: "Wasser gibt es am Campingplatz im Ort. Wildcampen ist hier verboten, und das aus gutem Grund.",
    link: "",
    geplant: false
  },
  {
    name: "Passo dello Stelvio",
    land: "Italien",
    lat: 46.5285,
    lng: 10.4536,
    datum: "2025-06-02",
    foto: "",
    alt: "",
    kurz: "Achtundvierzig Kehren, eine Kupplung mit eigener Meinung und oben ein Bratwurststand. Perfekt.",
    scheissdrauf: "Hinter mir eine Schlange Motorräder. Ich bin trotzdem im zweiten Gang geblieben.",
    camper: "Oben ist Übernachten heikel. Runter Richtung Bormio gibt es Platz und weniger Wind.",
    link: "",
    geplant: false
  },
  {
    name: "Großglockner Hochalpenstraße",
    land: "Österreich",
    lat: 47.0742,
    lng: 12.8339,
    datum: "2025-05-18",
    foto: "",
    alt: "",
    kurz: "Maut bezahlt, Aussicht bekommen, Finger gehoben. Ein fairer Handel.",
    scheissdrauf: "Ich wollte an dem Tag eigentlich nur Wäsche waschen.",
    camper: "Die Straße ist nachts gesperrt. Wer oben schlafen will, ist zu spät dran.",
    link: "",
    geplant: false
  },
  {
    name: "Tarifa",
    land: "Spanien",
    lat: 36.0128,
    lng: -5.6065,
    datum: "2025-02-11",
    foto: "",
    alt: "",
    kurz: "Wind, Kitesurfer und Afrika am Horizont. Der südlichste Finger bisher.",
    scheissdrauf: "Drei Tage nichts getan. Null schlechtes Gewissen.",
    camper: "Auf dem Parkplatz an der Playa de los Lances wird geräumt. Die Campingplätze westlich davon sind entspannt.",
    link: "",
    geplant: false
  },
  {
    name: "Nordkapp",
    land: "Norwegen",
    lat: 71.1710,
    lng: 25.7846,
    datum: "",
    foto: "",
    alt: "",
    kurz: "Der nächste Stopp. Weit oben, teuer, angeblich überlaufen — genau deshalb.",
    scheissdrauf: "",
    camper: "",
    link: "",
    geplant: true
  }
];
