# Herkunft: die Marketing-Skills

Zwölf Skills aus [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills).

- Übernommener Stand: `7868cb9251fad80a73d26e488a5ad5f6c4a9f335`
- Lizenz: MIT, Copyright (c) 2025 Corey Haines — Volltext in [`LIZENZ-marketingskills`](LIZENZ-marketingskills)
- Sprache: Englisch (das Original ist nicht übersetzt)

## Was übernommen wurde

| Skill | wofür |
|---|---|
| `product-marketing` | **zuerst anwenden** — legt `.agents/product-marketing.md` an, das alle anderen lesen |
| `offers` | Angebote und Pakete gestalten, Garantien, Bonusaufbau |
| `lead-magnets` | Leitfäden und Downloads zur Adressgewinnung |
| `cro` | Conversion auf Seiten und in Formularen |
| `customer-research` | Kundenforschung führen und auswerten |
| `content-strategy` | entscheiden, welche Inhalte entstehen sollen |
| `emails` | Sequenzen, Willkommensstrecken, automatisierte Strecken |
| `marketing-psychology` | psychologische Prinzipien und Denkmodelle |
| `launch` | Produkt- und Buchveröffentlichungen planen |
| `site-architecture` | Seitenhierarchie, Navigation, URL-Struktur |
| `referrals` | Empfehlungs- und Partnerprogramme |
| `community-marketing` | Gruppen und Gemeinschaften aufbauen |

Die übrigen 37 Skills des Quell-Repos sind bewusst draußen geblieben — sie zielen auf
Bezahlwerbung, Vertriebsbetrieb, App-Store und ähnliche Felder. Nachziehen geht jederzeit,
siehe unten.

## Was ich verändert habe

Die `SKILL.md` und die `references/` sind **unverändert** übernommen. Entfernt habe ich nur
die `evals/`-Ordner: das sind die Testdaten des Autors für seine eigene Skill-Entwicklung,
sie haben im Einsatz keinen Nutzen.

Mitkopiert wurde `tools/` im Repo-Wurzelverzeichnis (Registry und Integrations-Doku), weil
mehrere Skills relativ dorthin verlinken. Ohne sie zeigten diese Links ins Leere. Die
JS-Wrapper unter `tools/clis/` des Quell-Repos brauchen die zwölf Skills nicht, sie fehlen
hier.

## Verweise, die woanders hinzeigen

Einige Skills verweisen auf Geschwister-Skills, die wir nicht übernommen haben, weil du das
Thema schon auf Deutsch abdeckst:

| Verweis im Text | bei uns |
|---|---|
| `pricing` | `preisstrategie` |
| `copywriting` | `werbetexten` |
| `copy-editing` | `korrekturlesen` |
| `social` | `social-media-inhalte` |
| `seo-audit` | `seo-audit` (deutsche Fassung) |

Es sind reine „siehe auch"-Hinweise, keine harten Abhängigkeiten — nichts bricht dadurch.
Vereinzelt steht ein relativer Link wie `../../pricing/SKILL.md` im Text, der ins Leere
zeigt; gemeint ist dann die deutsche Entsprechung.

`customer-research` verweist zusätzlich auf `ads`, `competitors`, `marketing-plan`,
`prospecting`, `churn-prevention` und `cold-email` — die gibt es hier gar nicht.

## Nachziehen oder aktualisieren

```bash
git clone --depth 1 https://github.com/coreyhaines31/marketingskills.git /tmp/ms
cp -r /tmp/ms/skills/<name> skills/          # weiteren Skill holen
rm -rf skills/<name>/evals                   # Testdaten des Autors raus
```

Wer lieber alle 49 mit automatischen Aktualisierungen will, nimmt den Plugin-Weg — die
Skills lägen dann allerdings außerhalb dieses Repos:

```
/plugin marketplace add coreyhaines31/marketingskills
```
