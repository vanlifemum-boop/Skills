# Bildsprache der Reihe

Die Datei `serienstil.txt` daneben ist die maschinenlesbare Fassung. Sie wird jedem
Szenen-Prompt vorangestellt, damit alle Folgen zusammenpassen. Wer sie ändert, ändert
den Look der ganzen Reihe – deshalb steht sie an genau einer Stelle.

## Die Regeln und warum sie so lauten

| Regel | Grund |
|---|---|
| keine identifizierbaren Personen, keine Gesichter groß im Bild | Persönlichkeitsrecht; und die Reihe erklärt ein Verfahren, sie zeigt keine Familie |
| keine echten Behörden, Uniformen, Wappen, Logos | eine erfundene Behörde im Bild kann niemand als seine wiedererkennen |
| kein lesbarer Text im Bild | KI-Modelle erfinden Schrift; eine erfundene Aktennotiz sähe aus wie ein Beleg |
| keine weinenden Kinder, kein Festhalten, kein Polizeieinsatz | die Reihe soll erklären, nicht Angst erzeugen – und nicht bebildern, was rechtlich gerade als Ausnahme beschrieben wird |
| ruhige Kamera | der Ton der Reihe ist sachlich; hektische Bilder widersprechen dem Sprechertext |
| gedämpfte, natürliche Farben | hebt die Einblendungen hervor, statt mit ihnen zu konkurrieren |

## Einblendungen

Rechtliche Begriffe und Paragrafen laufen als Bauchbinde, nicht als gesprochener Text im
Bild. Die Einblendungen stehen je Kapitel im Folgen-JSON unter `einblendungen` — in der
Reihenfolge, in der sie erscheinen sollen.

## Wiederkehrende Moderationsfigur

Vorerst nicht. Eine erfundene Figur, die durch die Reihe führt, müsste über alle Folgen
hinweg gleich aussehen; bei generierten Videos ist das aufwendig und teuer. Bis dahin
tragen Sprecherstimme und Einblendungen die Reihe.
