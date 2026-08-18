# Bildwelt der Schulung über kie.ai erzeugen

Zwei Dateien:

- **`prompts.json`** — der Bildplan als Daten: der gemeinsame Stil-Block, das Referenzmotiv
  und die 16 Motive. Hier änderst du Bildideen, nicht im Skript.
- **`kie_bilder.py`** — erzeugt, lädt herunter, komprimiert, gibt Data-URIs aus.

## Warum zwei Phasen

Die Stilkonsistenz hängt an **einem** Anker. Zuerst entsteht das Referenzbild der Kompassrose,
du suchst einen Kandidaten aus, und dieses eine Bild geht danach als Bildreferenz in **jede**
weitere Generation. Ohne diesen Schritt bekommst du 16 hübsche Einzelbilder, die zusammen nach
Stockfoto-Sammelsurium aussehen.

## Ablauf

```bash
export KIE_AI_API_KEY=dein_schluessel     # nicht ins Repo, nicht in Chats
cd schulung/tools

# 1) Referenzbild, zwei Kandidaten
python3 kie_bilder.py ref

# 2) Kandidaten ansehen (out/REF_1.png, out/REF_2.png) und einen aussuchen.
#    Ein eigener Upload ist NICHT noetig: kie.ai liefert das erzeugte Bild
#    bereits oeffentlich aus, die URL steht in out/state.json.

# 3) Erst zwei Testmotive gegen den Anker prüfen — das dunkelste und das hellste
python3 kie_bilder.py motive --ref-url https://…/REF_1.png --nur IMG_L6,IMG_L10

# 4) Wenn beide sitzen: der Rest
python3 kie_bilder.py motive --ref-url https://…/REF_1.png

# 5) Komprimieren und als Data-URIs ausgeben (braucht Pillow)
pip install Pillow
python3 kie_bilder.py pack
```

Ergebnis: **`out/bilder.json`** — ein Objekt `{"IMG_L1": "data:image/webp;base64,…", …}`,
das in die Platzhalter der HTML-Schulung eingesetzt wird.

## Was wo landet — und was davon ins Repo gehört

```
out/master/     die Master in voller Auflösung (2 Referenzkandidaten + 16 Motive)  → versioniert
out/bilder.json die einsetzfertigen Data-URIs                                       → versioniert
out/state.json  Task-IDs und Quell-URLs, macht den Lauf nachvollziehbar             → versioniert
out/…           alles Übrige: Zwischenstände, Downloads, Caches                     → ignoriert
```

Die `.gitignore` im Wurzelverzeichnis setzt das durch (`out/*` plus drei Ausnahmen). **Deshalb
schreibt das Skript die Master nach `out/master/`, nicht direkt nach `out/`** — dort wären sie
von der Regel erfasst und nach dem nächsten Klon verloren, obwohl sie Guthaben gekostet haben.

`pack` akzeptiert in `out/master/` sowohl `.png` (frisch erzeugt) als auch `.webp` (die
versionierte Sicherung). Damit lässt sich `bilder.json` nach einem frischen Klon neu erzeugen,
ohne ein einziges Bild noch einmal zu bezahlen.

`state.json` enthält Task-IDs und Quell-URLs, **keinen API-Schlüssel**.

## Was das Skript für dich mitdenkt

- **Resumierbar.** Jeder fertige Task landet in `out/state.json` und wird beim nächsten Start
  übersprungen. Ein Abbruch kostet nichts doppelt.
- **`--dry-run`** zeigt die fertig zusammengebauten Prompts, ohne etwas zu senden und ohne
  etwas zu kosten. Nutz das vor dem ersten echten Lauf.
- **`--nur IMG_L6,IMG_L10`** generiert gezielt einzelne Motive nach.
- **`--neu`** überschreibt bereits erzeugte Motive.
- Backoff bei `429` und `5xx`, damit ein Rate-Limit den Lauf nicht abbricht.

## Netzwerk-Allowlist

Wenn das in einer Claude-Cloud-Umgebung laufen soll, reicht `api.kie.ai` **nicht**. kie.ai legt
die fertigen Bilder auf eigenen Hosts ab, und der Download scheitert sonst, obwohl die
Generierung geklappt hat. Diese Hosts stecken im offiziellen MCP-Server von kie.ai und sind alle
nötig:

```
api.kie.ai
proxy.kie.ai
kieai.redpandaai.co
tempfile.aiquickdraw.com
*.kie.ai
```

Bei **Network access → Custom** eintragen und den Haken *„Also include default list of common
package managers"* **gesetzt lassen** — sonst fehlen PyPI und npm, und Pillow lässt sich nicht
mehr installieren.

## Alternative: der offizielle MCP-Server

Es gibt einen fertigen MCP-Server, der dieselbe API abdeckt und zusätzlich Video, Musik und
Sprache kann:

```bash
claude mcp add kie-ai --env KIE_AI_API_KEY=… -- npx -y @felores/kie-ai-mcp-server
```

Er bringt unter anderem `nano_banana_image` mit und erwartet Bildreferenzen im Feld `image_urls`
— dieselbe Konvention, die dieses Skript nutzt. Für einen reinen Bilderlauf tut es das Skript
hier genauso und ist besser nachvollziehbar (resumierbar, `--dry-run`, feste Prompts in
`prompts.json`). Der MCP-Server lohnt sich, sobald Voiceover oder Video dazukommen.

**Beide Wege brauchen dieselbe Allowlist.** Der MCP-Server läuft lokal im Container und geht
über denselben Netzwerkausgang.

## Die eine Stelle, die klemmen kann

kie.ai bündelt viele Modelle, und die **Feldnamen im `input`-Block unterscheiden sich je
Modell**. Das Skript folgt dem dokumentierten Muster (`createTask` → `recordInfo`), aber die
genaue Schreibweise der Bildreferenz variiert: mal `image_urls`, mal `input_image`, mal
`reference_images`.

Falls die API einen Parameter ablehnt, sind das die beiden Schrauben — beide per Umgebungs-
variable, ohne das Skript anzufassen:

```bash
export KIE_MODEL=nano-banana-2            # anderes Modell
export KIE_REF_FIELD=input_image          # anderer Feldname für die Referenz
```

**Das Präfix ist uneinheitlich — nicht raten, sondern probieren.** Am 10.08.2026 gegen die
API geprüft: `nano-banana-pro`, `nano-banana-2` und `google/nano-banana` werden akzeptiert,
`google/nano-banana-pro`, `google/nano-banana-2` und `nano-banana` dagegen mit 422 abgelehnt.
Ein abgelehnter `createTask` kostet nichts, Durchprobieren ist also gefahrlos.

`image_urls` als Standard ist inzwischen bestätigt — der offizielle MCP-Server nutzt denselben
Feldnamen. Bekannte Modellkennungen dort: `nano-banana`, `nano-banana-2`, `nano-banana-2-lite`,
`nano-banana-edit`. Gegenprüfen unter <https://docs.kie.ai/> beim jeweiligen Modell.

## Kosten

Grober Rahmen aus der Recherche — **im eigenen Dashboard gegenprüfen**, Preise ändern sich:

| Modell | ca. je Bild | 23 Generationen (16 Motive + 2 Kandidaten + 5 Nachzieher) |
|---|---|---|
| `nano-banana-pro` | 18 Credits (~0,077 $) | ~1,80 $ |
| `nano-banana-2` (1K) | ~0,04–0,07 $ | ~1,20 $ |

Gemessen am 10.08.2026: ein Pro-Bild kostet 18 Credits, der komplette Lauf
(2 Kandidaten + 16 Motive + 1 Nachzieher) 372 Credits ≈ 1,60 $.

Empfehlung: **Nano Banana Pro** für das Referenzbild und die zwei Testmotive, weil dort die
Stilentscheidung fällt. Für den Rest reicht die günstigere Variante, wenn der Anker sitzt.

## Abnahme je Bild

Kein lesbarer Text · keine Gesichter oder Hände · Farbstimmung deckt sich mit dem Anker ·
wirkt weder anklagend noch rührselig · keine falschen Verfahrensinhalte (kein Richterhammer,
keine Robe, keine US-Gerichtssaal-Ikonografie).
