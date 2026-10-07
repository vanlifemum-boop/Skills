# Prompts für neue Avatar-Posen mit Mimik

Für jedes Bild: das bisherige Avatar-Bild (`assets/avatar-sheet.png`) als **Referenz** anhängen,
dann **Basis + Variante** als einen Prompt einfügen. Ein Bild pro Pose, Hochformat 2:3, 2K.

Damit ich die Bilder sauber freistellen kann:
- reinweißer Hintergrund, keine Schatten auf dem Boden
- ganzer Körper von Kopf bis Schuh, nichts abgeschnitten, etwas Rand oben und unten
- gleiche Größe und Kamerahöhe wie im Referenzbild

Dateinamen beim Zurückschicken: `mimik-A.png` … `mimik-I.png`.

## Basis (immer vorne einfügen)

```
Use the attached reference image as the identity reference. Same woman, identical face and features: long wavy blonde hair, light makeup, red lipstick, red nail polish. Same outfit: black sleeveless high-neck midi pencil dress with gathered neckline, black strappy high-heel sandals. Full body from head to toe, standing, facing the camera, centered, same scale and camera height as the reference, generous margin above the head and below the shoes. Pure white background (#FFFFFF), soft even studio lighting, no floor shadow, no props, no text. Photorealistic, sharp focus, 2:3 portrait.
```

## Varianten

| Datei | Szene | Variante (hinter die Basis einfügen) |
|---|---|---|
| `mimik-A.png` | 04 · § 171 | `Expression: serious and urgent, no smile, lips closed, eyebrows slightly drawn together, direct eye contact. Pose: right index finger raised at shoulder height in a "this is important" gesture, other arm relaxed at her side.` |
| `mimik-B.png` | 06 · weitere Paragrafen | `Expression: calm, matter-of-fact, neutral mouth, no smile. Pose: one arm extended, open hand pointing toward the RIGHT edge of the image, body turned slightly to the right, head turned to the camera.` |
| `mimik-C.png` | 08 · Amt versagt (Anfang) | `Expression: serious and stern, no smile, lips pressed together, steady gaze. Pose: arms crossed in front of the chest, weight on one leg.` |
| `mimik-D.png` | 08 · Gerichtsfall | `Expression: visibly concerned and sad, no smile, eyebrows raised in the middle, slightly lowered gaze, compassionate. Pose: hands loosely clasped in front of the body at waist height, shoulders slightly lowered.` |
| `mimik-E.png` | 09 · Und andersherum? | `Expression: skeptical and questioning, one eyebrow raised, head tilted slightly, small doubtful pout, no smile. Pose: one hand on the hip, the other hand open at chest height, palm up, as if asking "really?"` |
| `mimik-F.png` | 10 · Was tun (sofort) | `Expression: determined and encouraging, confident closed-mouth smile, firm gaze. Pose: one arm extended, index finger pointing toward the RIGHT edge of the image, head turned to the camera.` |
| `mimik-G.png` | 11 · Was tun (Wege) | `Expression: determined and encouraging, confident closed-mouth smile, firm gaze. Pose: one arm extended, index finger pointing toward the LEFT edge of the image, head turned to the camera.` |
| `mimik-H.png` | 12 · Hilfe holen | `Expression: warm and compassionate, soft gentle smile, kind eyes. Pose: right hand placed flat on the heart, left arm relaxed at her side.` |
| `mimik-I.png` | 05 · „gröblich“ (Ende) | `Expression: relieved and reassuring, relaxed natural smile, eyebrows relaxed. Pose: both hands open in front of the body at waist height, palms slightly down in a calming "it's okay" gesture.` |

## Tipp

Wenn das Gesicht vom Original abweicht: dasselbe Bild mit „Keep the face exactly as in the
reference image, change only the expression.“ noch einmal erzeugen. Bei Zeige-Posen genau
auf die Richtung achten (RIGHT/LEFT = Bildrand aus Sicht des Betrachters).
