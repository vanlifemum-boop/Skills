# Skills

Claude-Code-Skills, die in **allen** Projekten gelten sollen. Jeder Skill ist ein eigener
Ordner mit einer `SKILL.md` darin — genau so erwartet Claude Code es.

## Eigene Skills und Sprache

| Skill | wofür |
|---|---|
| [`media-skill`](media-skill/) | Bilder, Videos und Sprache über die kie.ai-API — mit Kostenvoranschlag, Ablage unter `~/Medien/` und lokaler Galerie |
| [`schulung`](schulung/) | interaktive Lerneinheit als eine einzige HTML-Datei (Higgsfield + HyperFrames) |
| [`grill-me`](grill-me/) | löchert dich mit Fragen, bis ein Plan wirklich steht |
| [`vermenschlichen`](vermenschlichen/) | Schreibregeln für deutsche Texte, die nicht nach KI klingen — greift bei allem, was auf Deutsch geschrieben wird |

## Arbeiten mit Claude (englisch)

| Skill | wofür |
|---|---|
| [`writing-for-agents`](writing-for-agents/) | Anweisungen für Agenten schreiben — hilfreich, wenn du weitere Skills baust |
| [`research`](research/) | eine Frage gegen belastbare Primärquellen untersuchen |
| [`handoff`](handoff/) | ein Gespräch für einen anderen Agenten zusammenfassen |
| [`wait-what`](wait-what/) | „das kam nicht an" — Claude formuliert neu |
| [`writing-fragments`](writing-fragments/) | Rohmaterial für einen Text zusammentragen, noch ohne Gliederung |
| [`writing-shape`](writing-shape/) | aus dem Rohmaterial Absatz für Absatz einen Text formen |
| [`writing-beats`](writing-beats/) | denselben Stoff stattdessen als Abfolge von Beats bauen |
| [`to-questionnaire`](to-questionnaire/) | eine offene Entscheidung als Fragebogen an andere geben |
| [`prototype`](prototype/) | Wegwerf-Prototyp, um eine Entwurfsfrage zu beantworten |
| [`wizard`](wizard/) | interaktiver bash-Assistent für Schritte, die nur ein Mensch tun kann |
| [`diagnosing-bugs`](diagnosing-bugs/) | Fehlersuche bei hartnäckigen Bugs |
| [`resolving-merge-conflicts`](resolving-merge-conflicts/) | Merge- und Rebase-Konflikte auflösen |
| [`git-guardrails-claude-code`](git-guardrails-claude-code/) | Hooks, die gefährliche git-Befehle blockieren |
| [`setup-pre-commit`](setup-pre-commit/) | Husky, lint-staged und Prettier in einem JS/TS-Projekt einrichten |
| [`tdd`](tdd/) | testgetriebene Entwicklung |
| [`security-audit`](security-audit/) | Codebasis auf ausnutzbare Sicherheitslücken prüfen |
| [`watch`](watch/) | ein Video ansehen und Fragen dazu beantworten (braucht `yt-dlp` und `ffmpeg`) |

Die drei `writing-*`-Skills gehören zusammen: erst `writing-fragments` (Material sammeln),
dann entweder `writing-shape` (Absatz für Absatz) oder `writing-beats` (als Beats). Sie sind
im Quell-Repo als Beta markiert und deshalb hier fest einkopiert. Für die Frage, wie der
fertige deutsche Satz klingt, bleibt [`vermenschlichen`](vermenschlichen/) zuständig.

## Marketing (englisch)

Zwölf Skills aus [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
(MIT). Sie sind auf Englisch — Claude antwortet dir trotzdem auf Deutsch.

| Skill | wofür |
|---|---|
| [`product-marketing`](product-marketing/) | **zuerst anwenden** — legt `.agents/product-marketing.md` an, das alle anderen lesen |
| [`offers`](offers/) | Angebote und Pakete gestalten, Garantien, Bonusaufbau |
| [`lead-magnets`](lead-magnets/) | Leitfäden und Downloads zur Adressgewinnung |
| [`cro`](cro/) | Conversion auf Seiten und in Formularen |
| [`customer-research`](customer-research/) | Kundenforschung führen und auswerten |
| [`content-strategy`](content-strategy/) | entscheiden, welche Inhalte entstehen sollen |
| [`emails`](emails/) | Sequenzen, Willkommensstrecken, automatisierte Strecken |
| [`marketing-psychology`](marketing-psychology/) | psychologische Prinzipien und Denkmodelle |
| [`launch`](launch/) | Produkt- und Buchveröffentlichungen planen |
| [`site-architecture`](site-architecture/) | Seitenhierarchie, Navigation, URL-Struktur |
| [`referrals`](referrals/) | Empfehlungs- und Partnerprogramme |
| [`community-marketing`](community-marketing/) | Gruppen und Gemeinschaften aufbauen |

**Fang mit `product-marketing` an.** Der Skill legt einmalig `.agents/product-marketing.md`
im Projekt an — Zielgruppe, Positionierung, Angebot. Alle anderen lesen die Datei, statt dich
jedes Mal dasselbe zu fragen.

Das Verzeichnis [`../tools/`](../tools/) im Repo-Wurzelverzeichnis gehört dazu — mehrere
dieser Skills verlinken dorthin.

## Woher die fremden Skills stammen

Alles, was nicht von uns ist, steht mit Quelle, übernommenem Stand und meinen Abweichungen
in [`HERKUNFT.md`](HERKUNFT.md). Die Lizenztexte liegen in [`lizenzen/`](lizenzen/).

## HyperFrames

Die 19 HyperFrames-Skills (Motion Graphics, Videoschnitt) sind bewusst **nicht** hier
einkopiert — sie bringen einen eigenen Installer mit, der sie aktuell hält:

```bash
npx skills add heygen-com/hyperframes            # Kernsatz, interaktive Auswahl
npx skills add heygen-com/hyperframes --all --full-depth   # alle 19
```

Braucht Node 22+ und ffmpeg. Der [`schulung`](schulung/)-Skill setzt sie voraus.

## Installieren

```bash
bash skills/installieren.sh
```

Das legt für jeden Skill einen Symlink unter `~/.claude/skills/` an. Von da an gilt er in
jedem Projekt. Weil es Symlinks sind, wirkt jedes spätere `git pull` sofort — kein zweites
Installieren nötig. Danach Claude Code einmal neu starten.

Ein bereits vorhandener echter Ordner unter `~/.claude/skills/` wird nie überschrieben,
sondern gemeldet und übersprungen.

Im selben Lauf wird [`vorgaben.md`](vorgaben.md) nach `~/.claude/CLAUDE.md` verlinkt — die
stehenden Anweisungen, die Claude in **jeder** Sitzung mitliest (etwa: Bilder und Videos
immer über kie.ai). Liegt dort schon eine echte Datei, bleibt sie unangetastet; der Installer
nennt dann die Zeile, mit der man die Vorgaben von Hand einbindet:

```text
@~/Skills/skills/vorgaben.md
```

## Für media-skill: den Schlüssel setzen

```bash
export KIE_API_KEY='dein-schluessel'
```

Dauerhaft in `~/.zshrc` (macOS) bzw. `~/.bashrc` (Linux) eintragen. Der Schlüssel kommt immer
aus der Umgebungsvariable — er gehört nicht in eine Datei im Repo.

Schnellprobe, ohne Guthaben zu verbrauchen:

```bash
python3 skills/media-skill/scripts/kie.py preis --modell gpt-image-2-text-to-image --aufloesung 2k
python3 skills/media-skill/scripts/kie.py guthaben
```

## Global nutzen

Die Skills sollen überall gelten, nicht nur in diesem Repo. Je nachdem, wo Claude läuft,
führt ein anderer Weg dahin.

### Lokal — jedes Projekt auf dem eigenen Rechner

Einmal klonen, einmal installieren:

```bash
git clone https://github.com/vanlifemum-boop/Skills.git ~/Skills
bash ~/Skills/skills/installieren.sh
```

Das ist der oben beschriebene Symlink-Weg; `git pull` reicht danach für Aktualisierungen.
Den `KIE_API_KEY` dazu in `~/.zshrc` bzw. `~/.bashrc` setzen.

### Cloud-Sitzungen — claude.ai/code, Handy, App

Eine Cloud-Sitzung sieht nur die Skills aus dem Repo, das gerade ausgecheckt ist. Der
`media-skill` taucht dort also nur auf, wenn die Sitzung ausgerechnet in diesem Repo läuft.

Damit er in **jedem** Repo verfügbar ist, gehört dieses Skript in das Feld **Setup-Skript**
der Cloud-Umgebung. Es läuft bei jedem Sitzungsstart, bevor Claude Code startet:

```bash
#!/bin/bash
set -euo pipefail
[ -d "$HOME/.skills-repo" ] || git clone --depth 1 \
  https://github.com/vanlifemum-boop/Skills.git "$HOME/.skills-repo"
bash "$HOME/.skills-repo/skills/installieren.sh"
```

Die Umgebung wird auf claude.ai/code über das Wolken-Symbol über dem Eingabefeld bearbeitet
— eine eigene Einstellungsseite dafür gibt es nicht. Dort gehören auch hin:

- **Netzwerkzugriff** auf `Benutzerdefiniert`, mit den Domains aus
  [`media-skill/SKILL.md`](media-skill/SKILL.md#freigegebene-domains) und gesetztem Häkchen
  „Auch Standardliste gängiger Paketmanager einschließen".
- **Umgebungsvariablen**: `KIE_API_KEY=…` als eigene Zeile. Achtung, das Feld ist kein
  Geheimnis-Speicher — der Wert ist für jeden sichtbar, der die Umgebung nutzt. Eine
  persönliche Umgebung dafür nehmen, keine geteilte.

Beim Start einer neuen Sitzung die passende Umgebung im Umschalter auswählen; laufende
Sitzungen behalten ihre alte Konfiguration.

### Normale Chats auf claude.ai

Dort läuft der `media-skill` **nicht**. Er setzt Claude Code voraus: Python-Skripte, Ablage
unter `~/Medien/`, Schlüssel aus der Umgebung. Für Chats führt der Weg über den
kie.ai-MCP-Server — Connector-Verkehr läuft über Anthropics Server und braucht die
Domain-Freigabe gar nicht erst.

## Einen weiteren Skill hinzufügen

1. Ordner anlegen: `skills/mein-skill/`
2. Darin `SKILL.md` mit Frontmatter — `name` muss dem Ordnernamen entsprechen:

   ```yaml
   ---
   name: mein-skill
   description: Wofür der Skill da ist und woran Claude erkennt, wann er greift.
   ---
   ```

3. `bash skills/installieren.sh` erneut laufen lassen.

Längere Nachschlagetexte gehören nach `references/`, ausführbare Helfer nach `scripts/` —
so wie bei `media-skill`. Das hält die `SKILL.md` kurz, denn sie wird bei jeder Sitzung
mitgelesen.
