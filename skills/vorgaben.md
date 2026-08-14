# Persönliche Vorgaben

Diese Datei wird von `installieren.sh` nach `~/.claude/CLAUDE.md` verlinkt und gilt dann in
**allen** Projekten — lokal wie in Cloud-Sitzungen. Sie ist kein Skill, sondern stehende
Anweisung: Claude liest sie in jeder Sitzung mit. Deshalb kurz halten.

## Bilder und Videos

Bilder und Videos werden **immer über kie.ai** erzeugt — mit dem `media-skill`
(`skills/media-skill/`, Aufruf über `scripts/kie.py`). Das ist gesetzt, nicht zur Auswahl.

**Canva ist raus.** Nicht danach fragen, nicht vorschlagen, nicht als Alternative nennen.
Verlangt ein Canva-Connector eine Autorisierung, das einmal sachlich melden und
weiterarbeiten — keine Rückfrage daraus machen.

Fehlt `KIE_API_KEY` in der Umgebung: das sagen und anhalten, statt auf ein anderes Werkzeug
auszuweichen.
