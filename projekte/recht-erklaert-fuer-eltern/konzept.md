# Konzept – „Recht erklärt für Eltern“

## Ziel der Filmreihe

Eine neue Video-Reihe für **YouTube und Instagram** erklärt Eltern verständlich rechtliche Abläufe rund um familienrechtliche und jugendhilferechtliche Themen.

Der Schwerpunkt der ersten Folge lautet:

> **Wie funktioniert eine Inobhutnahme? Was muss das Jugendamt tun – und was passiert, wenn Fehler gemacht werden?**

Die Reihe soll komplexe rechtliche Themen verständlich, ruhig und strukturiert erklären. Mögliche Fehler und Rechtsfolgen sollen differenziert dargestellt werden.

---

# 1. Konzept der ersten Folge

## Arbeitstitel

**„Die Inobhutnahme – was muss passieren, was darf nicht passieren und was können Eltern tun?“**

## Geplanter Ablauf

1. Was ist eine Inobhutnahme?
2. Wann darf das Jugendamt ein Kind in Obhut nehmen?
3. Was muss vor beziehungsweise bei der Maßnahme geprüft werden?
4. Was muss den Eltern erklärt werden?
5. Welche Rechte haben Eltern?
6. Welche Rechte hat das Kind?
7. Was muss dokumentiert werden?
8. Was passiert, wenn Eltern der Maßnahme widersprechen?
9. Wann muss das Familiengericht eingeschaltet werden?
10. Typische mögliche Fehler und Versäumnisse
11. Was können Eltern konkret tun?
12. Unterlagen sichern und Vorgänge dokumentieren
13. Rechtliche Überprüfung und mögliche Rechtsmittel
14. Ausblick auf die nächste Folge

---

# 2. Technisches Konzept

Das System soll aus einem Skript automatisch einzelne Videoszenen vorbereiten und über eine konfigurierte Kie.ai-API-Anbindung zur Videogenerierung übergeben.

## Ablauf

```text
Skript eingeben
      ↓
Themen und Szenen strukturieren
      ↓
Für jede Szene einen Video-Prompt erzeugen
      ↓
Kie.ai-API aufrufen
      ↓
Videogenerierung starten
      ↓
Status der Generierung prüfen
      ↓
Videoszenen abrufen
      ↓
Untertitel und Sprechertext hinzufügen
      ↓
Szenen zusammensetzen
      ↓
YouTube-Version erstellen
      ↓
Instagram-Reels erstellen
```

---

# 3. Projektstruktur

```text
recht-erklaert-fuer-eltern/
│
├── config/
│   └── settings.json
│
├── scripts/
│   └── folge-01-inobhutnahme.json
│
├── prompts/
│   ├── system_prompt.txt
│   └── scene_prompts.py
│
├── generated/
│   ├── scenes/
│   ├── audio/
│   ├── subtitles/
│   └── final/
│
├── kie_client.py
├── video_generator.py
├── subtitle_generator.py
├── video_editor.py
└── main.py
```

---

# 4. Episodenstruktur als JSON

```json
{
  "series": "Recht erklärt für Eltern",
  "episode": 1,
  "title": "Wie funktioniert eine Inobhutnahme?",
  "scenes": [
    {
      "id": 1,
      "duration": 12,
      "speaker_text": "Eine Inobhutnahme ist eine vorläufige Maßnahme. Auch bei einer solchen Maßnahme müssen die gesetzlichen Voraussetzungen und Verfahrensregeln beachtet werden.",
      "visual_prompt": "Serious cinematic documentary scene, German family sitting in a living room, documents on a table, emotional but respectful atmosphere, realistic, no identifiable real persons",
      "format": "16:9"
    },
    {
      "id": 2,
      "duration": 15,
      "speaker_text": "Entscheidend ist: Welche Voraussetzungen lagen tatsächlich vor, was wurde geprüft und was wurde dokumentiert?",
      "visual_prompt": "Close-up of official documents, legal files, timeline appearing beside documents, serious documentary style, realistic",
      "format": "16:9"
    }
  ]
}
```

---

# 5. Beispiel für einen Kie.ai-Client

> **Hinweis:** Die konkrete API-URL, Authentifizierung, Parameter und Endpunkte müssen anhand der aktuellen Kie.ai-API-Dokumentation konfiguriert werden. Deshalb sind diese Werte nicht fest im Code hinterlegt.

```python
import os
import time
import requests


class KieAIClient:

    def __init__(self):
        self.api_key = os.getenv("KIE_AI_API_KEY")
        self.base_url = os.getenv("KIE_AI_BASE_URL")

        if not self.api_key:
            raise ValueError("KIE_AI_API_KEY fehlt.")

        if not self.base_url:
            raise ValueError("KIE_AI_BASE_URL fehlt.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_video(self, prompt, duration=10, aspect_ratio="16:9"):

        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio
        }

        response = requests.post(
            f"{self.base_url}/video/create",
            headers=self.headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        return response.json()

    def get_task_status(self, task_id):

        response = requests.get(
            f"{self.base_url}/video/status/{task_id}",
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()
        return response.json()

    def wait_for_video(self, task_id):

        while True:

            status = self.get_task_status(task_id)

            print("Aktueller Status:", status)

            if status.get("status") == "completed":
                return status

            if status.get("status") == "failed":
                raise RuntimeError(
                    "Die Videogenerierung ist fehlgeschlagen."
                )

            time.sleep(10)
```

---

# 6. Hauptprogramm

```python
import json
from kie_client import KieAIClient


def load_episode(path):

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_episode(episode_file):

    episode = load_episode(episode_file)

    client = KieAIClient()

    generated_videos = []

    for scene in episode["scenes"]:

        print(
            f"Generiere Szene {scene['id']}: "
            f"{scene['speaker_text']}"
        )

        result = client.create_video(
            prompt=scene["visual_prompt"],
            duration=scene["duration"],
            aspect_ratio=scene["format"]
        )

        task_id = result["task_id"]

        completed = client.wait_for_video(task_id)

        video_url = completed["video_url"]

        generated_videos.append({
            "scene_id": scene["id"],
            "video_url": video_url,
            "speaker_text": scene["speaker_text"]
        })

    return generated_videos


if __name__ == "__main__":

    videos = generate_episode(
        "scripts/folge-01-inobhutnahme.json"
    )

    print("\nFERTIG GENERIERT:\n")

    for video in videos:
        print(video)
```

---

# 7. Automatische Prompt-Erstellung

Damit alle Folgen visuell zusammenpassen, soll die Reihe eine einheitliche Bildsprache erhalten.

## Visueller Grundstil

- seriöser Dokumentarstil
- ruhig und verständlich
- respektvolle Darstellung von Familien
- keine identifizierbaren realen Personen
- keine Darstellung konkreter realer Mitarbeiter oder Behördenmitarbeiter
- deutsche Alltagsumgebung
- Akten, Dokumente, Gericht und Familie als visuelle Elemente
- klare Einblendungen für rechtliche Begriffe
- wiederkehrende fiktive Moderationsfigur möglich

## Beispiel

```python
SERIES_STYLE = """
Serious German legal documentary.
Educational and factual.
Cinematic realistic style.
Respectful depiction of families.
No identifiable real persons.
No depiction of specific real authorities or employees.
Clear visual storytelling.
Professional documentary lighting.
"""


def create_scene_prompt(scene):

    return f"""
    {SERIES_STYLE}

    Scene topic:
    {scene['topic']}

    Narration:
    {scene['speaker_text']}

    Visual instruction:
    {scene['visual_description']}

    Important:
    The scene must support an educational legal explanation.
    Do not invent legal facts through visuals.
    """
```

---

# 8. Zwei Videoformate

## YouTube

```text
Format: 1920 × 1080
Seitenverhältnis: 16:9
Längere Erklärung
Kapitelstruktur
Untertitel
```

## Instagram Reels

```text
Format: 1080 × 1920
Seitenverhältnis: 9:16
Kurze, klar abgegrenzte Themen
Große Untertitel
Ein Schwerpunkt pro Reel
```

---

# 9. Aus einer YouTube-Folge mehrere Instagram-Reels erstellen

## YouTube-Folge 1

**Wie funktioniert eine Inobhutnahme von Anfang bis Ende?**

## Mögliche Reels

1. Was ist eine Inobhutnahme?
2. Welche Voraussetzungen müssen geprüft werden?
3. Was müssen Eltern erfahren?
4. Was muss dokumentiert werden?
5. Was passiert bei Widerspruch?
6. Wann wird das Familiengericht wichtig?
7. Was tun, wenn Unterlagen oder Dokumentationen fehlen?
8. Welche ersten Schritte können Eltern nach einer Maßnahme prüfen?

---

# 10. Geplante Filmreihe

## RECHT ERKLÄRT FÜR ELTERN

### Folge 1
**Die Inobhutnahme – Ablauf und Voraussetzungen**

### Folge 2
**Die ersten 24 Stunden – was passiert jetzt?**

### Folge 3
**Widerspruch der Eltern – was muss dann passieren?**

### Folge 4
**Das Familiengericht – wann muss es eingeschaltet werden?**

### Folge 5
**Akteneinsicht – welche Unterlagen gibt es?**

### Folge 6
**Dokumentation – warum jeder Zeitpunkt wichtig ist**

### Folge 7
**Fehler im Verfahren – was kann ein Fehler rechtlich bedeuten?**

### Folge 8
**Beschwerde, Dienstaufsicht oder Gericht?**

### Folge 9
**Das familienpsychologische Gutachten verstehen**

### Folge 10
**Welche Rechte hat das Kind?**

### Folge 11
**Welche Rechte haben Eltern?**

### Folge 12
**Der Weg zur Rückführung**

---

# 11. Nächster Arbeitsschritt

Für Folge 1 wird ein vollständiges Skript entwickelt:

**„Die Inobhutnahme – was muss passieren, was darf nicht passieren und was können Eltern tun?“**

Das Skript soll Szene für Szene aufgebaut werden:

1. rechtliche Ausgangslage erklären
2. Ablauf verständlich darstellen
3. Pflichten und Verfahrensschritte erläutern
4. mögliche Fehler klar benennen
5. zwischen Fehlern und tatsächlichen Rechtsfolgen unterscheiden
6. konkrete Handlungsmöglichkeiten für Eltern erklären

Die fertige Folge kann anschließend in einzelne Videoszenen zerlegt und durch das Kie.ai-System automatisiert zur Generierung vorbereitet werden.

---

> **Nachtrag zum Umsetzungsstand.** Dieses Dokument ist das Ursprungskonzept und bleibt
> unverändert stehen. Zwei Punkte wurden bei der Umsetzung anders entschieden:
>
> - Der in Abschnitt 5 skizzierte `KieAIClient` wird nicht gebaut. Im Repo liegt unter
>   `skills/media-skill/scripts/kie.py` bereits ein Client für die echte kie.ai-API;
>   `scripts/folge.py` ruft ihn auf.
> - Die Projektstruktur aus Abschnitt 3 wurde zusammengezogen: eine Quelldatei je Folge
>   unter `folgen/`, aus der Skript, Prompts und Aufrufe erzeugt werden. Details in
>   `README.md`.
>
> Der Arbeitsschritt aus Abschnitt 11 — das vollständige Skript für Folge 1 — ist erledigt:
> `skript/folge-01-inobhutnahme.md`.
