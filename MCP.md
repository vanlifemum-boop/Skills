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

Den Key hinterlegst du einmalig als Umgebungsvariable deiner Cloud-Umgebung:
auf claude.ai/code das Wolken-Symbol in der Zeile über dem Eingabefeld
antippen (einen direkten Link oder eine Einstellungsseite dafür gibt es
nicht), bei der Umgebung das Zahnrad wählen, im Feld **Environment
variables** eine Zeile `KIE_AI_API_KEY=dein_key` ergänzen, speichern.

Nicht zu verwechseln mit den Einstellungen der Claude-App (Profil,
Abrechnung, Konnektoren …) — dort gibt es die Umgebungsauswahl nicht. Sie
sitzt ausschließlich in der Code-Oberfläche über dem Eingabefeld.

Die Werte werden einmalig beim Session-Start kopiert — laufende Sessions
behalten ihre alten Werte, die Änderung greift erst in der nächsten Session.

**Zur Vorsicht:** Cloud-Umgebungen haben keinen Secrets-Store. Die Doku rät
deshalb generell davon ab, API-Keys dort abzulegen, weil jeder, der die
Umgebung nutzt, die Werte lesen kann. Bei einer rein persönlichen Umgebung
ist das der eigene Account, und eine Alternative gibt es derzeit nicht. Zwei
Konsequenzen: die Umgebung nicht mit anderen teilen, und beim Teilen von
Sessions daran denken, dass der Key im Session-Verlauf auftauchen kann.

Der Key gehört auf keinen Fall in `.mcp.json` — dieses Repo ist öffentlich.

Key erhältlich unter https://kie.ai → API Keys.

### Netzwerkfreigabe (zwingend)

Der Key allein reicht nicht. Cloud-Sessions laufen standardmäßig mit der
Zugriffsstufe **Trusted**, die nur eine feste Allowlist erlaubt (Paket-
Registries, GitHub, Cloud-SDKs). `api.kie.ai` steht dort nicht drauf, und der
Proxy blockt die Verbindung, bevor sie kie.ai überhaupt erreicht:

```
curl: (56) CONNECT tunnel failed, response 403
```

Der MCP-Server meldet das als `HTTP 403: The provider returned an invalid
response` — das sieht nach einem ungültigen Key aus, ist aber die Netzsperre.

Im selben Umgebungsdialog **Network access** auf **Custom** stellen und unter
**Allowed domains** ergänzen:

```
api.kie.ai
*.kie.ai
```

Dabei **Also include default list of common package managers** ankreuzen,
sonst fällt die restliche Allowlist weg.

Falls das Herunterladen fertiger Bilder oder Videos danach immer noch
scheitert: kie.ai liefert die Dateien über einen eigenen CDN-Host. Den
Hostnamen aus der zurückgegebenen URL ablesen und ebenfalls eintragen.

## Prüfen, ob es läuft

```
claude -p "ok" --output-format stream-json --verbose | grep -o '"mcp_servers":\[[^]]*\]'
```

Erwartete Ausgabe: `"mcp_servers":[{"name":"kie-ai","status":"connected"}]`

`claude mcp list` ist hier kein verlässlicher Test — der Befehl wertet
`enableAllProjectMcpServers` nicht aus und meldet trotz funktionierender
Konfiguration "Pending approval".
