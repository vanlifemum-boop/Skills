#!/usr/bin/env python3
"""schwenk.py — aus einem Standbild einen ruhigen Clip machen, ohne KI.

Für Belege ist das der einzige vertretbare Weg: Ein Video-Modell kann Zeichen
verändern oder erfinden, und aus einem Beweis wird eine Fälschung. Ein Schwenk
über das unveränderte Bild kann das nicht — er kostet auch nichts.

Zwei Bewegungen:
    schwenk   langsam senkrecht über ein hohes Bild (Chatverläufe)
    zoom      ganz langsames Heranfahren (Cover, Einzelmotive)
    zoomaus   ganz langsames Zurückfahren (Abbinder)

Beispiel:
    python3 scripts/schwenk.py beleg.png beleg-clip.mp4 --sekunden 8
    python3 scripts/schwenk.py cover.png cover-clip.mp4 --art zoom --sekunden 8
"""

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Fehler: Pillow fehlt. Installieren mit:  pip install Pillow")

BREITE, HOEHE = 720, 1280          # 9:16, die Instagram-Größe
BILDRATE = 24


def ffmpeg_pfad():
    from shutil import which
    gefunden = which("ffmpeg")
    if gefunden:
        return gefunden
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("Fehler: ffmpeg fehlt. Entweder ffmpeg installieren oder:  "
                 "pip install imageio-ffmpeg")


def bauen(quelle, ziel, sekunden, art, ruhe):
    ffmpeg = ffmpeg_pfad()
    b, h = Image.open(quelle).size

    if art == "schwenk":
        # Auf Zielbreite bringen; was übersteht, wird langsam durchfahren.
        skaliert = round(h * BREITE / b)
        if skaliert <= HOEHE:
            print("  Bild ist zu niedrig zum Schwenken — wird auf Zoom umgestellt.")
            art = "zoom"
        else:
            weg = skaliert - HOEHE
            # Am Anfang und am Ende je 'ruhe' Sekunden stehen bleiben.
            fahrt = max(sekunden - 2 * ruhe, 0.1)
            y = (f"min(max((t-{ruhe})/{fahrt},0),1)*{weg}")
            kette = (f"scale={BREITE}:-2:flags=lanczos,"
                     f"crop={BREITE}:{HOEHE}:0:'{y}'")
            print(f"  Schwenk über {weg} Pixel in {fahrt:g} s, "
                  f"je {ruhe:g} s Ruhe am Anfang und Ende")

    if art in ("zoom", "zoomaus"):
        # Um 8 Prozent heran- oder zurückfahren, mittig, über die ganze Länge.
        gross_b, gross_h = BREITE * 3, HOEHE * 3
        lauf = f"min(t/{sekunden},1)"
        z = f"1+0.08*{lauf}" if art == "zoom" else f"1.08-0.08*{lauf}"
        kette = (f"scale={gross_b}:{gross_h}:force_original_aspect_ratio=increase:flags=lanczos,"
                 f"crop={gross_b}:{gross_h},"
                 f"crop=w='{gross_b}/({z})':h='{gross_h}/({z})':x='(iw-ow)/2':y='(ih-oh)/2',"
                 f"scale={BREITE}:{HOEHE}:flags=lanczos")
        richtung = "auf 108" if art == "zoom" else "von 108 auf 100"
        print(f"  Zoom {richtung} Prozent über {sekunden:g} s")

    ruf = subprocess.run([
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-loop", "1", "-t", str(sekunden), "-i", str(quelle),
        "-vf", kette + f",fps={BILDRATE},format=yuv420p",
        "-c:v", "libx264", "-crf", "16", "-preset", "slow",
        str(ziel),
    ], capture_output=True, text=True)
    if ruf.returncode != 0:
        sys.exit(f"ffmpeg-Fehler:\n{ruf.stderr[:800]}")

    print(f"Geschrieben: {ziel}  ({sekunden:g} s, {BREITE}×{HOEHE}, 0 Credits)")


def main():
    z = argparse.ArgumentParser(
        description="Aus einem Standbild einen ruhigen 9:16-Clip machen — ohne KI.")
    z.add_argument("quelle", help="das Standbild")
    z.add_argument("ziel", help="Ausgabedatei .mp4")
    z.add_argument("--art", choices=("schwenk", "zoom", "zoomaus"), default="schwenk")
    z.add_argument("--sekunden", type=float, default=8.0)
    z.add_argument("--ruhe", type=float, default=1.0,
                   help="Standzeit am Anfang und Ende in Sekunden (nur beim Schwenk)")
    args = z.parse_args()

    if not Path(args.quelle).is_file():
        sys.exit(f"Fehler: {args.quelle} gibt es nicht.")
    bauen(args.quelle, args.ziel, args.sekunden, args.art, args.ruhe)


if __name__ == "__main__":
    main()
