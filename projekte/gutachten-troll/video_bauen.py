#!/usr/bin/env python3
"""video_bauen.py — aus Schnittliste, Clips, Grafiken und Text das Video bauen.

Drei Stufen, absichtlich getrennt statt ein großer Filtergraph: ein Fehler in
Minute fünf soll nicht die ersten vier Minuten Rechenzeit wegwerfen.

  1. Boomerang  Jeder 8-Sekunden-Clip wird vorwärts + rückwärts zu 16 Sekunden.
                Das verdoppelt die Laufzeit, ohne dass eine Schleife sichtbar
                springt — und ohne Zeitlupe, die zäh aussähe.
  2. Teile      Jeder Eintrag der Schnittliste wird ein eigener stummer Schnipsel
                in Zielauflösung: Clipausschnitt, Kamerafahrt über das Poster
                (zoompan) oder Karteikarte.
  3. Zusammen   Aneinanderhängen, Songtext über libass einbrennen, Ton dazu.

    python3 video_bauen.py --format 16-9
    python3 video_bauen.py --format 16-9 --nur-teile 3,4     # nur prüfen
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).parent
BAU = HIER / "bauplatz"
FORMATE = {"16-9": (1920, 1080), "9-16": (1080, 1920)}
FPS = 25

# Das Poster hat 1254 px. Für Kamerafahrten wird es einmal hochgerechnet, damit
# zoompan nicht auf dem Originalraster herumrutscht.
POSTER_FAKTOR = 2.4


def ffmpeg():
    pfad = subprocess.run([str(HIER / ".." / ".." / "scripts" / "ensure-ffmpeg.sh")],
                          capture_output=True, text=True, check=True).stdout.strip()
    return pfad.splitlines()[-1]


FF = None


def lauf(argumente, still=True):
    befehl = [FF, "-y", "-v", "error" if still else "warning"] + argumente
    ergebnis = subprocess.run(befehl, capture_output=True, text=True)
    if ergebnis.returncode != 0:
        raise SystemExit(f"ffmpeg gescheitert:\n  {' '.join(befehl[:14])} …\n{ergebnis.stderr[-1500:]}")


def kodierung(schnell=True):
    return ["-c:v", "libx264", "-preset", "veryfast" if schnell else "medium",
            "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]


# ---------------------------------------------------------------------------
# Stufe 1 — Boomerang
# ---------------------------------------------------------------------------

def clip_filter(format_name, breite, hoehe):
    """Bringt einen 16:9-Clip ins Zielformat."""
    if breite > hoehe:
        return (f"scale={breite}:{hoehe}:flags=lanczos,"
                f"unsharp=5:5:0.4,setsar=1")
    # Hochformat: der Clip bleibt als 16:9-Fenster stehen, dahinter eine
    # weichgezeichnete, abgedunkelte Kopie — Beschneiden würde den Troll köpfen.
    fenster_hoehe = round(breite * 9 / 16 / 2) * 2
    oben = int(hoehe * 0.27)
    return (f"split=2[gr][vg];"
            f"[gr]scale={breite}:{hoehe}:force_original_aspect_ratio=increase,"
            f"crop={breite}:{hoehe},gblur=sigma=40,eq=brightness=-0.30:saturation=0.6[hg];"
            f"[vg]scale={breite}:{fenster_hoehe}:flags=lanczos,unsharp=5:5:0.4[vd];"
            f"[hg][vd]overlay=0:{oben},setsar=1")


def boomerang_bauen(name, format_name, breite, hoehe):
    quelle = BAU / "clips" / f"{name}.mp4"
    ziel = BAU / "boomerang" / f"{name}_{format_name}.mp4"
    if ziel.exists():
        return ziel
    if not quelle.exists():
        return None
    ziel.parent.mkdir(parents=True, exist_ok=True)

    filter_kette = clip_filter(format_name, breite, hoehe)
    lauf(["-i", str(quelle), "-filter_complex",
          f"[0:v]{filter_kette}[v];[v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[out]",
          "-map", "[out]"] + kodierung() + [str(ziel)])
    return ziel


# ---------------------------------------------------------------------------
# Stufe 2 — die einzelnen Teile
# ---------------------------------------------------------------------------

def ausschnitt_bild(schluessel, feld, format_name, breite, hoehe):
    """Schneidet den Posterausschnitt auf das Zielseitenverhältnis zu."""
    from PIL import Image

    ziel = BAU / "ausschnitte" / f"{schluessel}_{format_name}.png"
    if ziel.exists():
        return ziel
    ziel.parent.mkdir(parents=True, exist_ok=True)

    poster = Image.open(HIER / "material" / "poster.jpg").convert("RGB")
    gross = poster.resize((int(poster.width * POSTER_FAKTOR),
                           int(poster.height * POSTER_FAKTOR)), Image.LANCZOS)
    w, h = gross.size

    # Das Poster trägt oben seinen Titel und unten den Claim. Beides gehört nicht
    # in eine Kamerafahrt — sonst steht angeschnittene Plakatschrift im Bild,
    # während unten schon der Songtext läuft. Also nur der Bereich dazwischen.
    band_oben, band_unten = 0.205 * h, 0.885 * h

    x, y, bw, bh = feld
    mx, my = (x + bw / 2) * w, (y + bh / 2) * h
    kw, kh = bw * w, bh * h

    # Auf das Zielverhältnis aufweiten, nie beschneiden — sonst fehlt das Motiv.
    verhaeltnis = breite / hoehe
    if kw / kh < verhaeltnis:
        kw = kh * verhaeltnis
    else:
        kh = kw / verhaeltnis

    # In Bild und Band zurückschieben, statt schwarze Ränder zu erzeugen.
    kh = min(kh, band_unten - band_oben)
    kw = min(kh * verhaeltnis, w)
    kh = kw / verhaeltnis
    links = min(max(mx - kw / 2, 0), w - kw)
    oben = min(max(my - kh / 2, band_oben), band_unten - kh)

    bild = gross.crop((int(links), int(oben), int(links + kw), int(oben + kh)))
    # Reichlich Reserve für die Fahrt: zoompan zoomt in das Bild hinein.
    bild = bild.resize((int(breite * 1.6), int(hoehe * 1.6)), Image.LANCZOS)
    bild.save(ziel)
    return ziel


def fahrt_filter(bilder, nummer, breite, hoehe, typ):
    """zoompan-Kette: abwechselnd hinein und hinaus.

    Karteikarten bekommen nur eine Andeutung von Bewegung — bei starkem Zoom
    wandern Satzkanten aus dem Bild. Posterausschnitte dürfen deutlicher fahren
    und bekommen etwas Korn, das die Hochrechnung des 1254-px-Posters kaschiert.
    """
    if typ == "grafik":
        z = ("min(zoom+0.00012,1.05)" if nummer % 2 == 0
             else "if(eq(on,0),1.05,max(zoom-0.00012,1.0))")
        nachbehandlung = ""
    else:
        z = ("min(zoom+0.00050,1.25)" if nummer % 2 == 0
             else "if(eq(on,0),1.25,max(zoom-0.00050,1.0))")
        nachbehandlung = ",noise=alls=2:allf=t"
    return (f"zoompan=z='{z}':d={bilder}:x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':s={breite}x{hoehe}:fps={FPS}"
            f"{nachbehandlung},setsar=1")


def teil_bauen(teil, nummer, format_name, breite, hoehe, ausschnitte):
    ziel = BAU / "teile" / format_name / f"{nummer:03d}.mp4"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    if ziel.exists():
        return ziel

    dauer = teil["bis"] - teil["von"]
    bilder = max(int(round(dauer * FPS)), 1)

    if teil["typ"] == "clip":
        quelle = BAU / "boomerang" / f"{teil['quelle']}_{format_name}.mp4"
        if not quelle.exists():
            raise SystemExit(f"Boomerang fehlt: {quelle.name}")
        lauf(["-stream_loop", "-1", "-i", str(quelle), "-frames:v", str(bilder),
              "-vf", f"fps={FPS},setsar=1"] + kodierung() + [str(ziel)])
        return ziel

    if teil["typ"] == "poster":
        bild = ausschnitt_bild(teil["quelle"], ausschnitte[teil["quelle"]],
                               format_name, breite, hoehe)
    else:
        bild = BAU / "grafik" / f"{teil['quelle']}_{format_name}.png"
        if not bild.exists():
            raise SystemExit(f"Grafik fehlt: {bild}")

    lauf(["-i", str(bild), "-vf", fahrt_filter(bilder, nummer, breite, hoehe, teil["typ"]),
          "-frames:v", str(bilder)] + kodierung() + [str(ziel)])
    return ziel


# ---------------------------------------------------------------------------
# Stufe 3 — zusammensetzen
# ---------------------------------------------------------------------------

def zusammensetzen(teile, format_name, ziel, dauer, crf, hoechstrate):
    liste = BAU / "teile" / format_name / "liste.txt"
    liste.write_text("".join(f"file '{p.resolve()}'\n" for p in teile), encoding="utf-8")

    ass = BAU / f"text_{format_name}.ass"
    schriften = BAU / "schrift"
    audio = HIER / "material" / "song.mp3"

    # Ein Ausblenden am Schluss, damit der Song nicht abgeschnitten wirkt.
    blende = f"fade=t=in:st=0:d=1.2,fade=t=out:st={dauer - 2.4:.2f}:d=2.4"

    lauf(["-f", "concat", "-safe", "0", "-i", str(liste),
          "-i", str(audio),
          "-vf", f"ass='{ass}':fontsdir='{schriften}',{blende}",
          "-map", "0:v", "-map", "1:a",
          "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
          "-maxrate", f"{hoechstrate}k", "-bufsize", f"{hoechstrate * 2}k",
          "-pix_fmt", "yuv420p", "-r", str(FPS),
          "-c:a", "aac", "-b:a", "192k",
          "-t", f"{dauer:.3f}", "-movflags", "+faststart", str(ziel)], still=False)


def main():
    global FF
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--format", choices=sorted(FORMATE), default="16-9")
    p.add_argument("--nur-teile", help="nur diese Teilenummern bauen, z. B. 0,1,2")
    p.add_argument("--ziel")
    p.add_argument("--crf", type=int, default=23,
                   help="Bildqualität: kleiner ist besser und größer (Standard 23)")
    p.add_argument("--hoechstrate", type=int, default=2600,
                   help="Spitzenbitrate in kbit/s — deckelt die Dateigröße")
    args = p.parse_args()

    FF = ffmpeg()
    breite, hoehe = FORMATE[args.format]
    plan = json.loads((HIER / "schnitt.json").read_text(encoding="utf-8"))
    teile = plan["teile"]

    nur = {int(n) for n in args.nur_teile.split(",")} if args.nur_teile else None

    # Nur die Boomerangs bauen, die von den gewählten Teilen gebraucht werden —
    # sonst blockiert ein noch fehlender Clip auch den Test eines anderen Teils.
    gebraucht = sorted({t["quelle"] for n, t in enumerate(teile)
                        if t["typ"] == "clip" and (nur is None or n in nur)})
    print(f"Stufe 1: {len(gebraucht)} Boomerangs")
    for name in gebraucht:
        if boomerang_bauen(name, args.format, breite, hoehe) is None:
            raise SystemExit(f"Clip fehlt: bauplatz/clips/{name}.mp4 — "
                             f"erst clips_erzeugen.py laufen lassen.")
    print(f"Stufe 2: {len(teile)} Teile")
    gebaut = []
    for nummer, teil in enumerate(teile):
        if nur is not None and nummer not in nur:
            continue
        gebaut.append(teil_bauen(teil, nummer, args.format, breite, hoehe,
                                 plan["ausschnitte"]))
        print(f"  {nummer:>3}/{len(teile)} {teil['typ']:<7} {teil['quelle']:<16} "
              f"{teil['bis'] - teil['von']:5.1f} s")

    if nur is not None:
        print("Nur Teile gebaut — kein Zusammenbau.")
        return 0

    ziel = Path(args.ziel) if args.ziel else HIER / f"gutachten-troll_{args.format}.mp4"
    print(f"Stufe 3: zusammensetzen → {ziel.name}")
    zusammensetzen(gebaut, args.format, ziel, plan["dauer"], args.crf,
                   args.hoechstrate)
    print(f"fertig: {ziel} ({ziel.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
