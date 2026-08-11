#!/usr/bin/env python3
"""grafik_szenen.py — Titel-, Akten- und Schlusskarten bauen.

Kostet keine Credits und bringt die Pointen ins Bild, die im Song nur gesagt
werden. Das Papier ist kein gemaltes Beige, sondern ein echter Ausschnitt aus
dem Poster — dadurch sitzen die Karten in derselben Bildwelt wie die Clips.

    python3 grafik_szenen.py
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HIER = Path(__file__).parent
POSTER = HIER / "material" / "poster.jpg"
ZIEL = HIER / "bauplatz" / "grafik"
SCHRIFT_DATEI = HIER / "bauplatz" / "schrift" / "ArchivoBlack.ttf"

CREME = (251, 237, 215)
PINK = (217, 93, 114)
TINTE = (38, 30, 24)
ROT = (168, 38, 38)

FORMATE = {"16-9": (1920, 1080), "9-16": (1080, 1920)}

# Der Farbton des Papiers im Poster, aus dem Bild gemessen (hellste Cremefläche).
PAPIER_TON = (243, 228, 202)


def schrift(groesse):
    return ImageFont.truetype(str(SCHRIFT_DATEI), groesse)


def papier(breite, hoehe):
    """Alterspapier, selbst gebaut.

    Ein Ausschnitt aus dem Poster wäre naheliegend, taugt aber nicht: überall im
    Bild liegt Schrift, und verwaschene Originalschrift im Hintergrund sieht nach
    Fehler aus. Also Grundton, feines Korn, ein paar weiche Flecken, Vignette.
    """
    grund = Image.new("RGB", (breite, hoehe), PAPIER_TON)

    # Feines Korn — ohne das wirkt die Fläche wie Pappe.
    korn = Image.effect_noise((breite, hoehe), 16).convert("L")
    grund = Image.composite(
        ImageEnhance.Brightness(grund).enhance(1.04),
        ImageEnhance.Brightness(grund).enhance(0.96),
        korn)

    # Ein paar Altersflecken, groß und weich.
    flecken = Image.new("L", (breite, hoehe), 0)
    stift = ImageDraw.Draw(flecken)
    einheit = min(breite, hoehe)
    for x, y, r in ((0.18, 0.22, 0.30), (0.82, 0.30, 0.24), (0.55, 0.86, 0.34),
                    (0.08, 0.74, 0.22), (0.70, 0.62, 0.18)):
        stift.ellipse((breite * x - einheit * r, hoehe * y - einheit * r,
                       breite * x + einheit * r, hoehe * y + einheit * r), fill=70)
    flecken = flecken.filter(ImageFilter.GaussianBlur(einheit // 6))
    getoent = ImageEnhance.Color(ImageEnhance.Brightness(grund).enhance(0.90)).enhance(1.15)
    grund = Image.composite(getoent, grund, flecken)

    # Vignette: außen abdunkeln, damit die Karte Tiefe bekommt.
    maske = Image.new("L", (breite, hoehe), 0)
    ImageDraw.Draw(maske).ellipse(
        (-breite * 0.20, -hoehe * 0.30, breite * 1.20, hoehe * 1.30), fill=255)
    maske = maske.filter(ImageFilter.GaussianBlur(einheit // 7))
    return Image.composite(grund, ImageEnhance.Brightness(grund).enhance(0.62), maske)


def zentriert(stift, text, y, groesse, farbe, breite, sperrung=0, max_breite=None):
    """Zeile mittig setzen, gibt die Unterkante zurück.

    `max_breite` verkleinert die Schrift so weit, bis die Zeile hineinpasst — im
    Hochformat sind die Kästen schmal, und abgeschnittene Wörter sehen kaputt aus.
    """
    grenze = max_breite or breite
    while groesse > 10:
        f = schrift(groesse)
        laenge = stift.textlength(text, font=f)
        if sperrung:
            laenge += sperrung * (len(text) - 1)
        if laenge <= grenze:
            break
        groesse = int(groesse * 0.94)
        sperrung *= 0.94
    f = schrift(groesse)
    if sperrung:
        gesamt = sum(stift.textlength(z, font=f) + sperrung for z in text) - sperrung
        x = (breite - gesamt) / 2
        for zeichen in text:
            stift.text((x, y), zeichen, font=f, fill=farbe)
            x += stift.textlength(zeichen, font=f) + sperrung
    else:
        laenge = stift.textlength(text, font=f)
        stift.text(((breite - laenge) / 2, y), text, font=f, fill=farbe)
    return y + groesse * 1.15


def stempel(bild, text, mitte, groesse, winkel=-7):
    """Roter Stempelabdruck mit Rahmen, leicht schief und angerauht."""
    f = schrift(groesse)
    hilfs = Image.new("RGBA", (int(len(text) * groesse * 0.85) + 80, int(groesse * 2.4)),
                      (0, 0, 0, 0))
    stift = ImageDraw.Draw(hilfs)
    laenge = stift.textlength(text, font=f)
    x = (hilfs.width - laenge) / 2
    stift.text((x, groesse * 0.55), text, font=f, fill=ROT + (235,))
    stift.rectangle([8, 8, hilfs.width - 8, hilfs.height - 8],
                    outline=ROT + (235,), width=max(groesse // 12, 4))

    # Abgenutzt aussehen lassen: Rauschen in den Alphakanal.
    rauschen = Image.effect_noise(hilfs.size, 42).point(lambda w: 255 if w > 96 else 150)
    alpha = hilfs.getchannel("A").point(lambda a: a)
    hilfs.putalpha(Image.composite(alpha, alpha.point(lambda a: int(a * 0.45)), rauschen))

    gedreht = hilfs.rotate(winkel, expand=True, resample=Image.BICUBIC)
    bild.paste(gedreht, (int(mitte[0] - gedreht.width / 2),
                         int(mitte[1] - gedreht.height / 2)), gedreht)


def aktenkarte(breite, hoehe, kopf, befund):
    """MUTTER — ZU EMOTIONAL: die Karten aus dem Pre-Chorus."""
    bild = papier(breite, hoehe)
    stift = ImageDraw.Draw(bild)
    gross = int(min(breite, hoehe) * 0.115)

    # Karteikarte
    rand = int(breite * 0.10)
    oben = int(hoehe * 0.30)
    unten = int(hoehe * 0.70)
    stift.rectangle([rand, oben, breite - rand, unten], fill=(246, 232, 206),
                    outline=(120, 96, 70), width=6)
    stift.line([rand, oben + int(hoehe * 0.19), breite - rand, oben + int(hoehe * 0.19)],
               fill=(150, 125, 95), width=3)

    innen = (breite - 2 * rand) * 0.88
    y = oben + int(hoehe * 0.045)
    y = zentriert(stift, kopf.upper(), y, gross, TINTE, breite,
                  sperrung=gross * 0.08, max_breite=innen)
    zentriert(stift, befund.upper(), oben + int(hoehe * 0.245), int(gross * 0.78),
              ROT, breite, sperrung=gross * 0.05, max_breite=innen)
    return bild


def titelkarte(breite, hoehe):
    bild = papier(breite, hoehe)
    stift = ImageDraw.Draw(bild)
    einheit = min(breite, hoehe)

    # Der Stempel liegt zuerst und unten — der Satz darüber bleibt frei.
    stempel(bild, "GUTACHTEN", (breite * 0.5, hoehe * 0.88), int(einheit * 0.05))

    y = hoehe * 0.16 if breite > hoehe else hoehe * 0.26
    y = zentriert(stift, "DER", y, int(einheit * 0.09), TINTE, breite, einheit * 0.012)
    y = zentriert(stift, "GUTACHTEN-", y, int(einheit * 0.125), TINTE, breite,
                  max_breite=breite * 0.88)
    y = zentriert(stift, "TROLL", y, int(einheit * 0.125), TINTE, breite)
    satz = breite * 0.84
    y = zentriert(stift, "ER HAT FÜR ALLES EINE ANTWORT –", y + einheit * 0.035,
                  int(einheit * 0.040), TINTE, breite, max_breite=satz)
    zentriert(stift, "BEVOR ÜBERHAUPT GEFRAGT WIRD!", y + einheit * 0.008,
              int(einheit * 0.040), PINK, breite, max_breite=satz)
    return bild


def schlusskarte(breite, hoehe):
    bild = papier(breite, hoehe)
    stift = ImageDraw.Draw(bild)
    einheit = min(breite, hoehe)

    stempel(bild, "ERGEBNIS: UNKLAR", (breite * 0.5, hoehe * 0.86),
            int(einheit * 0.046), winkel=5)

    satz = breite * 0.86
    y = hoehe * 0.20 if breite > hoehe else hoehe * 0.28
    y = zentriert(stift, "PAPIER KANN VIEL –", y, int(einheit * 0.078), TINTE, breite,
                  max_breite=satz)
    y = zentriert(stift, "ABER NICHT", y + einheit * 0.015, int(einheit * 0.078), TINTE,
                  breite, max_breite=satz)
    y = zentriert(stift, "DIE WAHRHEIT!", y, int(einheit * 0.078), PINK, breite,
                  max_breite=satz)
    zentriert(stift, "TEILEN STATT SCHWEIGEN", y + einheit * 0.055,
              int(einheit * 0.042), TINTE, breite, einheit * 0.006, max_breite=satz)
    return bild


KARTEN = {
    "titel": titelkarte,
    "schluss": schlusskarte,
    "akte-mutter": lambda b, h: aktenkarte(b, h, "Mutter", "zu emotional"),
    "akte-vater": lambda b, h: aktenkarte(b, h, "Vater", "zu fordernd"),
    "akte-kind": lambda b, h: aktenkarte(b, h, "Kind", "zu beeinflusst"),
    "akte-wahrheit": lambda b, h: aktenkarte(b, h, "Wahrheit", "passt nicht rein"),
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--format", choices=sorted(FORMATE) + ["alle"], default="alle")
    args = p.parse_args()

    formate = sorted(FORMATE) if args.format == "alle" else [args.format]
    ZIEL.mkdir(parents=True, exist_ok=True)

    for format_name in formate:
        breite, hoehe = FORMATE[format_name]
        for name, bauen in KARTEN.items():
            datei = ZIEL / f"{name}_{format_name}.png"
            bauen(breite, hoehe).save(datei)
            print(datei.relative_to(HIER))


if __name__ == "__main__":
    main()
