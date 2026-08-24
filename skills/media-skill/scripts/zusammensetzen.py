#!/usr/bin/env python3
"""zusammensetzen.py — mehrere Clips zu einem Reel aneinanderhängen.

Harte Schnitte, keine Blenden: Die Text-Einblendungen liegen später auf festen
Timecodes, und eine Blende verschiebt sie.

Beispiel:
    python3 scripts/zusammensetzen.py reel-1.mp4 C01.mp4 B02.mp4 C07.mp4
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


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


def zusammensetzen(ziel, teile):
    ffmpeg = ffmpeg_pfad()
    for t in teile:
        if not Path(t).is_file():
            sys.exit(f"Fehler: {t} gibt es nicht.")

    # Neu kodieren statt nur aneinanderreihen: die Clips kommen aus
    # verschiedenen Quellen und haben nicht denselben Bildaufbau.
    eingaben = []
    for t in teile:
        eingaben += ["-i", str(t)]
    kette = "".join(f"[{i}:v]" for i in range(len(teile)))
    kette += f"concat=n={len(teile)}:v=1:a=0[v]"

    ruf = subprocess.run([
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y", *eingaben,
        "-filter_complex", kette, "-map", "[v]",
        "-c:v", "libx264", "-crf", "18", "-preset", "slow",
        "-pix_fmt", "yuv420p", "-r", "24", str(ziel),
    ], capture_output=True, text=True)
    if ruf.returncode != 0:
        sys.exit(f"ffmpeg-Fehler:\n{ruf.stderr[:800]}")

    dauer = subprocess.run([ffmpeg, "-hide_banner", "-i", str(ziel)],
                           capture_output=True, text=True).stderr
    laenge = next((z.split("Duration:")[1].split(",")[0].strip()
                   for z in dauer.splitlines() if "Duration:" in z), "?")
    print(f"Geschrieben: {ziel}  ({len(teile)} Clips, {laenge})")


def main():
    z = argparse.ArgumentParser(description="Clips zu einem Reel aneinanderhängen.")
    z.add_argument("ziel", help="Ausgabedatei .mp4")
    z.add_argument("teile", nargs="+", help="die Clips in der gewünschten Reihenfolge")
    args = z.parse_args()
    zusammensetzen(args.ziel, args.teile)


if __name__ == "__main__":
    main()
