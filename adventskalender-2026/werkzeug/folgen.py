"""Drehbuch aller 24 Folgen. Texte wörtlich bzw. gekürzt aus dem Adventskalender 2026 (Systemfehler Familie).

Figur: F(basis, [posen], slot, ...). Basis z. B. 'k01_heute', 'k03_damals', 'mama01', 'beamter'.
Ton je Pose: 'still~sepia' (damals) oder 'traurig~faded' (60er-Jahre).
Zeilen in der Akte mit '!' am Anfang erscheinen als Stempel.
"""


def F(base, poses, slot, **kw):
    d = {"base": base, "poses": poses, "slot": slot}
    d.update(kw)
    return d


def H(k):
    return f"k{k:02d}_heute"


def D(k):
    return f"k{k:02d}_damals"


def S(poses):
    return [p + "~sepia" for p in poses]


def FA(poses):
    return [p + "~faded" for p in poses]


FOLGEN = {}


def folge(tag, kind, a, b, epoche, damals, recht, schluss, wandel=None, ende_posen=None):
    FOLGEN[tag] = {
        "tag": tag, "kind_heute": H(kind), "a": a, "b": b, "epoche": epoche, "damals": damals, "recht": recht,
        "schluss": schluss, "wandel": wandel or {"ziel": (D(kind), "traurig~sepia")},
        **({"ende_posen": ende_posen} if ende_posen else {}),
    }


# ---------------------------------------------------------------- 1
folge(1, 1,
      a={"raum": "flur", "zeilen": ["Mama, heb meinen Platz auf.", "Hier steht auch ein Weihnachtsbaum.",
                                    "Ein Weihnachtsbaum kann ja nichts dafür, dass er im falschen Zimmer steht."],
         "figuren": [F(H(3), ["froehlich", "hoffnungsvoll"], "back-l", follow=False, at=[7]),
                     F(H(8), ["froehlich"], "back-c"), F(H(5), ["ueberrascht", "froehlich"], "back-r", follow=False, at=[9]),
                     F(H(1), ["traurig", "nachdenklich", "weinend"], "hero")]},
      b={"raum": "wohnzimmer", "zeilen": ["Ich weiß noch, wie mein Stuhl an unserem Tisch klingt.",
                                          "Manchmal habe ich Angst, dass ihr euch daran gewöhnt, dass mein Platz leer bleibt."],
         "figuren": [F(H(1), ["hoffnungsvoll", "traurig"], "hero-l", ghost=True, fade_in=0.5, fade_out=9.6)]},
      epoche="KAISERREICH",
      damals={"raum": "speisesaal", "zeilen": ["Bevor es Jugendämter gab, wurden Kinder bereits in Anstalten erzogen.",
                                               "Religiöse Unterweisung, Arbeit, Ordnung, Gehorsam.",
                                               "Wie muss ein Kind werden, damit es den Erwartungen der Erwachsenen entspricht?"],
              "quelle": "Diakonie Deutschland – Erziehungshilfe im historischen Verlauf",
              "figuren": [F(D(4), S(["gefaltet"]), "back-l"), F(D(6), S(["gefaltet"]), "back-c"), F(D(7), S(["gefaltet"]), "back-r"),
                          F("erzieherin", S(["glocke", "zeigt", "streng"]), "mid-r"),
                          F(D(1), S(["still", "aengstlich", "weinend"]), "hero-l")]},
      recht={"titel": "Ein Kind muss kein perfekter Gesprächspartner sein, um beteiligt zu werden.", "paragraph": "§ 8 SGB VIII",
             "sub": "Beteiligung an Entscheidungen, die das Kind betreffen. Es darf sich auch selbst an das Jugendamt wenden.",
             "quelle": "§ 8 SGB VIII, Beteiligung von Kindern"},
      schluss="Ich weiß noch genau, wohin ich gehöre.")

# ---------------------------------------------------------------- 2
folge(2, 2,
      a={"raum": "kinderzimmer_nacht", "zeilen": ["Ich verstecke einen Brief an meine Mama.", "Das Blatt liegt unter meinem Kopfkissen.",
                                                  "Also habe ich einen kleinen Stern gemalt."],
         "figuren": [F(H(2), ["bett", "brief", "hoffnungsvoll"], "hero")]},
      b={"raum": "kinderzimmer_tag", "zeilen": ["Dann habe ich doch geschrieben: Ich will nach Hause.",
                                                "Mama, wenn du ihn bekommst: Der Stern heißt, dass ich dich liebe."],
         "figuren": [F(H(2), ["schreibt", "sitz_nachdenklich", "sitz_hoffnungsvoll"], "hero")]},
      epoche="1922",
      damals={"raum": "amtsstube", "zeilen": ["Am 9. Juli 1922 wurde das Reichsjugendwohlfahrtsgesetz erlassen.",
                                              "Ein Erziehungsanspruch für jedes deutsche Kind.",
                                              "Die entscheidende Frage blieb: Wer setzt es durch?"],
              "quelle": "Reichsjugendwohlfahrtsgesetz vom 9. Juli 1922, RGBl. I S. 633 ff.",
              "figuren": [F("beamter", S(["schreibt", "unterschreibt", "stempelt"]), "mid-r"),
                          F(D(2), S(["still", "nachdenklich", "traurig"]), "hero-l")]},
      recht={"titel": "Ein Hilfeplan soll erklären, wie Hilfe wirkt.", "paragraph": "§ 36 SGB VIII",
             "sub": "Gemeinsam mit Eltern und Kind aufgestellt – und regelmäßig überprüft.",
             "quelle": "§ 36 SGB VIII, Mitwirkung und Hilfeplan"},
      schluss="Der andere Satz heißt genau das, was da steht.")

# ---------------------------------------------------------------- 3
folge(3, 3,
      a={"raum": "kinderzimmer_tag", "zeilen": ["Im Wunschzettel habe ich alles durchgestrichen.", "Bis auf: nach Hause.",
                                                "Ich möchte auf unserem Sofa sitzen."],
         "figuren": [F(H(3), ["malt", "sitz_traurig", "sitz_hoffnungsvoll"], "hero")]},
      b={"raum": "kueche_zuhause", "zeilen": ["Ich möchte hören, wie du in der Küche die Schublade zumachst.",
                                              "Mama, du musst keine Schleife darum machen."],
         "figuren": [F("mama01", ["tisch", "hoffnungsvoll"], "mid-r"),
                     F(H(3), ["hoffnungsvoll", "froehlich"], "hero-l", ghost=True, fade_in=0.6)]},
      epoche="WEIMAR",
      damals={"raum": "gerichtssaal", "zeilen": ["Ein Gericht ordnete an.", "Ein Amt organisierte.", "Das Kind musste damit leben."],
              "quelle": "LWL: Forschungsbericht zur Heimerziehung in Westfalen",
              "figuren": [F("beamter", S(["ernst", "ueberreicht", "kopfschuetteln"]), "mid-r"),
                          F(D(3), S(["still", "aengstlich", "traurig"]), "hero-l")]},
      recht={"titel": "Über uns wurde gesprochen. Aber wir waren nicht eingeladen.", "paragraph": "§ 36 SGB VIII",
             "sub": "Gemeinsame Planung mit Kind und Eltern – eine interne Fachrunde ersetzt sie nicht.",
             "quelle": "§ 36 SGB VIII, § 25 SGB X"},
      schluss="Mach einfach die Tür auf, wenn ich wiederkommen darf.")

# ---------------------------------------------------------------- 4
folge(4, 4,
      a={"raum": "gemeinschaftsraum", "zeilen": ["Ich übe mein „Mir geht’s gut“, bevor ich dich anrufe.",
                                                 "Ich höre jemanden im Flur.", "Also sage ich, dass es mir gut geht."],
         "figuren": [F("betreuerin", ["akte", "nachdenklich"], "back-r"),
                     F(H(4), ["tel_tapfer", "tel_traurig", "tel_tapfer"], "hero")]},
      b={"raum": "kueche_zuhause", "zeilen": ["Du fragst noch einmal. Ganz vorsichtig.",
                                              "Frag, ob ich gerade wirklich frei reden kann."],
         "figuren": [F("mama01", ["tel_traurig", "tel_laechelnd", "tel_traurig"], "hero")]},
      epoche="1922",
      damals={"raum": "amtsstube", "zeilen": ["Ein Wort konnte darüber entscheiden, ob ein Kind zu Hause blieb.", "!Verwahrlosung",
                                              "Der Begriff ist älter als der Zweite Weltkrieg."],
              "quelle": "Reichsjugendwohlfahrtsgesetz vom 9. Juli 1922",
              "figuren": [F("beamter", S(["notiert", "stempelt", "ernst"]), "mid-r"),
                          F(D(4), S(["nachdenklich", "aengstlich", "traurig"]), "hero-l")]},
      recht={"titel": "Was passiert, wenn gar keine Hilfeplanung stattfindet?", "paragraph": "§ 37c SGB VIII",
             "sub": "Bei Hilfen außerhalb der Familie muss die Perspektive fortlaufend geklärt werden.",
             "quelle": "§ 36 und § 37c SGB VIII"},
      schluss="Ich weiß sonst manchmal nicht, wie ich anfangen soll.")

# ---------------------------------------------------------------- 5
folge(5, 5,
      a={"raum": "konferenzraum", "zeilen": ["Für das Gespräch über mein Leben war kein Platz für mich.",
                                             "Ich habe meine Fragen auf einen Zettel geschrieben.",
                                             "Dann habe ich gehört, dass über mich gesprochen wurde."],
         "figuren": [F("jugendamt", ["akte", "schreibt"], "back-l"), F("betreuerin", ["hoertzu", "erklaert"], "back-r"),
                     F(H(5), ["wartet", "traurig", "weinend"], "hero")]},
      b={"raum": "eingang", "zeilen": ["Ich war nicht dabei.", "Meinen Zettel habe ich noch."],
         "figuren": [F(H(5), ["traurig", "wartet"], "hero")]},
      epoche="HAMBURG",
      damals={"raum": "untersuchung", "zeilen": ["Kinder wurden nach ihrem angeblichen „Erbwert“ sortiert.",
                                                 "Heime wurden nach dem behaupteten Erbwert ihrer Bewohner eingeteilt.",
                                                 "Ein dokumentierter Teil der Geschichte öffentlicher Erziehung."],
              "quelle": "Hamburg, Landesbetrieb Erziehung und Beratung",
              "figuren": [F("beamter", S(["notiert", "ernst"]), "mid-r"),
                          F(D(5), S(["still", "aengstlich", "weinend"]), "hero-l")]},
      recht={"titel": "„Irgendwann vielleicht nach Hause“ ist noch keine Rückkehrperspektive.", "paragraph": "§ 37c SGB VIII",
             "sub": "Welche Voraussetzungen fehlen für eine Rückkehr – und was soll dafür geschehen?",
             "quelle": "§ 37c SGB VIII, Perspektivklärung"},
      schluss="Wann darf ich meinen Zettel endlich vorlesen?")

# ---------------------------------------------------------------- 6
folge(6, 6,
      a={"raum": "eingang", "zeilen": ["Ich habe meine Schuhe schon angezogen.",
                                       "Den Zettel mit meinen Fragen habe ich in die Jackentasche gesteckt.",
                                       "Aber unser Gespräch findet wieder nicht statt."],
         "figuren": [F(H(6), ["wartet", "hoffnungsvoll", "traurig"], "hero")]},
      b={"raum": "kinderzimmer_tag", "zeilen": ["Die Sätze der Erwachsenen waren länger als meine Fragen.",
                                                "Wohin gehen die Tage, die ich schon geduldig gewesen bin?"],
         "figuren": [F(H(6), ["sitz_traurig", "sitz_weinend"], "hero")]},
      epoche="BREMEN",
      damals={"raum": "amtsstube", "zeilen": ["Die Verfolgung begann nicht erst am Lagertor.", "Sie hatte einen Verwaltungsweg.",
                                              "Jugendamt, Schulen, Gesundheitswesen und Polizei standen in Verbindung."],
              "quelle": "Diakonie Bremen / Gerda Engelbracht: NS-Jugendfürsorge",
              "figuren": [F("beamter", S(["ueberreicht", "stempelt", "unterschreibt"]), "mid-r"),
                          F(D(6), S(["koffer", "aengstlich", "traurig"]), "hero-l")]},
      recht={"titel": "Eine Mutter hört nicht auf, Mutter zu sein.", "paragraph": "§ 37 SGB VIII",
             "sub": "Eltern haben Anspruch auf Beratung, Unterstützung und Förderung ihrer Beziehung zum Kind.",
             "quelle": "§ 37 SGB VIII, Beratung der Eltern",
             "figuren": [F("mama02", ["traurig", "hoffnungsvoll", "arme"], "mid-r", follow=False, at=[4, 7]),
                         F(H(6), ["nachdenklich", "hoffnungsvoll"], "hero-l", enter="left", follow=False, at=[5])]},
      schluss="Bekomme ich die Tage mit Mama irgendwann zurück?")

# ---------------------------------------------------------------- 7
folge(7, 7,
      a={"raum": "kinderzimmer_nacht", "zeilen": ["Ich habe vergessen, wie du mich morgens weckst.", "Davor habe ich Angst.",
                                                  "Wenn schon so eine kleine Sache weggehen kann, was vergesse ich als Nächstes?"],
         "figuren": [F(H(7), ["bett", "aengstlich", "nachdenklich"], "hero")]},
      b={"raum": "wohnzimmer", "zeilen": ["Unseren Tisch. Meine Tasse.", "Dann sammle ich dich wieder ein."],
         "figuren": [F("mama02", ["fenster", "hoffnungsvoll"], "mid-r", ghost=True, fade_in=0.5),
                     F(H(7), ["nachdenklich", "hoffnungsvoll"], "hero-l")]},
      epoche="1938",
      damals={"raum": "amtsstube", "zeilen": ["„Asozial“ war keine Beschreibung eines Kindes.", "!Asozial",
                                              "Es war ein Werkzeug seiner Ausgrenzung."],
              "quelle": "Landesarchiv Sachsen-Anhalt",
              "figuren": [F("beamter", S(["schreibt", "stempelt", "ernst"]), "mid-r"),
                          F(D(7), S(["still", "aengstlich", "weinend"]), "hero-l")]},
      recht={"titel": "Familienkontakt ist keine Belohnung für angepasstes Verhalten.", "paragraph": "§ 1684 BGB",
             "sub": "Das Kind hat ein Recht auf Umgang mit jedem Elternteil.", "quelle": "§ 1684 BGB, Umgang mit den Eltern"},
      schluss="Ich will deinen Satz wieder richtig hören.")

# ---------------------------------------------------------------- 8
folge(8, 8,
      a={"raum": "garten", "zeilen": ["Ich war heute fröhlich.", "Beim Spielen habe ich so gelacht, dass mir der Bauch wehgetan hat.",
                                      "Danach hatte ich Angst, dass ich dich verraten habe."],
         "figuren": [F(H(3), ["froehlich", "ueberrascht"], "back-l"), F(H(7), ["froehlich"], "back-r"),
                     F(H(8), ["froehlich", "froehlich", "nachdenklich"], "hero")]},
      b={"raum": "gemeinschaftsraum", "zeilen": ["Ein Lachen erzählt nicht meinen ganzen Tag.",
                                                 "Mama, darf beides nebeneinander in mir sein?"],
         "figuren": [F(H(8), ["sitz_nachdenklich", "sitz_traurig", "sitz_hoffnungsvoll"], "hero")]},
      epoche="UCKERMARK",
      damals={"raum": "lager", "zeilen": ["Im Juni 1942 kamen die ersten Mädchen in das Jugendlager Uckermark.",
                                          "Etwa 1.200 Mädchen und junge Frauen waren dort inhaftiert.",
                                          "Erwachsene hatten sie für unerziehbar erklärt."],
              "quelle": "Martin Guse / bpb: Das Jugend-KZ Uckermark 1942–1945",
              "figuren": [F(D(5), S(["still"]), "back-l"), F(D(9), S(["still"]), "back-r"),
                          F(D(8), S(["still", "aengstlich", "weinend"]), "hero")]},
      recht={"titel": "Ein Kind braucht einen Ort, an dem es den wichtigen Satz sagen kann.", "paragraph": "Art. 16 UN-KRK",
             "sub": "Schutz vor willkürlichen Eingriffen in Privatleben, Familie und Schriftverkehr.",
             "quelle": "UN-Kinderrechtskonvention, Artikel 16"},
      schluss="Ich kann einen Witz lustig finden und trotzdem nach Hause wollen.")

# ---------------------------------------------------------------- 9
folge(9, 9,
      a={"raum": "garten", "blitz": 4.4, "zeilen": ["Auf dem Gruppenfoto lächle ich.", "Heute wurde ein Foto gemacht.",
                                                    "Du siehst nicht, wie oft ich vorher zur Tür geschaut habe."],
         "figuren": [F(H(1), ["froehlich"], "back-l"), F(H(4), ["froehlich"], "back-c"), F(H(6), ["froehlich"], "back-r"),
                     F(H(9), ["froehlich", "froehlich", "nachdenklich"], "hero")]},
      b={"raum": "eingang", "zeilen": ["Du fehlst auch mit Weihnachtsmütze.",
                                       "Glaub bitte nicht, dass ich aufgehört habe, zur Tür zu schauen."],
         "figuren": [F(H(9), ["hinten", "traurig"], "hero")]},
      epoche="MORINGEN",
      damals={"raum": "lager", "zeilen": ["Im August 1940 wurde in Moringen das erste Jugendkonzentrationslager eingerichtet.",
                                          "!Unerziehbar", "Etwa 1.400 Jugendliche und junge Männer waren dort inhaftiert."],
              "quelle": "KZ-Gedenkstätte Moringen: Jugend-KZ 1940–1945",
              "figuren": [F(D(2), S(["still"]), "back-l"), F(D(6), S(["still"]), "back-r"),
                          F(D(9), S(["still", "aengstlich", "traurig"]), "hero")]},
      recht={"titel": "Geschwister gehören zur Geschichte eines Kindes.", "paragraph": "§ 1685 BGB",
             "sub": "Umgang mit Geschwistern – ihre Beziehung gehört auch in den Hilfeplan.",
             "quelle": "§ 1685 BGB, § 36 SGB VIII",
             "figuren": [F(H(6), ["nachdenklich", "froehlich"], "mid-r", follow=False, at=[6]),
                         F(H(9), ["nachdenklich", "hoffnungsvoll"], "hero-l", enter="left", follow=False, at=[5])]},
      schluss="Manchmal schaue ich noch, obwohl längst niemand mehr kommen kann.")

# ---------------------------------------------------------------- 10
folge(10, 1,
      a={"raum": "konferenzraum", "zeilen": ["Die Frage war eigentlich einfach: Wie geht es dir hier?",
                                             "Ich wusste sofort eine Antwort.", "Dann habe ich überlegt, wer sie später erfahren würde."],
         "figuren": [F("betreuerin", ["hoertzu", "nachdenklich"], "mid-r"),
                     F(H(1), ["sitz_nachdenklich", "sitz_hoffnungsvoll", "sitz_traurig"], "hero-l")]},
      b={"raum": "kinderzimmer_nacht", "zeilen": ["Ich bin nicht still, weil ich nichts zu sagen habe.",
                                                  "Ich bin still, weil ich Angst vor danach habe."],
         "figuren": [F(H(1), ["knie", "sitz_traurig"], "hero")]},
      epoche="POLEN",
      damals={"raum": "dorfstrasse", "zeilen": ["Polnische Kinder wurden geraubt.", "Die Nationalsozialisten erklärten sie für „deutsch“.",
                                                "Ein Ziel war die gewaltsame Germanisierung."],
              "quelle": "bpb: Der Lebensborn e. V. und die Zwangsverschleppung von Kindern",
              "figuren": [F("mutter1940", S(["ruft", "verzweifelt", "arme"]), "mid-r"),
                          F(D(1), S(["koffer", "aengstlich", "weinend"]), "hero-l")]},
      recht={"titel": "Eine Ombudsstelle auf einer Liste hilft noch keinem Kind.", "paragraph": "§ 9a SGB VIII",
             "sub": "Unabhängige Ombudsstellen – erreichbar, vertraulich und verständlich erklärt.",
             "quelle": "§ 9a SGB VIII, Ombudsstellen"},
      schluss="Helft mir erst, mich sicher genug zu fühlen.")

# ---------------------------------------------------------------- 11
folge(11, 2,
      a={"raum": "gemeinschaftsraum", "zeilen": ["Auf einem Blatt stehen Telefonnummern.",
                                                 "Hallo, ich bin ein Kind. Ich weiß nicht, ob ich hier richtig bin.",
                                                 "Schon bei diesem Satz wurde mein Hals eng."],
         "figuren": [F(H(2), ["brief", "tel_tapfer", "tel_traurig"], "hero")]},
      b={"raum": "fenster", "zeilen": ["Ich kenne die Adresse meiner Hilfe nicht.", "Zeigt mir, wie ich dort wirklich ankomme."],
         "figuren": [F(H(2), ["hinten", "hoffnungsvoll"], "hero")]},
      epoche="1941",
      damals={"raum": "untersuchung", "zeilen": ["Blonde Haare waren nicht die ganze Geschichte.",
                                                 "Die Auswahl folgte rassistischen Prüfungen.",
                                                 "Auch Kinder mit dunklen Haaren konnten ausgewählt werden."],
              "quelle": "Ausstellung „Uprooted“",
              "figuren": [F("beamter", S(["notiert", "schreibt"]), "mid-r"),
                          F(D(2), S(["still", "aengstlich", "traurig"]), "hero-l")]},
      recht={"titel": "Ist die Einrichtung das Problem, braucht das Kind einen Weg nach draußen.", "paragraph": "§ 45 SGB VIII",
             "sub": "Beschwerdemöglichkeiten innerhalb und außerhalb der Einrichtung.",
             "quelle": "§ 45 SGB VIII, Betriebserlaubnis"},
      schluss="Mit meiner leisen Stimme. Mit meiner Angst.")

# ---------------------------------------------------------------- 12
folge(12, 3,
      a={"raum": "gemeinschaftsraum", "zeilen": ["Ich habe ihn am Telefon gesagt. Unseren Witz.",
                                                 "Mein Bruder hat gefragt, was ich meine.", "Ich habe gesagt, ach, nichts."],
         "figuren": [F(H(3), ["tel_tapfer", "tel_traurig", "traurig"], "hero")]},
      b={"raum": "kinderzimmer_tag", "zeilen": ["Heute habe ich unseren Witz aufgeschrieben.", "Vielleicht lachen wir dann wieder."],
         "figuren": [F(H(3), ["schreibt", "sitz_hoffnungsvoll"], "hero")]},
      epoche="1935",
      damals={"raum": "archiv", "zeilen": ["Der Lebensborn e. V. wurde 1935 als SS-Organisation gegründet.",
                                           "Namen und Angaben zur Geburt konnten verändert werden.",
                                           "Ein neuer Name konnte helfen, ein geraubtes Kind verschwinden zu lassen."],
              "quelle": "Bundesarchiv: Geschichtsgalerie zum Lebensborn e. V.",
              "figuren": [F(D(3), S(["koffer", "still", "traurig"]), "hero")]},
      recht={"titel": "Heimaufsicht muss prüfen können, wie der Alltag wirklich aussieht.", "paragraph": "§ 46 SGB VIII",
             "sub": "Prüfungen vor Ort und nach Aktenlage – auch unangemeldet.", "quelle": "§ 46 SGB VIII, Prüfung vor Ort",
             "figuren": [F("jugendamt", ["aktearm", "freundlich"], "mid-r", follow=False, at=[6]),
                         F(H(3), ["nachdenklich", "hoffnungsvoll"], "hero-l", enter="left", follow=False, at=[5])]},
      schluss="Ich vermisse nicht nur Mama.")

# ---------------------------------------------------------------- 13
folge(13, 4,
      a={"raum": "kinderzimmer_nacht", "zeilen": ["Mama, ich habe deine Stimme leiser in Erinnerung, als ich möchte.",
                                                  "Gute Nacht, mein Schatz.", "Ich versuche, mir genau zu merken, wie du ihn gesagt hast."],
         "figuren": [F(H(4), ["bett", "nachdenklich", "traurig"], "hero")]},
      b={"raum": "gemeinschaftsraum", "zeilen": ["Die Stimme, bei der mein Bauch ruhig wird, kommt aus einem Telefon.",
                                                 "Heute habe ich nach dem Auflegen das Telefon festgehalten."],
         "figuren": [F("mama01", ["tel_laechelnd", "tel_traurig"], "mid-r", ghost=True, fade_in=0.4, fade_out=8.5),
                     F(H(4), ["tel_tapfer", "tel_traurig"], "hero-l")]},
      epoche="1942",
      damals={"raum": "pflegefamilie", "zeilen": ["Alodia wurde zu Alice.",
                                                  "Die Schwestern wurden verschleppt und in deutsche Pflegefamilien gebracht.",
                                                  "Nach dem Krieg fand ihre Mutter Halina sie wieder."],
              "quelle": "bpb: Reiner Engelmann, „Alodia, du bist jetzt Alice!“",
              "figuren": [F("pflegemutter", S(["freundlich", "unsicher", "besorgt"]), "mid-r"),
                          F(D(5), S(["still", "nachdenklich", "traurig"]), "hero-l")]},
      recht={"titel": "Das Kind ist nicht zu jung, nur weil seine Antwort unbequem sein könnte.", "paragraph": "§ 159 FamFG",
             "sub": "Grundsätzlich persönliche Anhörung des Kindes durch das Gericht.", "quelle": "§ 159 FamFG, Anhörung des Kindes"},
      schluss="Meine Hand war noch nicht bereit, dich loszulassen.")

# ---------------------------------------------------------------- 14
folge(14, 5,
      a={"raum": "fenster", "zeilen": ["Manchmal schaue ich aus dem Fenster und stelle mir den Weg zu dir vor.",
                                       "Erst die Straße. Dann wird es in meinem Kopf ungenau.", "Ich weiß nur, wo ich ankommen möchte."],
         "figuren": [F(H(5), ["hinten", "nachdenklich", "aengstlich"], "hero")]},
      b={"raum": "eingang", "zeilen": ["Ich will nicht weglaufen müssen, damit jemand merkt, dass ich hier wegwill.",
                                       "Ich brauche Hilfe, die wirklich zu mir kommt."],
         "figuren": [F(H(5), ["wartet", "traurig"], "hero")]},
      epoche="1943",
      damals={"raum": "pflegefamilie", "zeilen": ["Tamara wurde 1943 verschleppt.",
                                                  "Den Pflegeeltern erzählte man, sie sei ein deutsches Waisenkind.",
                                                  "Die tatsächliche Geschichte wurde ins Gegenteil verkehrt."],
              "quelle": "Universität Münster, Forschung von Isabel Heinemann",
              "figuren": [F("pflegemutter", S(["unsicher", "nachdenklich"]), "mid-r"),
                          F(D(8), S(["still", "traurig", "aengstlich"]), "hero-l")]},
      recht={"titel": "Wer eine Akte nicht kennt, kann sie kaum überprüfen.", "paragraph": "§ 25 SGB X",
             "sub": "Akteneinsicht für Beteiligte – für die Gerichtsakte gilt § 13 FamFG.",
             "quelle": "§ 25 SGB X, § 13 FamFG"},
      schluss="Ich frage schon die ganze Zeit nach einem sicheren Weg nach Hause.")

# ---------------------------------------------------------------- 15
folge(15, 6,
      a={"raum": "kinderzimmer_tag", "zeilen": ["Ich habe die Tage gezählt.", "Jeden Morgen habe ich einen Strich durchgestrichen.",
                                                "Heute habe ich erfahren, dass ich wieder warten muss."],
         "figuren": [F(H(6), ["schreibt", "sitz_nachdenklich", "sitz_traurig"], "hero")]},
      b={"raum": "konferenzraum", "zeilen": ["Die erwachsene Person hat in ihren Kalender geschaut.",
                                             "In meinem waren fast alle Striche schon weg."],
         "figuren": [F("jugendamt", ["kalender", "erklaert"], "mid-r"), F(H(6), ["traurig", "weinend"], "hero-l")]},
      epoche="1942",
      damals={"raum": "amtsstube", "zeilen": ["Auch Jugendämter waren beteiligt.",
                                              "An der Verschleierung von Verschleppungen und an falschen Identitäten.",
                                              "Diese Geschichte lässt sich nicht auf die SS allein abschieben."],
              "quelle": "NS-Dokumentationszentrum Köln: Geraubte Kinder",
              "figuren": [F("beamter", S(["unterschreibt", "stempelt", "ernst"]), "mid-r"),
                          F(D(6), S(["still", "aengstlich", "traurig"]), "hero-l")]},
      recht={"titel": "„Das wurde so entschieden“ ist noch keine Begründung.", "paragraph": "§ 35 SGB X",
             "sub": "Ein Verwaltungsakt braucht eine Begründung mit den wesentlichen Gründen.",
             "quelle": "§ 35 SGB X, Begründung"},
      schluss="Ich zähle jede einzelne Nacht bis dahin.")

# ---------------------------------------------------------------- 16
folge(16, 7,
      a={"raum": "kueche_wohngruppe", "zeilen": ["Heute gab es Plätzchen.", "Eines war am Rand ein bisschen dunkler.",
                                                 "Ich esse es ganz langsam. Es schmeckt fast nach früher."],
         "figuren": [F(H(7), ["nachdenklich", "hoffnungsvoll", "plaetzchen"], "hero")]},
      b={"raum": "kueche_zuhause", "zeilen": ["Da war Mehl auf dem Tisch, und ich habe zu viel Teig genascht.",
                                              "Manchmal ist Heimweh ganz klein. So klein wie ein Krümel."],
         "figuren": [F("mama02", ["hoffnungsvoll", "tisch"], "mid-r", ghost=True, fade_in=0.4),
                     F(H(7), ["froehlich", "traurig"], "hero-l")]},
      epoche="1939–1945",
      damals={"raum": "archiv", "zeilen": ["Wie viele Kinder wurden geraubt?",
                                           "Schätzungen: etwa 20.000 aus Polen, 20.000 aus der Sowjetunion, 10.000 aus West- und Südeuropa.",
                                           "Eine ehrliche Geschichte verschweigt auch die Unsicherheit nicht."],
              "quelle": "Universität Münster, Forschung von Isabel Heinemann",
              "figuren": [F(D(7), S(["still", "nachdenklich"]), "hero")]},
      recht={"titel": "Vor einer Trennung muss weniger eingreifende Hilfe geprüft werden.", "paragraph": "§ 1666a BGB",
             "sub": "Trennung nur, wenn der Gefahr nicht auf andere Weise begegnet werden kann.",
             "quelle": "§ 1666a BGB, Verhältnismäßigkeit"},
      schluss="Mama, heb mir bitte ein schiefes Plätzchen auf.")

# ---------------------------------------------------------------- 17
folge(17, 8,
      a={"raum": "kinderzimmer_tag", "zeilen": ["Ich habe etwas für dich gebastelt.",
                                                "Der Stern ist nicht gleichmäßig geworden. Eine Spitze ist kürzer.",
                                                "Auf die Rückseite habe ich meinen Namen geschrieben."],
         "figuren": [F(H(8), ["malt", "sitz_nachdenklich", "schreibt"], "hero")]},
      b={"raum": "wohnzimmer", "zeilen": ["Ich weiß nur nicht, ob ich sehe, wie du ihn auspackst.",
                                          "Nimm bitte einen Ast, den ich später erreichen kann."],
         "figuren": [F(H(8), ["stern", "hoffnungsvoll"], "hero-l", ghost=True, fade_in=0.3)]},
      epoche="1946",
      damals={"raum": "bahnhof", "zeilen": ["Nach 1945 mussten Familien beweisen, dass sie zusammengehörten.",
                                            "Suchdienste verbanden Namen, frühere Adressen und Spuren.",
                                            "Manche Kinder waren zu jung, um ihre Herkunft zu nennen."],
              "quelle": "Arolsen Archives: Kindersuche nach 1945",
              "figuren": [F("mutter1940", S(["sucht", "foto", "hoffnungsvoll"]), "mid-r"),
                          F(D(1), S(["koffer", "nachdenklich", "hoffnungsvoll"]), "hero-l")]},
      recht={"titel": "Eine Inobhutnahme ist eine Schutzmaßnahme mit Voraussetzungen.", "paragraph": "§ 42 SGB VIII",
             "sub": "Widersprechen die Eltern, muss das Kind übergeben oder das Familiengericht angerufen werden.",
             "quelle": "§ 42 SGB VIII, Inobhutnahme"},
      schluss="Ich möchte ihn selbst noch einmal geraderücken. Neben dir.")

# ---------------------------------------------------------------- 18
folge(18, 9,
      a={"raum": "kueche_zuhause", "zeilen": ["Du hast erzählt, dass ihr etwas umgestellt habt.", "Nur eine Kleinigkeit.",
                                              "Ich habe Angst, dass ich in meinem Zuhause immer kleiner werde."],
         "figuren": [F(H(9), ["nachdenklich", "traurig", "aengstlich"], "hero", shrink=10.5)]},
      b={"raum": "kinderzimmer_nacht", "zeilen": ["Dass meine Tasse noch da ist. Dass mein Kissen wartet.",
                                                  "Dass ich immer noch zu diesem Wir gehöre."],
         "figuren": [F(H(9), ["bett", "hoffnungsvoll"], "hero")]},
      epoche="1945",
      wandel={"ziel": ("k09_damals", "traurig~faded"), "jahre": ["2026", "1990", "1970"]},
      damals={"raum": "heim1960", "zeilen": ["1945 endete die NS-Herrschaft.", "Autoritäre Heimerziehung endete damit nicht automatisch.",
                                             "Der Alltag blieb streng, die Beteiligung der Kinder gering."],
              "quelle": "Hamburg, Landesbetrieb Erziehung und Beratung",
              "figuren": [F("k05_heim60", FA(["schrubbt"]), "back-l"), F("k01_heim60", FA(["gerade"]), "back-r"),
                          F("k08_heim60", FA(["kopfgesenkt", "traurig", "weinend"]), "hero")]},
      recht={"titel": "„Zu deinem Schutz“ ist noch keine Erlaubnis, ein Kind einzusperren.", "paragraph": "§ 1631b BGB",
             "sub": "Freiheitsentziehende Unterbringung braucht grundsätzlich die Genehmigung des Familiengerichts.",
             "quelle": "§ 1631b BGB, § 42 SGB VIII"},
      schluss="Auch wenn ich gerade nicht durch unsere Küche laufe.")

# ---------------------------------------------------------------- 19
folge(19, 1,
      a={"raum": "konferenzraum", "zeilen": ["Heute habe ich das Wort Perspektive gehört.",
                                             "Dann nicken Menschen und machen sich Notizen.", "Ich denke dabei an mein Bett heute Abend."],
         "figuren": [F("jugendamt", ["erklaert", "schreibt"], "back-l"), F("betreuerin", ["hoertzu", "nachdenklich"], "back-r"),
                     F(H(1), ["sitz_nachdenklich", "sitz_traurig", "sitz_nachdenklich"], "hero")]},
      b={"raum": "kinderzimmer_nacht", "zeilen": ["Mein Leben beginnt nicht erst, wenn euer Plan fertig ist.",
                                                  "Meine Schuhe werden zu klein."],
         "figuren": [F(H(1), ["bett", "nachdenklich"], "hero")]},
      epoche="1961",
      wandel={"ziel": ("k01_heim60", "traurig~faded"), "jahre": ["2026", "1990", "1970"]},
      damals={"raum": "heim1960", "zeilen": ["„Freiwillig“ konnte auf dem Papier stehen.",
                                             "1961 wurde die Freiwillige Erziehungshilfe bundesweit verankert.",
                                             "Wie frei war die Entscheidung tatsächlich?"],
              "quelle": "LWL: Forschungsbericht zur Heimerziehung in Westfalen",
              "figuren": [F("k08_heim60", FA(["gerade"]), "back-r"),
                          F("k01_heim60", FA(["gerade", "kopfgesenkt", "traurig"]), "hero")]},
      recht={"raum": "konferenzsaal", "titel": "Die UN-Kritik an Deutschland ist konkret.", "paragraph": "CRC/C/DEU/CO/5-6",
             "sub": "Kindgerechte Beschwerdewege und die Sicht der Kinder in Verfahren.",
             "quelle": "UN-Kinderrechtsausschuss, 13.10.2022, Rn. 11, 17, 26–27"},
      schluss="Ich bin auch das Kind, das heute noch wach liegt.")

# ---------------------------------------------------------------- 20
folge(20, 2,
      a={"raum": "gemeinschaftsraum", "zeilen": ["Manchmal höre ich an deinem ersten Hallo, dass du nicht weinen wolltest.",
                                                 "Dann ändere ich meine Geschichte.", "Ich sage, dass der Tag okay war."],
         "figuren": [F(H(2), ["tel_traurig", "tel_tapfer", "tel_tapfer"], "hero")]},
      b={"raum": "kueche_zuhause", "zeilen": ["Ich glaube, du machst manchmal dasselbe für mich.",
                                              "Ich möchte dir erzählen, was wehgetan hat."],
         "figuren": [F("mama01", ["tel_laechelnd", "tel_traurig", "weinend"], "hero")]},
      epoche="1949–1975",
      wandel={"ziel": ("k02_damals", "traurig~faded"), "jahre": ["2026", "1990"]},
      damals={"raum": "heim1960", "zeilen": ["Wer kontrollierte die Heime?",
                                             "Eine geregelte Heimaufsicht entstand erst durch das Gesetz von 1961.",
                                             "Kinder lebten in Heimen, deren Alltag ihre Vertreter kaum kannten."],
              "quelle": "Runder Tisch Heimerziehung, Abschlussbericht 2010",
              "figuren": [F("k01_heim60", FA(["gerade"]), "back-l"),
                          F("k05_heim60", FA(["schrubbt", "weinend", "aengstlich"]), "hero")]},
      recht={"titel": "Kutzner gegen Deutschland: War die Trennung wirklich erforderlich?", "paragraph": "Art. 8 EMRK",
             "sub": "EGMR 2002: Die Gründe rechtfertigten den schweren Eingriff nicht ausreichend.",
             "quelle": "EGMR, Kutzner gegen Deutschland, 26.02.2002, Nr. 46544/99"},
      schluss="Ich möchte nur meinen Satz zu Ende erzählen können.")

# ---------------------------------------------------------------- 21
folge(21, 3,
      a={"raum": "schulhof", "zeilen": ["Ich möchte nicht, dass fremde Menschen mein Gesicht kennen.",
                                        "Jemand aus meiner Klasse sieht im Internet ein Bild von mir.",
                                        "Ich wüsste nicht, wohin ich schauen soll."],
         "figuren": [F(H(7), ["ueberrascht"], "back-l"), F(H(3), ["hinten", "aengstlich", "traurig"], "hero")]},
      b={"raum": "kinderzimmer_tag", "zeilen": ["Ihr könnt für mich laut werden. Sehr laut sogar.",
                                                "Aber lasst mir eine Tür, die ich selbst schließen darf."],
         "figuren": [F(H(3), ["sitz_nachdenklich", "sitz_hoffnungsvoll"], "hero")]},
      epoche="DDR",
      wandel={"ziel": ("jwh_junge", "aengstlich~faded"), "jahre": ["2026", "1989"]},
      damals={"raum": "jugendwerkhof", "zeilen": ["Torgau: Geschlossener Jugendwerkhof, 1964 bis 1989.",
                                                  "Mehr als 4.000 Jugendliche zwischen 14 und 18 Jahren.",
                                                  "Eingewiesen ohne gerichtliches Verfahren."],
              "quelle": "Elisabeth Hingerl / bpb: Der Geschlossene Jugendwerkhof Torgau",
              "figuren": [F("jwh_maedchen", FA(["still", "marschiert"]), "back-r"),
                          F("jwh_junge", FA(["still", "aengstlich", "trotzig"]), "hero-l")]},
      recht={"titel": "Zeit kann Familienbindungen verändern, bevor ein Fehler korrigiert wird.", "paragraph": "Art. 8 EMRK",
             "sub": "Haase gegen Deutschland, EGMR 2004: Zeitablauf hat Folgen für Familien.",
             "quelle": "EGMR, Haase gegen Deutschland, 08.04.2004, Nr. 11057/02"},
      schluss="Trotzdem wäre es mein Gesicht. Mein Name.")

# ---------------------------------------------------------------- 22
folge(22, 4,
      a={"raum": "fenster", "zeilen": ["Noch zwei Nächte.", "Ich traue mich nicht mehr zu fragen, ob ich komme.",
                                       "Also frage ich etwas anderes. Ob es morgen schneien soll."],
         "figuren": [F(H(4), ["hinten", "nachdenklich", "hoffnungsvoll"], "hero")]},
      b={"raum": "eingang", "zeilen": ["In meinem Kopf habe ich meine Sachen längst gepackt.",
                                       "Den Stern. Den Brief. Die Sachen, die ich dir zeigen möchte."],
         "figuren": [F(H(4), ["wartet", "hoffnungsvoll"], "hero")]},
      epoche="2006",
      wandel={"ziel": ("alt_mann", "nachdenklich"), "jahre": ["2026", "2016"]},
      damals={"raum": "anhoerung", "zeilen": ["Sie waren längst erwachsen, als sie öffentlich kämpfen mussten.",
                                              "2006 Petition ehemaliger Heimkinder, 2009 bis 2010 Runder Tisch.",
                                              "Ihr Kinderleid sollte endlich anerkannt werden."],
              "quelle": "Unabhängige Aufarbeitungskommission: Runder Tisch Heimerziehung",
              "figuren": [F("alt_frau", ["kinderfoto", "weinend"], "mid-r"),
                          F("alt_mann", ["mikrofon", "nachdenklich", "hoffnungsvoll"], "hero-l")]},
      recht={"titel": "Eine Ergänzungspflegschaft ist keine unbegrenzte Entscheidungsgewalt.", "paragraph": "§ 1809 BGB",
             "sub": "Der Pfleger besorgt nur die übertragenen Aufgaben – zum Wohl des Kindes.",
             "quelle": "§ 1809, § 1813, § 1790 BGB"},
      schluss="Hinter meiner Frage nach dem Wetter steckt eine ganz andere.")

# ---------------------------------------------------------------- 23
folge(23, 5,
      a={"raum": "kinderzimmer_nacht", "zeilen": ["Morgen ist Weihnachten.", "Ich habe deinen Brief unter mein Kissen gelegt.",
                                                  "Ich fahre mit dem Finger unter den Zeilen entlang."],
         "figuren": [F(H(5), ["hoffnungsvoll", "brief", "brief"], "hero")]},
      b={"raum": "kinderzimmer_nacht", "cam": (-1300, -900, 1.1, 1.18, "power1.inOut"),
         "zeilen": ["An einer Stelle ist die Schrift anders.", "Es ist nicht deine Hand."],
         "figuren": [F(H(5), ["bett", "bett"], "hero")]},
      epoche="1990/91",
      wandel={"ziel": ("k05_damals", "nachdenklich~sepia"), "jahre": ["2026", "2010"]},
      damals={"raum": "archiv", "zeilen": ["1990/91 wurde das Recht neu ausgerichtet.",
                                           "Das SGB VIII löste das alte Jugendwohlfahrtsrecht ab.",
                                           "Aber ein neues Gesetz verändert keinen Alltag von allein."],
              "quelle": "bpb: Jugendhilfe und Polizei – historische Entwicklung",
              "figuren": [F("jugendamt", ["aktearm", "ernst"], "mid-r")]},
      recht={"titel": "Ein falscher Satz wird nicht wahr, weil er in der nächsten Akte steht.", "paragraph": "§ 84 SGB X",
             "sub": "Bei bestrittenen Daten muss die ungeklärte Sachlage festgehalten werden.",
             "quelle": "§ 84 SGB X, bestrittene Sozialdaten"},
      schluss="Aber es ist etwas, das du für mich festgehalten hast.")

# ---------------------------------------------------------------- 24
folge(24, 6,
      a={"raum": "kinderzimmer_nacht", "zeilen": ["Mama, heute fehlt mir kein Geschenk.", "Heute fehlst du.",
                                                  "Einen Moment wusste ich nicht mehr, wo ich bin."],
         "figuren": [F(H(6), ["bett", "traurig", "nachdenklich"], "hero")]},
      b={"raum": "wohnzimmer", "zeilen": ["Vielleicht steht bei dir schon mein Teller.",
                                          "Mama, wenn wir heute telefonieren, bleib einen Augenblick länger dran."],
         "figuren": [F("mama02", ["traurig", "tel_laechelnd"], "mid-r"),
                     F(H(6), ["hoffnungsvoll", "tel_tapfer"], "hero-l", ghost=True, fade_in=0.5)]},
      epoche="2022",
      wandel={"ziel": ("k06_heute", "nachdenklich"), "jahre": ["2026", "2024"]},
      damals={"raum": "konferenzsaal", "zeilen": ["2022 erinnerte der UN-Kinderrechtsausschuss Deutschland an die Beteiligung von Kindern.",
                                                  "Kindermeinungen werden vor Gerichten nicht immer berücksichtigt.",
                                                  "Die Geschichte endet nicht mit einer Reform."],
              "quelle": "UN-Kinderrechtsausschuss: CRC/C/DEU/CO/5-6, 13.10.2022",
              "figuren": [F(H(6), ["nachdenklich", "hoffnungsvoll"], "hero")]},
      recht={"titel": "Nach dem letzten Türchen darf das Recht des Kindes nicht wieder zugehen.", "paragraph": "§ 36 · § 9a · § 46",
             "sub": "Jede konkrete Sorge braucht eine Adresse und eine überprüfbare Antwort.",
             "quelle": "§ 36, § 9a, § 46 SGB VIII"},
      schluss="Ich möchte nur hören, dass du noch da bist.",
      ende_posen=["hoffnungsvoll", "tel_tapfer"])
