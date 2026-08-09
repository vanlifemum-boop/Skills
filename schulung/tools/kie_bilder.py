#!/usr/bin/env python3
"""
Bildwelt der Gutachten-Schulung ueber kie.ai erzeugen.

Ablauf in zwei Phasen, weil die Stilkonsistenz an einem einzigen Anker haengt:

  Phase 1 (ref)     Referenzbild der Kompassrose, mehrere Kandidaten.
                    Du suchst einen aus.
  Phase 2 (motive)  Alle uebrigen Motive, jeweils MIT dem gewaehlten
                    Referenzbild als Bildreferenz.

Danach:
  Phase 3 (pack)    Bilder auf ~80 KB komprimieren und als Base64-Data-URIs
                    in eine JSON-Datei schreiben, die in die HTML-Schulung geht.

Der Lauf ist resumierbar: Jeder abgeschlossene Task landet in state.json und
wird beim naechsten Start uebersprungen. Ein Abbruch kostet also nichts doppelt.

Aufruf:
    export KIE_AI_API_KEY=...
    python3 kie_bilder.py ref
    # Kandidat aussuchen, irgendwo oeffentlich abrufbar ablegen, dann:
    python3 kie_bilder.py motive --ref-url https://…/REF_1.png
    python3 kie_bilder.py pack

Vorher unverbindlich pruefen, was gesendet wuerde:
    python3 kie_bilder.py motive --ref-url https://…/REF_1.png --dry-run
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://api.kie.ai/api/v1/jobs"
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
STATE_PATH = OUT / "state.json"
PROMPTS_PATH = HERE / "prompts.json"

# ---------------------------------------------------------------------------
# Modellkonfiguration
#
# ACHTUNG: Die genauen Feldnamen im input-Block unterscheiden sich je Modell.
# Diese Konfiguration folgt dem dokumentierten Muster von kie.ai. Wenn die API
# einen Parameter ablehnt, ist das die einzige Stelle, die du anfassen musst —
# gegenpruefen unter https://docs.kie.ai/ beim jeweiligen Modell.
#
# Preisrahmen (Stand der Recherche, bitte im Dashboard gegenpruefen):
#   google/nano-banana-pro   ~0.12 USD je Bild, sehr gut bei Stilreferenzen
#   google/nano-banana-2     ~0.04-0.07 USD je Bild bei 1K, guenstigste Option
# ---------------------------------------------------------------------------

MODELL = os.environ.get("KIE_MODEL", "google/nano-banana-pro")
SEITENVERHAELTNIS = "16:9"
BILDGROESSE = "1K"

# Feld, unter dem das Modell Bildreferenzen erwartet. Bei einigen Modellen
# heisst es image_urls, bei anderen input_image oder reference_images.
REF_FELD = os.environ.get("KIE_REF_FIELD", "image_urls")


def input_block(prompt: str, ref_url: str | None) -> dict:
    """Baut den modellspezifischen input-Block."""
    block: dict = {
        "prompt": prompt,
        "aspect_ratio": SEITENVERHAELTNIS,
        "image_size": BILDGROESSE,
        "output_format": "png",
    }
    if ref_url:
        block[REF_FELD] = [ref_url]
    return block


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


def api_key() -> str:
    # KIE_AI_API_KEY ist der Name, den auch der offizielle MCP-Server erwartet.
    # KIE_API_KEY wird als Zweitname akzeptiert, damit beide Schreibweisen gehen.
    for name in ("KIE_AI_API_KEY", "KIE_API_KEY"):
        key = os.environ.get(name, "").strip()
        if key:
            return key
    sys.exit(
        "Kein API-Schluessel gesetzt.\n"
        "  export KIE_AI_API_KEY=dein_schluessel\n"
        "Den Schluessel nicht ins Repo schreiben und nicht in Chats einfuegen."
    )


def request(method: str, url: str, body: dict | None = None, tries: int = 5) -> dict:
    """HTTP mit exponentiellem Backoff bei 429 und 5xx."""
    data = json.dumps(body).encode() if body is not None else None
    for versuch in range(1, tries + 1):
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {api_key()}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:400]
            if e.code in (429, 500, 502, 503, 504) and versuch < tries:
                wartezeit = 2**versuch
                print(f"    HTTP {e.code}, neuer Versuch in {wartezeit}s — {detail[:120]}")
                time.sleep(wartezeit)
                continue
            sys.exit(f"HTTP {e.code} bei {method} {url}\n{detail}")
        except urllib.error.URLError as e:
            if versuch < tries:
                wartezeit = 2**versuch
                print(f"    Netzwerkfehler ({e.reason}), neuer Versuch in {wartezeit}s")
                time.sleep(wartezeit)
                continue
            sys.exit(f"Netzwerkfehler bei {method} {url}: {e.reason}")
    raise AssertionError("unerreichbar")


def task_anlegen(prompt: str, ref_url: str | None) -> str:
    antwort = request(
        "POST",
        f"{BASE}/createTask",
        {"model": MODELL, "input": input_block(prompt, ref_url)},
    )
    task_id = (antwort.get("data") or {}).get("taskId") or antwort.get("taskId")
    if not task_id:
        sys.exit(f"Keine taskId in der Antwort:\n{json.dumps(antwort, indent=2)[:800]}")
    return task_id


def auf_ergebnis_warten(task_id: str, max_sekunden: int = 600) -> list[str]:
    """Pollt recordInfo bis fertig. Gibt die Bild-URLs zurueck."""
    start = time.time()
    intervall = 5
    while True:
        antwort = request("GET", f"{BASE}/recordInfo?taskId={task_id}")
        daten = antwort.get("data") or {}
        zustand = str(daten.get("state") or daten.get("status") or "").lower()

        if zustand in ("success", "succeeded", "completed", "1"):
            roh = daten.get("resultJson") or daten.get("result") or {}
            if isinstance(roh, str):
                roh = json.loads(roh)
            urls = roh.get("resultUrls") or roh.get("images") or roh.get("urls") or []
            urls = [u if isinstance(u, str) else u.get("url") for u in urls]
            urls = [u for u in urls if u]
            if not urls:
                sys.exit(f"Fertig, aber keine URL gefunden:\n{json.dumps(daten, indent=2)[:800]}")
            return urls

        if zustand in ("fail", "failed", "error", "2", "3"):
            grund = daten.get("failMsg") or daten.get("errorMessage") or daten
            sys.exit(f"Task {task_id} fehlgeschlagen: {grund}")

        if time.time() - start > max_sekunden:
            sys.exit(f"Timeout nach {max_sekunden}s fuer Task {task_id} (Zustand: {zustand!r})")

        time.sleep(intervall)
        intervall = min(intervall + 2, 15)


def herunterladen(url: str, ziel: Path) -> None:
    ziel.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=180) as r, open(ziel, "wb") as f:
        f.write(r.read())


# ---------------------------------------------------------------------------
# Zustand
# ---------------------------------------------------------------------------


def state_laden() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"fertig": {}}


def state_sichern(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def plan_laden() -> dict:
    return json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))


def vollprompt(plan: dict, prompt: str, akzent: str | None = None) -> str:
    teile = [prompt.strip().rstrip(".")]
    if akzent:
        teile.append(akzent)
    teile.append(plan["style_block"])
    return ", ".join(teile)


# ---------------------------------------------------------------------------
# Phasen
# ---------------------------------------------------------------------------


def phase_ref(args) -> None:
    plan = plan_laden()
    ref = plan["reference"]
    anzahl = args.kandidaten or ref.get("candidates", 2)
    prompt = vollprompt(plan, ref["prompt"])

    print(f"Referenzbild, {anzahl} Kandidaten, Modell {MODELL}")
    print(f"  Prompt: {prompt[:150]}…\n")
    if args.dry_run:
        print("  [dry-run] nichts gesendet")
        return

    state = state_laden()
    for i in range(1, anzahl + 1):
        schluessel = f"REF_{i}"
        if schluessel in state["fertig"]:
            print(f"  {schluessel}: bereits vorhanden, uebersprungen")
            continue
        print(f"  {schluessel}: Task wird angelegt …")
        task_id = task_anlegen(prompt, None)
        urls = auf_ergebnis_warten(task_id)
        ziel = OUT / f"{schluessel}.png"
        herunterladen(urls[0], ziel)
        state["fertig"][schluessel] = {"task": task_id, "url": urls[0], "datei": str(ziel)}
        state_sichern(state)
        print(f"  {schluessel}: fertig → {ziel}")

    print(
        "\nJetzt einen Kandidaten aussuchen und Phase 2 damit starten:\n"
        "  python3 kie_bilder.py motive --ref out/REF_1.png"
    )


def phase_motive(args) -> None:
    plan = plan_laden()
    motive = plan["motifs"]

    if args.nur:
        gewuenscht = {m.strip() for m in args.nur.split(",")}
        motive = [m for m in motive if m["id"] in gewuenscht]
        if not motive:
            sys.exit(f"Keine Motive passen zu --nur {args.nur}")

    # Das Referenzbild muss fuer die API oeffentlich erreichbar sein.
    ref_url = args.ref_url
    if not ref_url and not args.ohne_referenz:
        sys.exit(
            "Fuer die Bildreferenz braucht die API eine erreichbare URL.\n"
            "Lade das gewaehlte Referenzbild irgendwo hin, wo kie.ai es abrufen kann,\n"
            "und uebergib die URL mit --ref-url.\n"
            "\n"
            "Wenn du bewusst ohne Anker generieren willst:  --ohne-referenz\n"
            "Dann bricht allerdings die Stilkonsistenz ueber die 16 Bilder."
        )

    print(f"{len(motive)} Motive, Modell {MODELL}")
    print(f"Referenz: {ref_url or 'KEINE (--ohne-referenz)'}\n")

    state = state_laden()
    for m in motive:
        schluessel = m["id"]
        if schluessel in state["fertig"] and not args.neu:
            print(f"  {schluessel}: bereits vorhanden, uebersprungen")
            continue

        prompt = vollprompt(plan, m["prompt"], m.get("accent"))
        print(f"  {schluessel} (Level {m['level']})")
        if args.dry_run:
            print(f"      {prompt[:170]}…")
            continue

        task_id = task_anlegen(prompt, ref_url)
        urls = auf_ergebnis_warten(task_id)
        ziel = OUT / f"{schluessel}.png"
        herunterladen(urls[0], ziel)
        state["fertig"][schluessel] = {"task": task_id, "url": urls[0], "datei": str(ziel)}
        state_sichern(state)
        print(f"      fertig → {ziel}")
        time.sleep(1)  # freundlich zur Rate-Limit-Grenze

    if not args.dry_run:
        print("\nAlle Motive erzeugt. Weiter mit:  python3 kie_bilder.py pack")


def phase_pack(args) -> None:
    """Komprimiert auf ~80 KB und schreibt Data-URIs als JSON."""
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow fehlt:  pip install Pillow")

    dateien = sorted(OUT.glob("IMG_*.png"))
    if not dateien:
        sys.exit(f"Keine IMG_*.png in {OUT} — erst Phase 2 laufen lassen.")

    ziel_bytes = args.kb * 1024
    ergebnis: dict[str, str] = {}
    print(f"{len(dateien)} Bilder, Zielgroesse ~{args.kb} KB\n")

    for pfad in dateien:
        bild = Image.open(pfad).convert("RGB")
        bild.thumbnail((args.breite, args.breite * 9 // 16), Image.LANCZOS)

        from io import BytesIO

        # Hoechste Qualitaet nehmen, die unter die Zielgroesse passt.
        # Passt keine, gewinnt die kleinste Variante — nicht die groesste.
        bestes, beste_q = None, None
        for q in range(85, 34, -5):
            puffer = BytesIO()
            bild.save(puffer, format="WEBP", quality=q, method=6)
            roh = puffer.getvalue()
            if len(roh) <= ziel_bytes:
                bestes, beste_q = roh, q
                break
            bestes, beste_q = roh, q  # bisher kleinste Variante mitnehmen

        name = pfad.stem
        ergebnis[name] = "data:image/webp;base64," + base64.b64encode(bestes).decode()
        print(f"  {name:14} {len(bestes)//1024:4} KB  (q={beste_q})")

    ziel = OUT / "bilder.json"
    ziel.write_text(json.dumps(ergebnis, indent=2), encoding="utf-8")
    gesamt = sum(len(v) for v in ergebnis.values()) * 3 // 4
    print(f"\n→ {ziel}")
    print(f"  {len(ergebnis)} Bilder, zusammen ~{gesamt//1024} KB als Data-URIs")


# ---------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="phase", required=True)

    a = sub.add_parser("ref", help="Referenzbild der Kompassrose erzeugen")
    a.add_argument("--kandidaten", type=int, help="Anzahl Kandidaten (Standard aus prompts.json)")
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=phase_ref)

    b = sub.add_parser("motive", help="Alle Motive mit Referenzbild erzeugen")
    b.add_argument("--ref-url", help="Oeffentlich erreichbare URL des gewaehlten Referenzbilds")
    b.add_argument("--ohne-referenz", action="store_true", help="Ohne Anker — Stilkonsistenz bricht")
    b.add_argument("--nur", help="Nur diese IDs, kommagetrennt (z. B. IMG_L6,IMG_L10)")
    b.add_argument("--neu", action="store_true", help="Bereits erzeugte Motive neu generieren")
    b.add_argument("--dry-run", action="store_true")
    b.set_defaults(func=phase_motive)

    c = sub.add_parser("pack", help="Komprimieren und als Data-URIs ausgeben")
    c.add_argument("--kb", type=int, default=80, help="Zielgroesse je Bild in KB (Standard 80)")
    c.add_argument("--breite", type=int, default=1280, help="Maximale Breite in px (Standard 1280)")
    c.set_defaults(func=phase_pack)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
