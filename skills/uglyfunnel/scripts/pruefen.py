#!/usr/bin/env python3
"""Prüft alle Funnel-Seiten: Ganzseiten-Screenshots bei 1920 und 390 px nach <funnels>/_vorschau/,
meldet JS-Fehler, kaputte Bilder und seitliches Scrollen am Handy.
Aufruf: python3 pruefen.py <pfad/zu/funnels>   (braucht: pip install playwright && playwright install chromium)"""
import sys, pathlib
from playwright.sync_api import sync_playwright

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'funnels').resolve()
out = root / '_vorschau'; out.mkdir(exist_ok=True)
seiten = sorted(p for p in root.rglob('*.html') if '_vorschau' not in p.parts)
probleme = 0
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for p in seiten:
        name = str(p.relative_to(root).with_suffix('')).replace('/', '_')
        for w, h in ((1920, 1080), (390, 844)):
            pg = b.new_page(viewport={'width': w, 'height': h})
            fehler = []
            pg.on('pageerror', lambda e: fehler.append(str(e)))
            pg.on('console', lambda m: fehler.append(m.text) if m.type == 'error' else None)
            pg.goto(p.as_uri(), wait_until='networkidle')
            pg.wait_for_timeout(500)
            kaputt = pg.evaluate("[...document.images].filter(i => i.complete && !i.naturalWidth).map(i => i.getAttribute('src'))")
            breite = pg.evaluate('document.documentElement.scrollWidth')
            pg.screenshot(path=str(out / f'{name}_{w}.png'), full_page=True)
            meld = []
            if fehler: meld.append(f'JS-Fehler: {fehler[:3]}')
            if kaputt: meld.append(f'Bilder fehlen: {kaputt[:5]}')
            if breite > w + 1: meld.append(f'seitliches Scrollen ({breite}px)')
            if meld: probleme += 1
            print(f"{'!!' if meld else 'ok'} {name} {w}px " + ' | '.join(meld))
            pg.close()
    b.close()
print(f'\n{len(seiten)} Seiten geprüft, {probleme} Ansichten mit Problemen. Screenshots: {out}')
