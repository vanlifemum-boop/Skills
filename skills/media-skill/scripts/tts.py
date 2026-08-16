#!/usr/bin/env python3
"""tts.py — spricht den Sprechtext des Reels über kie.ai ein.

Zwei Gründe, warum das nicht `kie.py erzeugen` macht:

1. `google/gemini-2-5-pro-tts` nimmt kein `prompt`. Es verlangt `speakers` und
   `dialogue_turns` in einer festen Form — `kie.py` schickt aber `prompt` und
   bekommt dafür nacheinander 422 „speakers … / speaker_id … / voice_name …".
2. Die fertige Datei liegt auf `tempfile.aiquickdraw.com`; dieser Host antwortet
   hinter dem Agenten-Proxy auf Pythons urllib mit HTTP 403, auf curl mit 200.

Die richtige Form, Feld für Feld erfragt:

    {"language": "de-DE",
     "speakers": [{"speaker_id": "Speaker 1", "voice_name": "Sulafat"}],
     "dialogue_turns": [{"speaker_id": "Speaker 1", "text": "…"}]}

`speaker_id` muss wörtlich „Speaker N" heißen — ein Name wie „Erzählerin" wird
abgelehnt. Und es bleibt bei **einem einzigen** Turn mit dem ganzen Text: mehrere
Turns schneidet das Modell nach rund neun Sekunden kommentarlos ab.

    python3 tts.py --projekt 244-tage
    python3 tts.py --projekt 244-tage --stimme Achernar
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kie  # noqa: E402

from veo import _mit_curl_holen  # noqa: E402

kie._datei_holen = _mit_curl_holen

# Ein Text, Absätze durch Leerzeilen — daraus wird genau ein dialogue_turn.
TEXT = """Vor 244 Tagen holten zwei Frauen mein Kind. Er durfte mitnehmen, was er tragen konnte: seinen Teddy und drei Bücher.

Seitdem zähle ich. 244 Tage, in denen ein Platz in meinem Leben leer geblieben ist. Mein Kind wächst weiter — und ich verpasse Momente, die ich niemals zurückbekomme.

Ich will keine Tage mehr zählen. Ich will einfach nur wieder Mama sein. 244 Tage sind genug."""


def main():
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("--projekt", default="244-tage")
    zerleger.add_argument("--text", default=TEXT)
    zerleger.add_argument("--sprache", default="de-DE")
    zerleger.add_argument("--stimme", default="Sulafat",
                          help="Gemini-Stimme, z. B. Sulafat (warm), Achernar (weich), Leda")
    args = zerleger.parse_args()

    try:
        geschaetzt, erklaerung = kie.kosten(
            "google/gemini-2-5-pro-tts", sekunden=len(args.text) / 15
        )
        print(f"google/gemini-2-5-pro-tts: {erklaerung} = "
              f"{kie.zahl(geschaetzt)} Credits · "
              f"{kie.euro(geschaetzt * kie.EUR_JE_CREDIT)} € (geschätzt)")

        task_id = kie.auftrag_anlegen("google/gemini-2-5-pro-tts", {
            "language": args.sprache,
            "speakers": [{"speaker_id": "Speaker 1", "voice_name": args.stimme}],
            "dialogue_turns": [{"speaker_id": "Speaker 1", "text": args.text}],
        })
        print(f"  Auftrag {task_id} angelegt.")
        urls, verbraucht = kie.auf_ergebnis_warten(task_id)

        credits = verbraucht if verbraucht is not None else geschaetzt
        ordner = kie.zielordner(args.projekt)
        kie.herunterladen_und_protokollieren(
            urls, ordner, "google/gemini-2-5-pro-tts", args.text, "audio", credits
        )
        print(f"Abgerechnet: {kie.zahl(float(credits))} Credits · "
              f"{kie.euro(float(credits) * kie.EUR_JE_CREDIT)} €")
        return 0
    except kie.Abbruch as fehler:
        print(f"Fehler: {fehler}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
