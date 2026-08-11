#!/usr/bin/env python3
"""struktur.py — Wiederholungen im Song finden (Refrain 1 = Refrain 2 = Refrain 3).

Die Abschnittsgrenzen sind die halbe Miete für das Timing. Statt sie zu raten:
Chroma-Merkmale je Viertelsekunde, daraus eine Selbstähnlichkeitsmatrix. Gleiche
Musik ergibt Nebendiagonalen — dort liegen die Wiederholungen. Die Matrix wird als
Bild ausgegeben, damit man sie ansehen kann, und die stärksten Wiederholungen
werden zusätzlich als Zahlen gemeldet.

    python3 struktur.py
"""

import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

HIER = Path(__file__).parent
AUDIO = HIER / "material" / "song.mp3"
BILD = HIER / "bauplatz" / "pruefstreifen" / "struktur.png"

RATE = 22050
FENSTER = 4096
SPRUNG = RATE // 4          # ein Merkmal je 0,25 s
MIN_ABSTAND = 20.0          # Wiederholungen näher als 20 s sind nur Nachbarschaft


def ffmpeg_pfad():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def chroma():
    """Zwölf Tonklassen je Zeitschritt, lautstärkeunabhängig normiert."""
    roh = subprocess.run(
        [ffmpeg_pfad(), "-v", "error", "-i", str(AUDIO), "-ac", "1",
         "-ar", str(RATE), "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    signal = np.frombuffer(roh, dtype=np.float32).astype(np.float64)

    anzahl = 1 + (len(signal) - FENSTER) // SPRUNG
    stapel = np.lib.stride_tricks.sliding_window_view(signal, FENSTER)[::SPRUNG][:anzahl]
    spektrum = np.abs(np.fft.rfft(stapel * np.hanning(FENSTER), axis=1))

    frequenzen = np.fft.rfftfreq(FENSTER, 1 / RATE)
    brauchbar = (frequenzen > 55) & (frequenzen < 2000)
    halbtoene = np.round(12 * np.log2(frequenzen[brauchbar] / 440.0) + 69).astype(int)
    klassen = halbtoene % 12

    merkmale = np.zeros((anzahl, 12))
    gewicht = spektrum[:, brauchbar]
    for k in range(12):
        merkmale[:, k] = gewicht[:, klassen == k].sum(axis=1)

    # Je Zeitschritt auf Länge 1 — dann ist das Skalarprodukt ein Ähnlichkeitsmaß.
    laenge = np.linalg.norm(merkmale, axis=1, keepdims=True)
    return merkmale / np.maximum(laenge, 1e-9)


def main():
    merkmale = chroma()
    schritt = SPRUNG / RATE
    n = len(merkmale)

    # Über 2 s mitteln: glättet Einzeltöne weg, Akkordfolgen bleiben.
    breit = int(2.0 / schritt)
    kern = np.ones(breit) / breit
    geglaettet = np.vstack([np.convolve(merkmale[:, k], kern, mode="same") for k in range(12)]).T
    laenge = np.linalg.norm(geglaettet, axis=1, keepdims=True)
    geglaettet = geglaettet / np.maximum(laenge, 1e-9)

    aehnlich = geglaettet @ geglaettet.T

    # Als Bild: hell = ähnlich.
    bild = ((aehnlich - aehnlich.min()) / (aehnlich.max() - aehnlich.min()) * 255).astype(np.uint8)
    BILD.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(bild).resize((1100, 1100), Image.LANCZOS).save(BILD)

    # Nebendiagonalen: für jeden Versatz die mittlere Ähnlichkeit entlang der Diagonale.
    min_versatz = int(MIN_ABSTAND / schritt)
    werte = []
    for versatz in range(min_versatz, n - min_versatz):
        diagonale = np.diagonal(aehnlich, offset=versatz)
        werte.append((float(diagonale.mean()), versatz * schritt))
    werte.sort(reverse=True)

    print(f"Bild: {BILD}")
    print(f"Auflösung {schritt:.2f} s, {n} Schritte, Dauer {n*schritt:.1f} s")
    print("\nStärkste Wiederholungs-Abstände:")
    gesehen = []
    for wert, versatz in werte:
        if any(abs(versatz - g) < 8 for g in gesehen):
            continue
        gesehen.append(versatz)
        print(f"  Versatz {versatz:7.2f} s   Ähnlichkeit {wert:.3f}")
        if len(gesehen) >= 8:
            break

    json.dump(
        {"aufloesung": schritt, "beste_versaetze": [round(v, 2) for _, v in werte[:200]]},
        open(HIER / "bauplatz" / "struktur.json", "w"), ensure_ascii=False)


if __name__ == "__main__":
    main()
