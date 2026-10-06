#!/bin/bash
# Verlinkt in Cloud-Sitzungen alle Skills aus skills/ nach ~/.claude/skills,
# damit sie ohne Handarbeit verfügbar sind. Lokal passiert nichts — dort
# einmal selbst `bash skills/installieren.sh` ausführen.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Ausführliche Ausgabe nach stderr, damit sie nicht im Sitzungskontext landet.
bash "${CLAUDE_PROJECT_DIR:-$(pwd)}/skills/installieren.sh" >&2
