# kie.ai überall einbinden

kie.ai ist ein API-Aggregator für Bild-, Video-, Musik- und Sprachgenerierung (Nano Banana,
Veo 3, Suno, ElevenLabs, Seedance, Flux, Midjourney und weitere) — bezahlt pro Aufruf, ohne Abo.

„Überall nutzbar" bedeutet vier verschiedene Dinge, und die brauchen unterschiedliche Schritte.
**Ebene 1 und 2 sind erledigt und liegen im Repo. Ebene 3 musst du in der Oberfläche machen.
Ebene 4 ist ein eigenes Projekt.**

---

## Ebene 1 — In diesem Repo · erledigt

`.mcp.json` im Wurzelverzeichnis registriert den Server projektweit:

```json
{
  "mcpServers": {
    "kie-ai": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@felores/kie-ai-mcp-server"],
      "env": { "KIE_AI_API_KEY": "${KIE_AI_API_KEY}" }
    }
  }
}
```

**Der Schlüssel steht bewusst nicht in der Datei**, nur die Referenz darauf. Claude Code löst
`${VAR}` in `.mcp.json` auf. Ist die Variable nicht gesetzt, lädt die Konfiguration trotzdem und
meldet den fehlenden Wert in `claude mcp list`.

Dazu in `.claude/settings.json`: `enableAllProjectMcpServers`, die WebFetch-Berechtigungen und die
Sandbox-Allowlist.

**Ein Haken, den du kennen solltest:** In einem frisch geklonten, noch nicht vertrauten Ordner
wird `enableAllProjectMcpServers` aus einer eingecheckten `.claude/settings.json` **ignoriert** —
ein Repo kann seine eigenen Server nicht freigeben. Der Server steht dann auf
`⏸ Pending approval`. In einer interaktiven Sitzung genügt einmal `claude` starten und den
Vertrauensdialog bestätigen. Für nicht-interaktive Cloud-Sessions ist Ebene 3 der bessere Weg.

---

## Ebene 2 — Auf deiner Maschine, in allen Projekten

Einmalig, gilt danach überall:

```bash
claude mcp add -s user kie-ai --env KIE_AI_API_KEY=dein_schluessel \
  -- npx -y @felores/kie-ai-mcp-server
```

Geprüft: Der Server ist damit **sofort verbunden**, ohne Freigabedialog, und in jedem Projekt
verfügbar. User-Scope schlägt Projekt-Scope bei gleichem Namen — die `.mcp.json` wird dann also
überschattet, was hier gewollt ist.

Kontrolle: `claude mcp get kie-ai` → `Scope: User config`, `Status: √ Connected`.

---

## Ebene 3 — Cloud-Sessions (Claude Code on the web)

Zwei Einstellungen in der Umgebung, beide über das **Wolken-Symbol über dem Eingabefeld** auf
claude.ai/code → Zahnrad an der Umgebung.

### a) Netzwerkzugriff

**Network access → Custom**, und diese Hosts eintragen. `api.kie.ai` allein reicht **nicht** —
die fertigen Dateien liegen auf eigenen Ablage-Hosts, sonst scheitert der Download, obwohl die
Generierung geklappt und Guthaben gekostet hat:

```
api.kie.ai
proxy.kie.ai
kieai.redpandaai.co
tempfile.aiquickdraw.com
*.kie.ai
```

Den Haken *„Also include default list of common package managers"* **gesetzt lassen** — sonst
fehlen npm und PyPI, und schon `npx` kann den MCP-Server nicht mehr laden.

### b) Schlüssel und Registrierung

`KIE_AI_API_KEY=…` in die **Environment variables** der Umgebung.

> Die Doku rät davon ab, Schlüssel dort abzulegen: Jeder, der die Umgebung nutzt, kann sie lesen,
> und es gibt keinen Secrets-Store. Praktikabler Umgang: eine **eigene Umgebung** nur dafür, den
> Schlüssel als **Wegwerf-Schlüssel** behandeln und nach getaner Arbeit auf kie.ai widerrufen.
> Und die Session nicht öffentlich teilen.

Damit der Server ohne Freigabedialog startet, zusätzlich ins **Setup script** der Umgebung:

```bash
claude mcp add -s user kie-ai --env KIE_AI_API_KEY="$KIE_AI_API_KEY" \
  -- npx -y @felores/kie-ai-mcp-server
```

Das umgeht die Vertrauensfrage aus Ebene 1 vollständig, weil User-Scope auch in einem nicht
vertrauten Ordner gilt.

**Wichtig:** Eine laufende Session übernimmt Änderungen an der Umgebung **nicht**. Netzwerk-
richtlinie und Variablen werden beim Start einmal festgeschrieben. Nach jeder Änderung eine
**neue Session** starten und dort die Umgebung auswählen.

Test in der neuen Session:

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://api.kie.ai/
```

Alles außer `000` heißt: Es läuft.

---

## Ebene 4 — Als Connector in claude.ai (Chat, Mobile, Desktop)

**Das geht heute nicht ohne eigenen Server.** kie.ai bietet keinen öffentlichen Remote-MCP-
Endpunkt, den man als Connector eintragen könnte. Der Server von `@felores` läuft standardmäßig
als lokaler stdio-Prozess.

Er kann aber auch als **Remote-Dienst über Streamable HTTP** laufen — eine Instanz für mehrere
Clients, mit Bearer-Token-Authentifizierung und Host-Allowlist, Dockerfile und Coolify-Compose
liegen im Projekt bei (<https://github.com/felores/kie-cli-mcp>).

Der Weg wäre also: selbst hosten, mit TLS und Token absichern, dann die URL in den
claude.ai-Connector-Einstellungen eintragen. Danach wäre kie.ai tatsächlich überall verfügbar,
auch im Chat und auf dem Handy.

**Mein Rat: erst mal nicht.** Das ist ein eigener Betriebsaufwand samt öffentlich erreichbarem
Endpunkt, hinter dem dein Guthaben hängt. Ebene 2 und 3 decken Claude Code vollständig ab.
Sinnvoll wird Ebene 4, wenn mehrere Leute oder mehrere Geräte denselben Zugang brauchen.

---

## Was der Server kann

`@felores/kie-ai-mcp-server`, Version 3.6.0. Werkzeuge unter anderem `nano_banana_image`,
`flux_kontext_image`, `bytedance_seedream_image`, `qwen_image`, `z_image`, `topaz_upscale_image`
sowie Video-, Musik- und Sprachmodelle.

Bildreferenzen erwartet er im Feld `image_urls` — dieselbe Konvention wie
`schulung/tools/kie_bilder.py`.

**Modellkennungen sind uneinheitlich, nicht raten.** Am 10.08.2026 gegen die API geprüft:
`nano-banana-pro`, `nano-banana-2` und `google/nano-banana` werden akzeptiert;
`google/nano-banana-pro`, `google/nano-banana-2` und `nano-banana` mit 422 abgelehnt. Ein
abgelehnter `createTask` kostet nichts, Durchprobieren ist gefahrlos.

## Kosten

Gemessen am 10.08.2026: ein Bild mit `nano-banana-pro` kostet 18 Credits. Der komplette Bilderlauf
der Schulung — 2 Referenzkandidaten, 16 Motive, 1 Nachzieher — lag bei 372 Credits ≈ **1,60 $**.
Guthaben ab 5 $, kein Abo.

## Skript statt MCP

Für wiederholbare Läufe mit festen Prompts ist `schulung/tools/kie_bilder.py` die bessere Wahl:
resumierbar über `state.json`, `--dry-run` ohne Kosten, Prompts versioniert in `prompts.json`.
Der MCP-Server lohnt sich für Freihand-Arbeit und für Video, Musik und Sprache.
Beide Wege brauchen dieselbe Allowlist aus Ebene 3.
