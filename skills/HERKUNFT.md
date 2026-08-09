# Herkunft der übernommenen Skills

Ein Teil der Skills hier stammt aus fremden Repos. Diese Datei hält fest, woher, in welchem
Stand und was ich beim Übernehmen verändert habe. Lizenztexte liegen in
[`lizenzen/`](lizenzen/).

Eigenentwicklungen sind `media-skill`, `schulung` und `grill-me` — sie tauchen hier nicht auf.

| Quelle | Lizenz | übernommener Stand |
|---|---|---|
| [LOGIN-TB/claude-skills](https://github.com/LOGIN-TB/claude-skills) | MIT, © 2026 LOGIN | `ff74380` |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT, © 2025 Corey Haines | `7868cb9` |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | MIT, © 2025–2026 Cloudflare | `8bac420` |
| [bradautomates/claude-video](https://github.com/bradautomates/claude-video) | MIT, © 2026 Bradley Bonanno | `83da59f` |
| [mattpocock/skills](https://github.com/mattpocock/skills) | MIT, © 2026 Matt Pocock | `84fdeff` |

Alle `SKILL.md` und `references/` sind **unverändert** übernommen. Was ich weggelassen habe,
steht jeweils darunter.

---

## LOGIN-TB/claude-skills

`vermenschlichen` — Schreibregeln für deutsche Texte, die nicht nach KI klingen.

Der einzige Skill des Repos, vollständig übernommen.

## coreyhaines31/marketingskills

Zwölf von 49: `product-marketing`, `offers`, `lead-magnets`, `cro`, `customer-research`,
`content-strategy`, `emails`, `marketing-psychology`, `launch`, `site-architecture`,
`referrals`, `community-marketing`.

**Fang mit `product-marketing` an** — er legt `.agents/product-marketing.md` an, das alle
anderen lesen, statt dich jedes Mal dasselbe zu fragen.

Weggelassen: die `evals/`-Ordner (Testdaten des Autors für seine eigene Skill-Entwicklung)
und 37 Skills zu Bezahlwerbung, Vertriebsbetrieb und App-Store.

Ebenfalls weggelassen sind die englischen Entsprechungen zu Themen, die du schon auf Deutsch
abdeckst. Wo im Text ein Verweis darauf steht, ist bei uns Folgendes gemeint:

| Verweis im Text | bei uns |
|---|---|
| `pricing` | `preisstrategie` |
| `copywriting` | `werbetexten` |
| `copy-editing` | `korrekturlesen` |
| `social` | `social-media-inhalte` |
| `seo-audit` | `seo-audit` (deutsche Fassung) |

Es sind reine „siehe auch"-Hinweise, keine harten Abhängigkeiten. `customer-research`
verweist zusätzlich auf `ads`, `competitors`, `marketing-plan`, `prospecting`,
`churn-prevention` und `cold-email` — die gibt es hier gar nicht.

Mehrere dieser Skills verlinken relativ auf `../../tools/`. Deshalb liegen Registry und
Integrations-Doku des Quell-Repos unter [`../tools/`](../tools/) im Wurzelverzeichnis; ohne
sie zeigten die Links ins Leere. Die JS-Wrapper aus `tools/clis/` braucht die Auswahl nicht.

## cloudflare/security-audit-skill

`security-audit` — sucht ausnutzbare Sicherheitslücken in einer Codebasis, mit Blick auf
echte Auswirkung statt auf theoretische Bedenken. Der einzige Skill des Repos.

Nicht zu verwechseln mit dem eingebauten `/security-review`, das nur die offenen Änderungen
eines Branches prüft. Dieser hier nimmt sich das ganze Projekt vor.

## bradautomates/claude-video

`watch` — sieht sich ein Video an (URL oder Datei) und beantwortet Fragen dazu. Lädt per
`yt-dlp`, zieht Einzelbilder per `ffmpeg` und holt das Transkript aus den Untertiteln.

**Voraussetzungen:** `yt-dlp` und `ffmpeg`. Fehlen Untertitel, weicht der Skill auf Whisper
aus und braucht dafür `OPENAI_API_KEY`.

Das Quell-Repo enthält zusätzlich Hooks; der Skill braucht sie nicht, sie sind draußen.

## mattpocock/skills

Elf von 35: `writing-for-agents`, `research`, `handoff`, `wait-what`, `diagnosing-bugs`,
`resolving-merge-conflicts`, `git-guardrails-claude-code`, `to-questionnaire`, `prototype`,
`tdd`, `wizard`.

`writing-for-agents` ist der nützlichste davon, wenn du weiter eigene Skills baust — er
beschreibt, wie man Anweisungen für Agenten schreibt.

Weggelassen:

- **`deprecated/` und `in-progress/`** — vom Autor selbst als überholt bzw. unfertig markiert.
- **Skills, die sein eigenes Setup brauchen:** `setup-matt-pocock-skills`, `ask-matt`,
  `migrate-to-shoehorn`, `to-spec`, `to-tickets`, `implement`, `triage` und `wayfinder` setzen
  seinen Issue-Tracker oder seine Werkzeuge voraus.
- **Dopplungen mit dem, was du schon hast:** `grill-me`, `grilling` und `grill-with-docs`
  (du hast `grill-mich`), `code-review` (eingebaut), `teach` (du hast `learn`).
- `codebase-design` und `domain-modeling`, weil sie auf `implement` aufbauen und tief in
  Software-Architektur gehen.

---

## Einen Skill nachziehen oder aktualisieren

```bash
git clone --depth 1 https://github.com/<quelle>.git /tmp/quelle
cp -r /tmp/quelle/skills/<name> skills/
rm -rf skills/<name>/evals          # nur bei marketingskills nötig
bash skills/installieren.sh
```

Danach hier den neuen Stand vermerken, damit der nächste Abgleich weiß, worauf er aufsetzt.
