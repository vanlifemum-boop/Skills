# Skills

Claude-Code-Skills, die in **allen** Projekten gelten sollen. Jeder Skill ist ein eigener
Ordner mit einer `SKILL.md` darin — genau so erwartet Claude Code es.

| Skill | wofür |
|---|---|
| [`media-skill`](media-skill/) | Bilder, Videos und Sprache über die kie.ai-API — mit Kostenvoranschlag, Ablage unter `~/Medien/` und lokaler Galerie |
| [`schulung`](schulung/) | interaktive Lerneinheit als eine einzige HTML-Datei (Higgsfield + HyperFrames) |
| [`grill-me`](grill-me/) | löchert dich mit Fragen, bis ein Plan wirklich steht |
| [`vermenschlichen`](vermenschlichen/) | Schreibregeln für deutsche Texte, die nicht nach KI klingen — greift bei allem, was auf Deutsch geschrieben wird |

`vermenschlichen` ist übernommen aus [LOGIN-TB/claude-skills](https://github.com/LOGIN-TB/claude-skills)
(MIT). Herkunft und Abgleich mit der Quelle stehen in
[`vermenschlichen/HERKUNFT.md`](vermenschlichen/HERKUNFT.md).

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

Herkunft, was ich verändert habe und wie du weitere Skills nachziehst:
[`HERKUNFT-marketingskills.md`](HERKUNFT-marketingskills.md).
Das Verzeichnis [`../tools/`](../tools/) im Repo-Wurzelverzeichnis gehört dazu — mehrere
dieser Skills verlinken dorthin.

## Installieren

```bash
bash skills/installieren.sh
```

Das legt für jeden Skill einen Symlink unter `~/.claude/skills/` an. Von da an gilt er in
jedem Projekt. Weil es Symlinks sind, wirkt jedes spätere `git pull` sofort — kein zweites
Installieren nötig. Danach Claude Code einmal neu starten.

Ein bereits vorhandener echter Ordner unter `~/.claude/skills/` wird nie überschrieben,
sondern gemeldet und übersprungen.

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
