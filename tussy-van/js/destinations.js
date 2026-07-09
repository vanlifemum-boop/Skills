/* Reiseziele — hier eigene Ziele eintragen/ändern.
   country: Filter-Schlüssel | color: bg-blue, bg-deep, bg-army, bg-terra, bg-camel
   Die id muss zur id in js/route-points.json passen (dann sitzt der Kartenpunkt richtig). */
window.TV_DESTINATIONS = [
  {
    id: "kolberg", country: "polen", flag: "🇵🇱", name: "Kołobrzeg & Ostseeküste", region: "Ostsee-Liebe",
    color: "bg-blue",
    blurb: "Weiße Strände, Kiefernwälder und der beste Sonnenuntergang direkt vor der Schiebetür — ein Ostsee-Klassiker, den ich immer wieder anfahre.",
    stellplatz: "Camping 78 Baltic direkt hinter der Düne, ruhig & bulli-freundlich.",
    zeit: "Mai–September, im Herbst herrlich leer.",
    tipp: "Abends an der Mole Fischbrötchen holen und aufs Wasser schauen."
  },
  {
    id: "ruegen", country: "deutschland", flag: "🇩🇪", name: "Rügen", region: "Kreidefelsen & Buchenwald",
    color: "bg-deep",
    blurb: "Der Klassiker, der nie langweilig wird: Kreideküste, Alleen und kleine Fischerdörfer.",
    stellplatz: "Stellplatz am Hafen Lauterbach — morgens Brötchen vom Kutter.",
    zeit: "Juni oder September, Hauptsaison meiden.",
    tipp: "Sonnenaufgang am Königsstuhl — um 5 Uhr gehört er dir allein."
  },
  {
    id: "eckernfoerde", country: "deutschland", flag: "🇩🇪", name: "Eckernförde", region: "Ostsee-Bilderbuch",
    color: "bg-army",
    blurb: "Bunte Giebelhäuser, ein feiner Sandstrand mitten in der Stadt und Räucherfisch an jeder Ecke.",
    stellplatz: "Wohnmobilstellplatz Süderberg / am Hafen — zu Fuß in die Altstadt.",
    zeit: "Mai–September.",
    tipp: "Original Eckernförder Sprotten frisch aus der Räucherei probieren."
  },
  {
    id: "sylt", country: "deutschland", flag: "🇩🇪", name: "Sylt", region: "Nordsee-Insel",
    color: "bg-blue",
    blurb: "Endlose Weststrände, Wanderdünen und der raue Charme der Nordsee — mit dem Autozug rollt der Bulli mit.",
    stellplatz: "Campingplatz Westerland / Rantum, früh reservieren (Insel = knapp).",
    zeit: "Juni–September; im Winter stürmisch-schön & leer.",
    tipp: "Ellenbogen im Norden: Schafe, Leuchttürme, Ende der Welt-Gefühl."
  },
  {
    id: "legoland", country: "daenemark", flag: "🇩🇰", name: "Legoland Billund", region: "Familien-Highlight",
    color: "bg-terra",
    blurb: "Das Original in Dänemark — Millionen Steine, Fahrgeschäfte und leuchtende Kinderaugen. Perfekt für einen Familienstopp.",
    stellplatz: "Campingplätze direkt am Park (Legoland Holiday / Billund) — praktisch fußläufig.",
    zeit: "April–Oktober (Park-Saison).",
    tipp: "Nachmittagsticket kaufen und den nächsten Vormittag gleich mitnehmen — oft günstiger."
  },
  {
    id: "hamburg", country: "deutschland", flag: "🇩🇪", name: "Hamburg", region: "Hafen & Großstadt",
    color: "bg-deep",
    blurb: "Speicherstadt, Hafen, Fischmarkt und Kiez — Großstadt-Kick zwischen zwei Küsten-Etappen.",
    stellplatz: "Wohnmobilstellplatz an der Alster / Wohnmobilpark Kaltenkirchen; mit HVV-Ticket in die City.",
    zeit: "Ganzjährig — Regenjacke einpacken.",
    tipp: "Sonntags früh zum Fischmarkt: Party-Ende trifft Frühaufsteher."
  },
  {
    id: "carolinensiel", country: "deutschland", flag: "🇩🇪", name: "Carolinensiel", region: "Ostfriesland",
    color: "bg-camel",
    blurb: "Museumshafen, Wattenmeer und ostfriesische Ruhe — hier tickt die Uhr nach Ebbe und Flut.",
    stellplatz: "Reisemobilhafen Harlesiel direkt am Deich, mit Fähre nach Wangerooge.",
    zeit: "Mai–September.",
    tipp: "Geführte Wattwanderung mitmachen — barfuß und mit Guide, nie allein."
  },
  {
    id: "norddeich", country: "deutschland", flag: "🇩🇪", name: "Norden / Norddeich", region: "Nordsee-Deich",
    color: "bg-army",
    blurb: "Deichspaziergänge, Seehundstation und Fähranleger nach Juist & Norderney — Nordsee zum Anfassen.",
    stellplatz: "Wohnmobilstellplatz Norddeich direkt hinterm Deich, Meerblick inklusive.",
    zeit: "April–Oktober.",
    tipp: "Tee ostfriesisch: erst Kluntje, dann Sahne — nicht umrühren!"
  },
  {
    id: "amsterdam", country: "niederlande", flag: "🇳🇱", name: "Amsterdam & Nordsee", region: "Grachten + Dünen",
    color: "bg-camel",
    blurb: "Stadt und Meer in einem Trip: tagsüber Grachten, abends in den Dünen von Zandvoort stehen.",
    stellplatz: "Camperpark Amsterdam, mit Fähre in 15 Min. im Zentrum.",
    zeit: "April (Tulpen!) oder August.",
    tipp: "Fahrrad mitnehmen — der Bulli bleibt stehen, du rollst überall hin."
  },
  {
    id: "duesseldorf", country: "deutschland", flag: "🇩🇪", name: "Düsseldorf", region: "Rhein & Altstadt",
    color: "bg-blue",
    blurb: "Rheinpromenade, die „längste Theke der Welt“ und moderne Architektur im Medienhafen.",
    stellplatz: "Reisemobilhafen am Robert-Lehr-Ufer, direkt am Rhein & nah an der Altstadt.",
    zeit: "Frühling bis Herbst.",
    tipp: "Ein Altbier in der Altstadt — solange du nicht abwinkst, wird nachgeschenkt."
  },
  {
    id: "koeln", country: "deutschland", flag: "🇩🇪", name: "Köln", region: "Dom & Rhein",
    color: "bg-deep",
    blurb: "Der Dom, der Rhein und dieses kölsche Lebensgefühl — Großstadt, die sich wie ein Dorf anfühlt.",
    stellplatz: "Wohnmobilstellplatz Köln-Riehl / am Rheinpark, mit KVB-Bahn in Domnähe.",
    zeit: "Ganzjährig; Karneval nur für Hartgesottene.",
    tipp: "Über die Hohenzollernbrücke laufen und die Schlösser-Aussicht mitnehmen."
  },
  {
    id: "bonn", country: "deutschland", flag: "🇩🇪", name: "Bonn", region: "Beethoven & Rhein",
    color: "bg-army",
    blurb: "Ehemalige Hauptstadt, Beethovens Geburtsstadt und ein grüner, entspannter Rheinbogen.",
    stellplatz: "Wohnmobilstellplatz am Rheinufer (Bonn / Bad Godesberg).",
    zeit: "Frühling & Sommer, wenn die Kirschblüte in der Altstadt blüht.",
    tipp: "Im April die rosa Kirschblütengasse in der Altstadt — Postkarte pur."
  },
  {
    id: "paris", country: "frankreich", flag: "🇫🇷", name: "Paris — direkt am Eiffelturm?", region: "Stadt der Liebe",
    color: "bg-terra",
    blurb: "Eiffelturm, Louvre, Seine — Paris mit dem Camper geht, wenn man weiß, wo man legal steht.",
    stellplatz: "Direkt am Eiffelturm darf man NICHT übernachten. Zentrumsnächste legale Adresse: Camping Huttopia Paris (Bois de Boulogne), am Seine-Ufer im 16. Arrondissement — Gratis-Shuttle zur Metro Porte Maillot, dann ~15 Min. bis zum Eiffelturm.",
    zeit: "April–Juni & September; Sommer ist voll, im Winter ruhiger.",
    tipp: "Metro-Wochenkarte holen und den Bulli stehen lassen — Parken in Paris ist Nervensache."
  },
  {
    id: "normandie", country: "frankreich", flag: "🇫🇷", name: "Normandie", region: "Klippen & Calvados",
    color: "bg-camel",
    blurb: "Étretat bei Ebbe, Camembert vom Hof und Geschichte an jedem Strand.",
    stellplatz: "Aire Municipale in Yport — 5 € mit Meerblick.",
    zeit: "Mai, Juni oder goldener Oktober.",
    tipp: "Markt in Honfleur am Samstag — Budget fürs Käsefach einplanen."
  },
  {
    id: "biarritz", country: "frankreich", flag: "🇫🇷", name: "Biarritz & Baskenland", region: "Surf & Pintxos",
    color: "bg-blue",
    blurb: "Atlantikwellen, grüne Hügel und die entspannteste Vanlife-Community Europas.",
    stellplatz: "Aire de Bidart, fußläufig zum Strand — früh kommen!",
    zeit: "September/Oktober: warmes Wasser, leere Line-ups.",
    tipp: "Über die Grenze nach San Sebastián zum Pintxos-Essen tingeln."
  },
  {
    id: "andalusien", country: "spanien", flag: "🇪🇸", name: "Andalusien", region: "Tapas & Bergdörfer",
    color: "bg-terra",
    blurb: "Weiße Dörfer, Flamenco aus offenen Fenstern und Bergstraßen, die der T4 gerade so schafft.",
    stellplatz: "Área de El Chorro — Ausgangspunkt für den Caminito del Rey.",
    zeit: "März–Mai oder Oktober, Sommer ist Backofen.",
    tipp: "Tanken & Wasser in den Dörfern — unterwegs kommt lange nichts."
  },
  {
    id: "barcelona", country: "spanien", flag: "🇪🇸", name: "Barcelona", region: "Gaudí & Mittelmeer",
    color: "bg-blue",
    blurb: "Sagrada Família, Tapas-Gassen und Stadtstrand — Metropole und Meer in einem.",
    stellplatz: "Camping Tres Estrellas / El Toro Bravo südlich der Stadt, mit Bahn ins Zentrum.",
    zeit: "Mai, Juni & September.",
    tipp: "Sagrada-Família-Tickets vorab online — die Schlange vor Ort ist endlos."
  },
  {
    id: "calella", country: "spanien", flag: "🇪🇸", name: "Calella & Costa Brava", region: "Buchten & Steilküste",
    color: "bg-camel",
    blurb: "Türkise Buchten, Pinien bis ans Wasser und Küstenpfade — die Costa Brava nördlich von Barcelona.",
    stellplatz: "Campingplätze rund um Calella / Pals, viele direkt am Meer.",
    zeit: "Juni–September, Wasser bleibt bis Oktober warm.",
    tipp: "Den Camí de Ronda wandern — Küstenpfad von Bucht zu Bucht."
  },
  {
    id: "marseille", country: "frankreich", flag: "🇫🇷", name: "Marseille & Calanques", region: "Hafen & Felsbuchten",
    color: "bg-deep",
    blurb: "Rauer Hafencharme und gleich daneben die Calanques — weiße Kalkfelsen über türkisem Wasser.",
    stellplatz: "Stellplätze Richtung Cassis; von dort in die Calanques wandern.",
    zeit: "Mai–Juni & September (im Hochsommer teils Zufahrtssperren wegen Waldbrandgefahr).",
    tipp: "Frühmorgens zur Calanque d'En-Vau starten, bevor die Hitze kommt."
  },
  {
    id: "provence", country: "frankreich", flag: "🇫🇷", name: "Provence", region: "Lavendel & Ockerfelsen",
    color: "bg-army",
    blurb: "Zwischen Lavendelfeldern und Ockerschluchten riecht sogar der Motorraum gut.",
    stellplatz: "France Passion: bei Winzern stehen — kostenlos, ein Karton Wein ist Ehrensache.",
    zeit: "Ende Juni/Anfang Juli zur Lavendelblüte.",
    tipp: "Sénanque-Abtei vor 8 Uhr — danach kommen die Busse."
  },
  {
    id: "genua", country: "italien", flag: "🇮🇹", name: "Genua & Ligurien", region: "Hafenstadt & Cinque Terre",
    color: "bg-terra",
    blurb: "Verwinkelte Altstadt, bestes Pesto und das Tor zu den Cinque Terre.",
    stellplatz: "Stellplätze rund um Genua / Sestri Levante; in die Cinque Terre besser per Zug.",
    zeit: "Mai, Juni & September.",
    tipp: "Focaccia zum Frühstück — in Ligurien völlig normal und herrlich."
  },
  {
    id: "pisa", country: "italien", flag: "🇮🇹", name: "Pisa", region: "Schiefer Turm",
    color: "bg-blue",
    blurb: "Der schiefe Turm live — kleiner als gedacht, aber ein Muss. Schnell besucht, gut kombinierbar.",
    stellplatz: "Camping / Area Sosta bei Pisa, Shuttle oder Rad zur Piazza dei Miracoli.",
    zeit: "Frühling & Herbst; Sommer heiß und voll.",
    tipp: "Turmfoto abhaken und weiter nach Lucca — die schönere, ruhigere Nachbarstadt."
  },
  {
    id: "florenz", country: "italien", flag: "🇮🇹", name: "Florenz", region: "Renaissance-Wiege",
    color: "bg-deep",
    blurb: "Dom, Uffizien und toskanisches Licht — eine Stadt wie ein begehbares Gemälde.",
    stellplatz: "Area Camper Firenze (Villa Costanza), mit Straßenbahn direkt ins Zentrum.",
    zeit: "April–Mai & Oktober.",
    tipp: "Sonnenuntergang am Piazzale Michelangelo — ganz Florenz zu Füßen, gratis."
  },
  {
    id: "rom", country: "italien", flag: "🇮🇹", name: "Rom", region: "Ewige Stadt",
    color: "bg-army",
    blurb: "Kolosseum, Trevi-Brunnen, Pizza al taglio — 3.000 Jahre Geschichte an jeder Ecke.",
    stellplatz: "Camping Village Roma / Fabulous, mit Bus & Metro ins Zentrum.",
    zeit: "April–Juni & Oktober; Sommer glühend heiß.",
    tipp: "Frühmorgens zum Trevi-Brunnen — vor 7 Uhr fast menschenleer."
  },
  {
    id: "venedig", country: "italien", flag: "🇮🇹", name: "Venedig", region: "Lagunenstadt",
    color: "bg-blue",
    blurb: "Kanäle statt Straßen, Gondeln statt Autos — einmal im Leben ein Muss.",
    stellplatz: "Camping / Area Sosta in Fusina oder Punta Sabbioni, mit dem Vaporetto rüber.",
    zeit: "April–Mai & September/Oktober (Hochwasser eher im Spätherbst).",
    tipp: "Den Bulli am Festland lassen und mit dem Boot kommen — in Venedig fährt kein Auto."
  },
  {
    id: "istrien", country: "kroatien", flag: "🇭🇷", name: "Istrien", region: "Adria & Trüffel",
    color: "bg-terra",
    blurb: "Kristallwasser, Steinbuchten und Trüffelpasta für kleines Geld — Kroatiens sanfter Norden.",
    stellplatz: "Camp Mon Perin bei Bale — riesig, naturbelassen, direkt am Meer.",
    zeit: "Juni oder September, Wasser bleibt bis Oktober warm.",
    tipp: "Motovun bei Abendlicht — der Blick übers Mirna-Tal ist Postkarte pur."
  },
  {
    id: "gardasee", country: "italien", flag: "🇮🇹", name: "Gardasee", region: "Dolce Vita am Wasser",
    color: "bg-blue",
    blurb: "Espresso am Hafen, Gelato zum Sonnenuntergang und Bergstraßen mit Panorama-Garantie.",
    stellplatz: "Area Sosta in Manerba, ruhige Südwest-Ecke des Sees.",
    zeit: "Mai/Juni oder September.",
    tipp: "Die Westuferstraße SS45bis früh morgens fahren — Tunnel + Seeblick = Kino."
  },
  {
    id: "bodensee", country: "deutschland", flag: "🇩🇪", name: "Zeppelin Museum am Bodensee", region: "Friedrichshafen",
    color: "bg-deep",
    blurb: "Luftschiff-Geschichte zum Anfassen in Friedrichshafen — und rundherum der glitzernde Bodensee.",
    stellplatz: "Wohnmobilstellplatz Friedrichshafen am See, fußläufig zum Zeppelin Museum.",
    zeit: "April–Oktober.",
    tipp: "Mit dem Katamaran nach Konstanz übersetzen — Seeausflug ohne Stau."
  },
  {
    id: "tirol", country: "oesterreich", flag: "🇦🇹", name: "Tirol", region: "Pässe & Bergseen",
    color: "bg-army",
    blurb: "Serpentinen hoch, Kühlwasser im Blick, oben Kaiserschmarrn — Alpenrunden sind T4-Therapie.",
    stellplatz: "Camping Ötztal Längenfeld, mit Bergblick aus der Heckklappe.",
    zeit: "Juni–September, Pässe sind sonst zu.",
    tipp: "Timmelsjoch statt Brenner: mautig, aber jede Kurve ein Foto."
  },
  {
    id: "leipzig", country: "deutschland", flag: "🇩🇪", name: "Leipzig", region: "Kultur & Kanäle",
    color: "bg-terra",
    blurb: "Kreativstadt mit Bachs Erbe, hippen Vierteln und Kanälen zum Paddeln.",
    stellplatz: "Wohnmobilstellplatz am Cospudener See / auenrandlich, mit Bahn in die City.",
    zeit: "Frühling bis Herbst.",
    tipp: "Im Sommer durch die Leipziger Kanäle paddeln — die Stadt vom Wasser aus."
  },
  {
    id: "dresden", country: "deutschland", flag: "🇩🇪", name: "Dresden", region: "Elbflorenz",
    color: "bg-blue",
    blurb: "Frauenkirche, Zwinger und die Elbe — barocke Pracht, wunderschön wieder aufgebaut.",
    stellplatz: "Wohnmobilstellplatz an der Marienbrücke / Messe, zu Fuß & Bahn in die Altstadt.",
    zeit: "Frühling bis Herbst; Advent für die Striezelmarkt-Fans.",
    tipp: "Elbwiesen-Blick von der Neustädter Seite auf die Altstadt-Silhouette."
  },
  {
    id: "berlin", country: "deutschland", flag: "🇩🇪", name: "Berlin — nah am Brandenburger Tor?", region: "Hauptstadt",
    color: "bg-deep",
    blurb: "Brandenburger Tor, Mauerreste, Museen und Nächte, die nie enden — Berlin mit dem Camper ist machbar.",
    stellplatz: "Direkt am Brandenburger Tor darf man NICHT übernachten (Innenstadt-Verbot). Zuverlässig & legal: z. B. DCC-Campingplatz Berlin-Gatow oder Campingplatz Am Krossinsee — von dort mit S-/U-Bahn ~30–45 Min. bis zum Brandenburger Tor. Private City-Stellplätze wechseln häufig, daher vorher aktuell prüfen.",
    zeit: "Mai–September; Museen & Clubs ganzjährig.",
    tipp: "BVG-Tageskarte lösen und den Bulli stehen lassen — Berlin fährt sich am besten mit der Bahn."
  },
  {
    id: "breslau", country: "polen", flag: "🇵🇱", name: "Breslau / Wrocław", region: "Zwerge & Marktplatz",
    color: "bg-army",
    blurb: "Bunter Ring, über 300 versteckte Bronze-Zwerge und Inseln in der Oder — Polens heimliche Perle.",
    stellplatz: "Campingplatz / Stellplatz nahe der Oder, zu Fuß oder per Tram in die Altstadt.",
    zeit: "Mai–September.",
    tipp: "Zwerge suchen ist das inoffizielle Stadtspiel — Kinder lieben es, Erwachsene auch."
  },
  {
    id: "krakau", country: "polen", flag: "🇵🇱", name: "Kraków", region: "Königsstadt",
    color: "bg-terra",
    blurb: "Mittelalterlicher Marktplatz, Wawel-Schloss und lebendiges Kazimierz — Polens schönste Altstadt.",
    stellplatz: "Camping Clepardia / Smok am Stadtrand, mit Tram/Bus ins Zentrum.",
    zeit: "Mai–September; Altstadt ganzjährig stimmungsvoll.",
    tipp: "Abends in Kazimierz durch die Bar- und Foodtruck-Höfe ziehen."
  },
  {
    id: "warschau", country: "polen", flag: "🇵🇱", name: "Warschau", region: "Hauptstadt Polens",
    color: "bg-blue",
    blurb: "Wieder aufgebaute Altstadt, Wolkenkratzer daneben und grüne Weichsel-Ufer — Kontraste pur.",
    stellplatz: "Campingplatz / Stellplatz nahe der Weichsel, mit Metro & Tram ins Zentrum.",
    zeit: "Mai–September.",
    tipp: "Am rechten Weichselufer (Praga) die Strand-Bars — Großstadt mit Sandstrand-Feeling."
  },
  {
    id: "posen", country: "polen", flag: "🇵🇱", name: "Posen / Poznań", region: "Zwischenstopp mit Charme",
    color: "bg-camel",
    blurb: "Prachtvoller Marktplatz mit den kämpfenden Ziegenböckchen am Rathaus — perfekter Halt auf dem Heimweg.",
    stellplatz: "Stellplatz / Camping am Malta-See, zu Fuß am Wasser, Tram ins Zentrum.",
    zeit: "Mai–September.",
    tipp: "Mittags um 12 zum Rathaus: die mechanischen Ziegenböcke stoßen die Köpfe zusammen."
  },
  {
    id: "tschenstochau", country: "polen", flag: "🇵🇱", name: "Częstochowa / Tschenstochau", region: "Historischer Wallfahrtsort",
    color: "bg-terra",
    blurb: "Der berühmte Wallfahrtsort mit dem Kloster Jasna Góra und der „Schwarzen Madonna\" — ein stiller, beeindruckender Zwischenstopp auf dem Weg in den Norden.",
    stellplatz: "Parkplätze und Stellplätze rund um Jasna Góra, von dort zu Fuß hoch zum Kloster.",
    zeit: "Mai–September; an hohen Feiertagen sehr voll mit Pilgern.",
    tipp: "Zur stillen Zeit früh morgens hoch — der Blick über die Stadt vom Klosterberg lohnt sich."
  },
  {
    id: "danzig", country: "polen", flag: "🇵🇱", name: "Danzig / Gdańsk", region: "Ostsee & Hanse",
    color: "bg-blue",
    blurb: "Der krönende Norden dieser Reise: prächtige Hansestadt an der Ostsee, langer Markt, Backsteingotik und Bernstein — und das Meer gleich nebenan.",
    stellplatz: "Stellplätze Richtung Strand (Brzeźno/Stogi), mit Tram bequem in die Altstadt.",
    zeit: "Juni–September, dann ist die Ostsee am schönsten.",
    tipp: "Am Langen Markt einen echten Bernstein suchen und barfuß am breiten Sandstrand von Brzeźno laufen."
  }
];
