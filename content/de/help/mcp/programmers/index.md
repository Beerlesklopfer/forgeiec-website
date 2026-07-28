---
title: "MCP fuer Applikationsingenieure"
summary: "Wie der ForgeIEC-Studio-MCP-Server von aussen angesprochen wird — Aufruf, Auth, Beispiele"
---

## Zielpublikum

Sie sind Applikationsingenieur und wollen den MCP-Server von ForgeIEC
Studio **direkt aufrufen**, statt nur ueber den Chat-Reiter im Studio
selbst zu arbeiten. Typische Einsatzfaelle:

- Mit einem **kleinen Skript** (z.B. Shell, Python, PowerShell)
  wiederkehrende Aktionen automatisieren — etwa abends alle
  Projektdateien testkompilieren
- Eine **eigene Pruef-Routine** anstossen — z.B. nach jedem Deploy
  einen festen Diagnose-Loop fahren
- Ein anderes **Werkzeug** anbinden — z.B. ein Excel- oder
  Auswertungs-Programm das Live-Werte abholt
- Verstehen wie der Server intern reagiert wenn etwas **schief
  geht** und ein eigener Aufruf-Pfad gebraucht wird

Diese Seite gibt die Protokoll-Details + ablauffaehige Beispiele
mit `curl` (standard auf Linux + Windows).

---

## Protokoll-Lifecycle

MCP folgt strikt einem **3-Phasen-Lifecycle**:

```
1. initialize     →  Server stellt sich vor: protocolVersion,
                      serverInfo, capabilities, instructions
2. tools/list     →  Server liefert komplette Tool-Liste mit Schemas
3. tools/call     →  Client ruft ein Tool auf; Loop fuer alle weiteren
                      Calls
```

Spec: [https://modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification).

ForgeIEC implementiert Version **2025-03-26** + `capabilities.tools.
listChanged: true`.

---

## Endpunkte

Der ForgeIEC-MCP-Server hoert standardmaessig auf:

| Pfad | Methode | Zweck |
|---|---|---|
| `/mcp/v1/info` | GET | Health-Check (kein Auth noetig) |
| `/mcp/v1/manifest` | GET | Statisches Manifest (Spec-konform fuer Discovery) |
| `/mcp/v1/rpc` | POST | JSON-RPC 2.0 Wire-Endpoint |
| `/mcp/v1/events` | GET (SSE) | Server-Sent-Events fuer asynchrone Push-Updates (z.B. Live-Monitor-Stream) |

Default-Port: **7531** (siehe [IT-Seite](/help/mcp/it/) wenn Sie
das aendern muessen).

Lokal-only-Bind (`127.0.0.1`) wenn kein Profil mit `acceptsInboundMcp
= true` existiert; sonst `0.0.0.0` und Auth zwingend.

---

## Authentifizierung

ForgeIEC unterstuetzt **zwei Stufen**:

### Bearer-Token

Ein 256-bit Token pro Profil. Der Editor zeigt es im
`Preferences → AI → Profile → Bearer Token`-Feld. Setzen Sie es im
`Authorization`-Header:

```bash
curl -k https://forgeiec-ws.local:7531/mcp/v1/info \
     -H "Authorization: Bearer <ihr-token-hier>"
```

`-k` weil das Server-Cert selbst-signiert ist (siehe naechster
Abschnitt fuer Trust-Setup).

### mTLS (Mutual TLS, optional)

Wenn Sie ein Team-Setup haben (Caretaker hat Member-Certs ausgestellt),
koennen Sie statt Bearer mit einem Client-Cert anmelden:

```bash
curl https://forgeiec-ws.local:7531/mcp/v1/info \
     --cacert /pfad/zum/team-ca.pem \
     --cert   /pfad/zum/eigenen-cert.pem \
     --key    /pfad/zum/eigenen-cert.key
```

Der Server akzeptiert dann **entweder** Bearer **oder** Client-Cert.

---

## initialize-Aufruf

Erst die Server-Identitaet abrufen:

```bash
curl -sk -X POST https://forgeiec-ws.local:7531/mcp/v1/rpc \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-03-26",
      "clientInfo": { "name": "my-script", "version": "0.1" },
      "capabilities": {}
    }
  }'
```

Response (gekuerzt):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "serverInfo": { "name": "forgeiec-mcp", "version": "v1" },
    "capabilities": { "tools": { "listChanged": true } },
    "instructions": "ForgeIEC MCP server (v1) ..."
  }
}
```

`instructions` ist **wichtig**: Hier steht ForgeIEC's Sicherheits-
Modell, der empfohlene Diagnose-Loop und der Anti-Loop-Hint fuer
LLM-Clients. Wenn Sie einen Client schreiben, **leiten Sie das in
die System-Prompt-Schicht weiter**.

---

## Tool-Liste abrufen

```bash
curl -sk -X POST https://forgeiec-ws.local:7531/mcp/v1/rpc \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
  }'
```

Die Antwort enthaelt ca. 180 Tools, jedes mit:

```json
{
  "name": "project.summary",
  "description": "Returns project metadata...",
  "inputSchema": { "type": "object", "properties": {}, "required": [] }
}
```

Zur menschen-lesbaren Uebersicht ueber alle Tools rufen Sie
`forge.help` (gruppiert nach Familie) oder `forge.help_for(name)`
(detailliert pro Tool) auf — letzteres ist gedacht damit ein LLM
sich selbst weiterbilden kann ohne dass Sie ihn briefen muessen.

---

## Tool-Aufruf

Beispiel: `project.summary` (kein Input):

```bash
curl -sk -X POST https://forgeiec-ws.local:7531/mcp/v1/rpc \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", "id": 3, "method": "tools/call",
    "params": {
      "name": "project.summary",
      "arguments": {}
    }
  }'
```

Response-Struktur (MCP-Spec-konform):

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"ok\": true, \"data\": {\"project_name\": ..., \"pou_count\": ...}}"
      }
    ],
    "isError": false
  }
}
```

Der **inhaltliche Envelope** (im `text`-Feld als JSON-String):

```json
{
  "ok": true,
  "data": { ... },
  "audit": {
    "called_by": "...",
    "timestamp": "2026-05-12T20:13:05Z",
    "tool": "project.summary"
  }
}
```

Bei Fehler:

```json
{
  "ok": false,
  "error": "FORGE_ERR_NO_PROJECT",
  "message": "no project is open",
  "remediation": {
    "next_steps": ["project.open with path=..."],
    "rule": "..."
  }
}
```

Die `error`-Codes sind alle `FORGE_ERR_<KIND>` (nicht generische
HTTP-Codes) — siehe naechster Abschnitt.

---

## Confirmation State Machine

Schreibende Tools (`project.write.*`, `codegen.deploy`,
`runtime.stop`, `editor.quit`, …) returnen beim **ersten Aufruf**
typischerweise:

```json
{
  "ok": false,
  "error": "FORGE_ERR_CONFIRMATION_REQUIRED",
  "confirmation": {
    "id": "cfa63753-0878-47de-8c48-db9e81a7de6d",
    "question": "Add bellows.Bellows.LED_00 (iec_type=BOOL)?",
    "options": ["yes"],
    "context": { "tool": "project.write.add_variable", ... },
    "expires_ms": 1778616326671
  }
}
```

Ihr Client muss dann `editor.confirm` mit `id` + `choice` aufrufen:

```bash
curl -sk -X POST https://forgeiec-ws.local:7531/mcp/v1/rpc \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", "id": 4, "method": "tools/call",
    "params": {
      "name": "editor.confirm",
      "arguments": {
        "id": "cfa63753-0878-47de-8c48-db9e81a7de6d",
        "choice": "yes"
      }
    }
  }'
```

Die Response von `editor.confirm` ist das **Ergebnis des
urspruenglich aufgerufenen Tools** (das Tool wird auf der Server-
Seite resumed). Es bedeutet: Sie sehen jetzt das `add_variable`-
Result, nicht eine Confirm-Bestaetigung.

`choice = "cancel"` bricht ab → `FORGE_ERR_USER_CANCELED`.

Timeout: 5 Minuten Default; danach `choice = "timeout"`.

Pending-Confirmations koennen ueber `editor.pending_confirmations`
abgefragt werden — nuetzlich wenn Ihr Client die `id` verliert.

---

## Fehler-Klassen (FORGE_ERR_*)

Die wichtigsten:

| Code | Bedeutung |
|---|---|
| `FORGE_ERR_NO_PROJECT` | Kein Projekt geoeffnet |
| `FORGE_ERR_NOT_FOUND` | POU/Variable/Topic existiert nicht |
| `FORGE_ERR_ALREADY_EXISTS` | Doppelter Name |
| `FORGE_ERR_INVALID_INPUT` | Pflichtfeld fehlt oder Format falsch |
| `FORGE_ERR_PERMISSION_DENIED` | Write-Tool in Default-Build, oder mTLS-Cert nicht in peers.toml |
| `FORGE_ERR_CONFIRMATION_REQUIRED` | State-Machine wartet auf editor.confirm |
| `FORGE_ERR_USER_CANCELED` | Operator hat "cancel" gewaehlt |
| `FORGE_ERR_IN_PROGRESS` | Async-Operation (z.B. deploy) laeuft schon |
| `FORGE_ERR_TIMEOUT` | Wait-Limit ueberschritten (z.B. Oszi-Trigger) |
| `FORGE_ERR_BRIDGE_INVOKE_FAILED` | Interner Bug — bitte als Bug melden |

Jeder Error hat typischerweise ein `remediation.next_steps`-Feld
mit konkreten Vorschlaegen — werten Sie das in Ihrem Client aus
und zeigen Sie es dem Nutzer.

---

## Beispiel: end-to-end Knight-Rider mit curl

```bash
TOKEN="..."
URL="https://forgeiec-ws.local:7531/mcp/v1/rpc"
JQ_RESULT='.result.content[0].text|fromjson'

call() {
  curl -sk -X POST "$URL" \
       -H "Authorization: Bearer $TOKEN" \
       -H "Content-Type: application/json" \
       -d "$1" | jq -r "$JQ_RESULT"
}

# 1) Projekt-Identitaet
call '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"project.summary","arguments":{}}}'

# 2) Variable anlegen (returns FORGE_ERR_CONFIRMATION_REQUIRED)
call '{"jsonrpc":"2.0","id":2,"method":"tools/call",
       "params":{"name":"project.write.add_variable",
                 "arguments":{"name":"LED_00","iecType":"BOOL",
                              "scope_kind":"bellows",
                              "scope_name":"Bellows",
                              "address":"%MX0.0"}}}'
# → extrahieren Sie confirmation.id aus der Response

# 3) Bestaetigen
call '{"jsonrpc":"2.0","id":3,"method":"tools/call",
       "params":{"name":"editor.confirm",
                 "arguments":{"id":"<id-aus-2>","choice":"yes"}}}'
```

---

## SSE-Stream fuer Live-Werte

`monitor.subscribe` registriert einen Watch + returnt eine
`stream_id`. Der eigentliche Wert-Push laeuft ueber den SSE-
Endpoint `/mcp/v1/events`:

```bash
curl -sk -N -H "Authorization: Bearer $TOKEN" \
     "https://forgeiec-ws.local:7531/mcp/v1/events?stream_id=<id>"
```

Format: standard-konformer SSE, jede `data:`-Zeile ist ein JSON-
Update mit `{address, value, ts_us, forced}`.

Stoppen via `monitor.unsubscribe(stream_id)`.

---

## Eigene Tools dazu schreiben?

**Aktuell:** Das Tool-Set von ForgeIEC Studio ist **hartkodiert** —
es gibt **keine Plug-in-API** fuer User-defined Tools im Server-
Prozess. Wenn Sie eine Aktion brauchen die noch fehlt:

- **Schreiben Sie ein Issue** mit Use-Case
- **Fork + Pull-Request** ist explizit willkommen — die Tool-
  Registrierung ist in `editor/src/runtime/FMcpServer.cpp` an einer
  Stelle pro Familie (z.B. `registerProjectExtraTools`)
- **Alternativ ein zweiter MCP-Server** der ForgeIEC's MCP nutzt
  und seine eigene Tool-Liste anbietet (Aggregator-Pattern)

Eine echte Plug-in-API ist auf der Roadmap, hat aber noch keinen
Sprint.

---

## Weiter

- [IT-Sicht](/help/mcp/it/) — wie deployen + monitoren
- [Architektur-Tiefe](/help/ai/architecture/) — Spec-Details + Standards
- [Source-Repository](https://git.forgeiec.io/ForgeIEC/forgeiec-studio)
- [Zurueck zur MCP-Uebersicht](/help/mcp/)
