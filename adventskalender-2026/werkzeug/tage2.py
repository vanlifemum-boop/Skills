"""Tagesdaten für Stil 2 (Bilderbuch-Film). Zeilen: (Text, Start, Ende, Einblendung) in Sekunden der Szene.
Texte wörtlich bzw. gekürzt aus dem Adventskalender 2026 (Systemfehler Familie)."""
TAGE = {
    1: {
        "tag": 1,
        "kind_nr": 1,
        "flur_kinder": [3, 5, 8],
        "geschwister": [7, 4],
        "damals_kinder": [(2, 1), (4, 1), (6, 1), (3, 2), (5, 2), (7, 2), (8, 3), (9, 3)],
        "flur_zeilen": [
            ("Mama, heb meinen Platz auf.", 0.0, 3.4, "none"),
            ("Hier steht auch ein Weihnachtsbaum.", 3.8, 7.6, "blur"),
            ("Ein Weihnachtsbaum kann ja nichts dafür, dass er im falschen Zimmer steht.", 8.0, 15.6, "grey"),
        ],
        "zuhause_zeilen": [
            ("Ich weiß noch, wie mein Stuhl an unserem Tisch klingt.", 0.4, 5.6, "blur"),
            ("Manchmal habe ich Angst, dass ihr euch daran gewöhnt, dass mein Platz leer bleibt.", 6.0, 11.6, "grey"),
        ],
        "epoche": "KAISERREICH",
        "damals_zeilen": [
            ("Bevor es Jugendämter gab, wurden Kinder bereits in Anstalten erzogen.", 0.8, 6.4, "type"),
            ("Religiöse Unterweisung, Arbeit, Ordnung, Gehorsam.", 6.8, 11.2, "stamp"),
            ("Wie muss ein Kind werden, damit es den Erwartungen der Erwachsenen entspricht?", 11.6, 18.6, "type"),
        ],
        "damals_quelle": "Diakonie Deutschland – Erziehungshilfe im historischen Verlauf",
        "recht_titel": "Ein Kind muss kein perfekter Gesprächspartner sein, um beteiligt zu werden.",
        "paragraph": "§ 8 SGB VIII",
        "recht_sub": "Beteiligung an Entscheidungen, die das Kind betreffen. Es darf sich auch selbst an das Jugendamt wenden.",
        "recht_quelle": "§ 8 SGB VIII, Beteiligung von Kindern",
        "kind_schluss": "Ich weiß noch genau, wohin ich gehöre.",
    },
}
