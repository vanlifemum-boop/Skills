# MCP-Server in diesem Projekt

Die Datei `.mcp.json` im Repo-Root definiert die MCP-Server, die Claude Code in
diesem Projekt automatisch startet. Weil sie eingecheckt ist, gilt sie in jeder
Session — auch in frisch geklonten Remote-Containern.

`.claude/settings.json` setzt `enableAllProjectMcpServers: true`. Ohne das
müsste jede neue Session die Server aus `.mcp.json` erst manuell freigeben.

## kie-ai

Bildgenerierung, Video, TTS über kie.ai (Flux, Midjourney, Kling, Seedance,
ElevenLabs u. a.).

Der Server braucht die Umgebungsvariable `KIE_AI_API_KEY` — ohne sie bricht er
beim Start ab. Der Key steht bewusst **nicht** in `.mcp.json`; dort steht nur
die Referenz `${KIE_AI_API_KEY}`, die Claude Code beim Start aus der Umgebung
auflöst.

Den Key hinterlegst du einmalig als Umgebungsvariable deiner Claude-Code-
Umgebung (claude.ai/code → Environments → Environment variables). Danach ist er
in jeder Session dieses Repos verfügbar.

Key erhältlich unter https://kie.ai → API Keys.

## Prüfen, ob es läuft

```
claude -p "ok" --output-format stream-json --verbose | grep -o '"mcp_servers":\[[^]]*\]'
```

Erwartete Ausgabe: `"mcp_servers":[{"name":"kie-ai","status":"connected"}]`

`claude mcp list` ist hier kein verlässlicher Test — der Befehl wertet
`enableAllProjectMcpServers` nicht aus und meldet trotz funktionierender
Konfiguration "Pending approval".
