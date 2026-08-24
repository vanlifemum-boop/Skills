#!/usr/bin/env python3
"""einfrieren.py — Bildbereiche eines Clips aus dem Originalbild zurückholen.

Video-Modelle lassen feine Schrift zerfallen: aus „TATORT" wird nach zwei Sekunden
ein Fantasiezeichen. Statt dafür einen neuen Clip zu bezahlen, wird der betroffene
Bereich aus dem unveränderten Standbild als feste Ebene über den Clip gelegt.

Kostet nichts, ist pixelgenau und nimmt dem Modell die Gelegenheit, Zeichen zu
erfinden — bei Belegen der einzige vertretbare Weg.

Beispiel:
    python3 scripts/einfrieren.py clip.mp4 original.png clip-fest.mp4 \
        --bereich 140,14,590,86
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Fehler: Pillow fehlt. Installieren mit:  pip install Pillow")


def ffmpeg_pfad():
    """Erst das System fragen, sonst das mitgelieferte Binary von imageio-ffmpeg."""
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


def masse(ffmpeg, video):
    ruf = subprocess.run([ffmpeg, "-hide_banner", "-i", str(video)],
                         capture_output=True, text=True)
    for zeile in ruf.stderr.splitlines():
        if "Video:" in zeile:
            for stueck in zeile.split(","):
                stueck = stueck.strip().split(" ")[0]
                if "x" in stueck:
                    b, _, h = stueck.partition("x")
                    if b.isdigit() and h.isdigit():
                        return int(b), int(h)
    sys.exit("Fehler: Bildmaße des Clips nicht gefunden.")


def einfrieren(video, standbild, ziel, bereiche):
    ffmpeg = ffmpeg_pfad()
    breite, hoehe = masse(ffmpeg, video)

    # Das Standbild auf die Clipgröße bringen, damit die Bereiche passen.
    quelle = Image.open(standbild).convert("RGBA").resize((breite, hoehe), Image.LANCZOS)
    ebene = Image.new("RGBA", (breite, hoehe), (0, 0, 0, 0))
    for text in bereiche:
        teile = [int(w) for w in text.split(",")]
        if len(teile) != 4:
            sys.exit(f"Fehler: Bereich braucht vier Werte: {text!r}")
        l, o, r, u = teile
        ebene.paste(quelle.crop((l, o, r, u)), (l, o))
        print(f"  eingefroren: {l},{o} bis {r},{u}")

    with tempfile.TemporaryDirectory() as tmp:
        maske = Path(tmp) / "ebene.png"
        ebene.save(maske)
        ruf = subprocess.run([
            ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(video), "-i", str(maske),
            "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto[v]",
            "-map", "[v]", "-c:v", "libx264", "-crf", "16",
            "-pix_fmt", "yuv420p", "-preset", "slow",
            str(ziel),
        ], capture_output=True, text=True)
        if ruf.returncode != 0:
            sys.exit(f"ffmpeg-Fehler:\n{ruf.stderr[:800]}")

    print(f"Geschrieben: {ziel}")


def main():
    z = argparse.ArgumentParser(
        description="Bildbereiche eines Clips aus dem Originalbild zurückholen.")
    z.add_argument("video", help="der erzeugte Clip")
    z.add_argument("standbild", help="das unveränderte Ausgangsbild")
    z.add_argument("ziel", help="Ausgabedatei")
    z.add_argument("--bereich", action="append", required=True, metavar="L,O,R,U",
                   help="links,oben,rechts,unten in Pixeln der CLIP-Größe")
    args = z.parse_args()

    for pfad in (args.video, args.standbild):
        if not Path(pfad).is_file():
            sys.exit(f"Fehler: {pfad} gibt es nicht.")
    einfrieren(args.video, args.standbild, args.ziel, args.bereich)


if __name__ == "__main__":
    main()
