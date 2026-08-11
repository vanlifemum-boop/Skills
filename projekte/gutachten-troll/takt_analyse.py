#!/usr/bin/env python3
"""takt_analyse.py — Taktgitter und Gesangsphrasen aus dem Song holen.

Warum das nötig ist: in dieser Umgebung ist keine Spracherkennung verfügbar
(huggingface.co ist gesperrt), der Songtext muss also ohne Transkript auf die
Zeitachse. Dafür drei Messungen aus dem Signal selbst:

  1. Taktgitter   — Onset-Hüllkurve (Spectral Flux) → Autokorrelation → BPM + Phase.
  2. Gesangsspur  — Mitte-minus-Seite je Frequenzband: was in beiden Kanälen gleich
                    laut liegt, ist die Stimme. Bandbegrenzt auf 300–3500 Hz.
  3. Phrasen      — zusammenhängende Bereiche mit Gesang, getrennt durch Atempausen.

Ergebnis: analyse.json mit bpm, taktanfängen, phrasen und der Hüllkurve.

    python3 takt_analyse.py [--audio material/song.mp3]
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HIER = Path(__file__).parent

# Analyse-Auflösung: 22050 Hz reicht für Stimme (bis 11 kHz), FFT alle 10 ms.
RATE = 22050
FENSTER = 2048
SPRUNG = 220  # 220/22050 = 9,977 ms

# Die Stimme lebt zwischen Grundton und Zischlauten.
BAND_UNTEN, BAND_OBEN = 300, 3500

# Ein Takt braucht mindestens so viele Sekunden — begrenzt die BPM-Suche.
BPM_MIN, BPM_MAX = 70, 190


def ffmpeg_pfad():
    """Der ffmpeg aus imageio-ffmpeg — siehe scripts/ensure-ffmpeg.sh."""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        import shutil
        pfad = shutil.which("ffmpeg")
        if not pfad:
            raise SystemExit("Kein ffmpeg gefunden: pip install imageio-ffmpeg")
        return pfad


def stereo_laden(audio):
    """Dekodiert die Datei nach float32-Stereo, gibt (links, rechts) zurück."""
    befehl = [
        ffmpeg_pfad(), "-v", "error", "-i", str(audio),
        "-ac", "2", "-ar", str(RATE), "-f", "f32le", "-",
    ]
    roh = subprocess.run(befehl, capture_output=True, check=True).stdout
    proben = np.frombuffer(roh, dtype=np.float32).reshape(-1, 2)
    return proben[:, 0].astype(np.float64), proben[:, 1].astype(np.float64)


def spektren(links, rechts):
    """STFT von Mitte und Seite. Gibt (betrag_mitte, betrag_seite, zeiten) zurück."""
    mitte = (links + rechts) / 2
    seite = (links - rechts) / 2

    fenster = np.hanning(FENSTER)
    anzahl = 1 + (len(mitte) - FENSTER) // SPRUNG
    indizes = np.arange(anzahl) * SPRUNG

    def stft(signal):
        # Ein Block je Sprung, gefenstert, reelle FFT.
        stapel = np.lib.stride_tricks.sliding_window_view(signal, FENSTER)[::SPRUNG][:anzahl]
        return np.abs(np.fft.rfft(stapel * fenster, axis=1))

    return stft(mitte), stft(seite), indizes / RATE


def onset_huellkurve(betrag):
    """Spectral Flux: wie viel Energie ist gegenüber dem Vorbild dazugekommen."""
    log = np.log1p(betrag)
    zuwachs = np.maximum(log[1:] - log[:-1], 0).sum(axis=1)
    zuwachs = np.concatenate([[0.0], zuwachs])
    # Gleitenden Mittelwert abziehen, damit laute Passagen nicht dominieren.
    fenster = 101
    kern = np.ones(fenster) / fenster
    grund = np.convolve(zuwachs, kern, mode="same")
    return np.maximum(zuwachs - grund, 0)


def bpm_schaetzen(huelle, zeiten):
    """Autokorrelation der Onset-Hüllkurve → Tempo und Phase des Taktschlags."""
    schritt = zeiten[1] - zeiten[0]
    signal = huelle - huelle.mean()
    korr = np.correlate(signal, signal, mode="full")[len(signal) - 1:]

    min_lag = int(60.0 / BPM_MAX / schritt)
    max_lag = int(60.0 / BPM_MIN / schritt)
    bereich = korr[min_lag:max_lag]
    lag = min_lag + int(np.argmax(bereich))
    bpm = 60.0 / (lag * schritt)

    # Phase: welcher Versatz trifft die Schläge am besten?
    beste_phase, bester_wert = 0, -np.inf
    for phase in range(lag):
        treffer = huelle[phase::lag]
        if treffer.sum() > bester_wert:
            bester_wert, beste_phase = treffer.sum(), phase

    return bpm, beste_phase * schritt, lag * schritt


def gesangs_huellkurve(betrag_mitte, betrag_seite):
    """Was in der Mitte lauter ist als an den Seiten, ist die Stimme."""
    frequenzen = np.fft.rfftfreq(FENSTER, 1 / RATE)
    band = (frequenzen >= BAND_UNTEN) & (frequenzen <= BAND_OBEN)
    mitten_ueberschuss = np.maximum(betrag_mitte[:, band] - betrag_seite[:, band], 0)
    huelle = mitten_ueberschuss.sum(axis=1)
    # Leicht glätten (50 ms), damit einzelne Konsonanten keine Lücke reißen.
    kern = np.ones(5) / 5
    return np.convolve(huelle, kern, mode="same")


def gleitender_median(werte, fenster):
    """Grobe, aber schnelle Näherung: Median je Block, dann linear dazwischen."""
    bloecke = max(len(werte) // fenster, 1)
    kanten = np.linspace(0, len(werte), bloecke + 1).astype(int)
    mitten, punkte = [], []
    for a, b in zip(kanten[:-1], kanten[1:]):
        mitten.append((a + b) / 2)
        punkte.append(np.median(werte[a:b]))
    if len(mitten) < 2:
        return np.full(len(werte), punkte[0] if punkte else 1.0)
    return np.interp(np.arange(len(werte)), mitten, punkte)


def normieren(huelle, zeiten, fenster_sek=8.0):
    """Auf den lokalen Grundpegel beziehen — der Song wird hinten deutlich lauter,
    eine feste Schwelle über die ganze Länge findet dort keine Phrasen mehr."""
    schritt = zeiten[1] - zeiten[0]
    grund = gleitender_median(huelle, int(fenster_sek / schritt))
    return huelle / np.maximum(grund, np.percentile(huelle, 20) * 0.25 + 1e-9)


def phrasen_finden(huelle, zeiten, schwelle=1.35, min_pause=0.28, min_laenge=0.30):
    """Zusammenhängende Gesangsbereiche, getrennt durch Pausen.

    `huelle` ist die auf den lokalen Grundpegel normierte Gesangskurve, `schwelle`
    also ein Faktor: 1,35 heißt „35 % über dem, was hier gerade normal ist"."""
    schritt = zeiten[1] - zeiten[0]
    aktiv = huelle > schwelle

    # Kurze Löcher schließen.
    luecke = int(min_pause / schritt)
    kanten = np.diff(aktiv.astype(int))
    starts = list(np.where(kanten == 1)[0] + 1)
    enden = list(np.where(kanten == -1)[0] + 1)
    if aktiv[0]:
        starts.insert(0, 0)
    if aktiv[-1]:
        enden.append(len(aktiv))

    roh = list(zip(starts, enden))
    verschmolzen = []
    for start, ende in roh:
        if verschmolzen and start - verschmolzen[-1][1] < luecke:
            verschmolzen[-1] = (verschmolzen[-1][0], ende)
        else:
            verschmolzen.append((start, ende))

    return [
        {"start": round(float(zeiten[s]), 3), "ende": round(float(zeiten[min(e, len(zeiten) - 1)]), 3)}
        for s, e in verschmolzen
        if (e - s) * schritt >= min_laenge
    ]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audio", default=str(HIER / "material" / "song.mp3"))
    p.add_argument("--ziel", default=str(HIER / "analyse.json"))
    args = p.parse_args()

    print("Dekodiere …", file=sys.stderr)
    links, rechts = stereo_laden(args.audio)
    dauer = len(links) / RATE

    print("Rechne Spektren …", file=sys.stderr)
    betrag_mitte, betrag_seite, zeiten = spektren(links, rechts)

    huelle_onset = onset_huellkurve(betrag_mitte + betrag_seite)
    bpm, phase, takt = bpm_schaetzen(huelle_onset, zeiten)
    huelle_gesang = normieren(gesangs_huellkurve(betrag_mitte, betrag_seite), zeiten)
    huelle_gesamt = (betrag_mitte + betrag_seite).sum(axis=1)
    huelle_gesamt = huelle_gesamt / huelle_gesamt.max()
    phrasen = phrasen_finden(huelle_gesang, zeiten)

    schlaege = np.arange(phase, dauer, takt)

    daten = {
        "dauer": round(dauer, 3),
        "bpm": round(bpm, 2),
        "schlag_abstand": round(takt, 4),
        "erster_schlag": round(phase, 4),
        "schlaege": [round(float(s), 3) for s in schlaege],
        "phrasen": phrasen,
        "aufloesung": round(float(zeiten[1] - zeiten[0]), 5),
        "huelle_gesang": [round(float(w), 3) for w in huelle_gesang],
        "huelle_gesamt": [round(float(w), 4) for w in huelle_gesamt],
    }
    Path(args.ziel).write_text(json.dumps(daten, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Dauer      {dauer:.2f} s")
    print(f"Tempo      {bpm:.1f} BPM · Schlag alle {takt:.3f} s · erster bei {phase:.3f} s")
    print(f"Phrasen    {len(phrasen)} gefunden")
    print(f"→ {args.ziel}")


if __name__ == "__main__":
    main()
