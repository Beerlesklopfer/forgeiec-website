---
title: "MCP for application engineers"
summary: "How to call the ForgeIEC Studio MCP server from outside — invocation, auth, examples"
---

## Target audience

You are an application engineer and want to call the MCP server of
ForgeIEC Studio **directly**, instead of working only through the
chat tab inside Studio itself. Typical use cases:

- Automate recurring actions with a **small script** (shell, Python,
  PowerShell) — e.g. test-compile all project files overnight
- Trigger your own **check routine** — e.g. run a fixed diagnostic
  loop after every deploy
- Connect another **tool** — e.g. an Excel sheet or analysis
  program that fetches live values
- Understand how the server reacts internally when something
  **goes wrong** and a custom call path is needed

This page gives the protocol details + runnable examples with
`curl` (standard on Linux + Windows).

---

## Protocol lifecycle

MCP follows a strict **3-phase lifecycle**:

```
1. initialize     →  Server introduces itself: protocolVersion,
                      serverInfo, capabilities, instructions
2. tools/list     →  Server returns full tool list with schemas
3. tools/call     →  Client calls a tool; loop for all further calls
```

Spec: [https://modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification).

ForgeIEC implements version **2025-03-26** + `capabilities.tools.
listChanged: true`.

---

## Endpoints

The ForgeIEC Studio MCP server listens by default on:

| Path | Method | Purpose |
|---|---|---|
| `/mcp/v1/info` | GET | Health check (no auth needed) |
| `/mcp/v1/manifest` | GET | Static manifest (spec-conformant for discovery) |
| `/mcp/v1/rpc` | POST | JSON-RPC 2.0 wire endpoint |
| `/mcp/v1/events` | GET (SSE) | Server-Sent Events for asynchronous push updates (e.g. live monitor stream) |

Default port: **7531** (see [IT page](/help/mcp/it/) if you need to
change it).

Local-only bind (`127.0.0.1`) when no profile with
`acceptsInboundMcp = true` exists; otherwise `0.0.0.0` and auth
mandatory.

---

## Authentication

ForgeIEC supports **two modes**:

### Bearer token

A 256-bit token per profile. Studio shows it in
`Preferences → AI → Profile → Bearer Token`. Set it in the
`Authorization` header:

```bash
curl -k https://forgeiec-ws.local:7531/mcp/v1/info \
     -H "Authorization: Bearer <your-token-here>"
```

`-k` because the server cert is self-signed (see next section for
trust setup).

### mTLS (mutual TLS, optional)

If you have a team setup (Caretaker has issued member certs), you
can authenticate with a client cert instead of bearer:

```bash
curl https://forgeiec-ws.local:7531/mcp/v1/info \
     --cacert /path/to/team-ca.pem \
     --cert   /path/to/your-cert.pem \
     --key    /path/to/your-cert.key
```

The server then accepts **either** bearer **or** client cert.

---

## initialize call

First retrieve the server identity:

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

Response (abbreviated):

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

`instructions` is **important**: it contains ForgeIEC's security
model, the recommended diagnostic loop, and the anti-loop hint for
LLM clients. When you write a client, **pass it through to the
system-prompt layer**.

---

## Fetching the tool list

```bash
curl -sk -X POST https://forgeiec-ws.local:7531/mcp/v1/rpc \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
  }'
```

The response contains ~180 tools, each with:

```json
{
  "name": "project.summary",
  "description": "Returns project metadata...",
  "inputSchema": { "type": "object", "properties": {}, "required": [] }
}
```

For a human-readable overview of all tools, call `forge.help`
(grouped by family) or `forge.help_for(name)` (detailed per tool)
— the latter is designed so an LLM can self-educate without you
having to brief it.

---

## Tool call

Example: `project.summary` (no input):

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

Response structure (MCP-spec-conformant):

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

The **payload envelope** (in the `text` field as a JSON string):

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

On error:

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

All error codes are `FORGE_ERR_<KIND>` (not generic HTTP codes) —
see next section.

---

## Confirmation State Machine

Write tools (`project.write.*`, `codegen.deploy`, `runtime.stop`,
`editor.quit`, …) typically return on the **first call**:

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

Your client must then call `editor.confirm` with `id` + `choice`:

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

The response from `editor.confirm` is the **result of the
originally called tool** (the tool is resumed on the server side).
That means: you now see the `add_variable` result, not just a
confirm acknowledgement.

`choice = "cancel"` aborts → `FORGE_ERR_USER_CANCELED`.

Timeout: 5 minutes default; afterwards `choice = "timeout"`.

Pending confirmations can be queried via
`editor.pending_confirmations` — useful when your client loses the
`id`.

---

## Error classes (FORGE_ERR_*)

The important ones:

| Code | Meaning |
|---|---|
| `FORGE_ERR_NO_PROJECT` | No project open |
| `FORGE_ERR_NOT_FOUND` | POU/variable/topic doesn't exist |
| `FORGE_ERR_ALREADY_EXISTS` | Duplicate name |
| `FORGE_ERR_INVALID_INPUT` | Required field missing or wrong format |
| `FORGE_ERR_PERMISSION_DENIED` | Write tool in default build, or mTLS cert not in peers.toml |
| `FORGE_ERR_CONFIRMATION_REQUIRED` | State machine waits for editor.confirm |
| `FORGE_ERR_USER_CANCELED` | Operator chose "cancel" |
| `FORGE_ERR_IN_PROGRESS` | Async operation (e.g. deploy) already running |
| `FORGE_ERR_TIMEOUT` | Wait limit exceeded (e.g. scope trigger) |
| `FORGE_ERR_BRIDGE_INVOKE_FAILED` | Internal bug — please report |

Every error typically has a `remediation.next_steps` field with
concrete suggestions — surface that in your client and show it to
the user.

---

## Example: end-to-end Knight Rider with curl

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

# 1) Project identity
call '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"project.summary","arguments":{}}}'

# 2) Create variable (returns FORGE_ERR_CONFIRMATION_REQUIRED)
call '{"jsonrpc":"2.0","id":2,"method":"tools/call",
       "params":{"name":"project.write.add_variable",
                 "arguments":{"name":"LED_00","iecType":"BOOL",
                              "scope_kind":"bellows",
                              "scope_name":"Bellows",
                              "address":"%MX0.0"}}}'
# → extract confirmation.id from the response

# 3) Confirm
call '{"jsonrpc":"2.0","id":3,"method":"tools/call",
       "params":{"name":"editor.confirm",
                 "arguments":{"id":"<id-from-2>","choice":"yes"}}}'
```

---

## SSE stream for live values

`monitor.subscribe` registers a watch + returns a `stream_id`. The
actual value push runs over the SSE endpoint `/mcp/v1/events`:

```bash
curl -sk -N -H "Authorization: Bearer $TOKEN" \
     "https://forgeiec-ws.local:7531/mcp/v1/events?stream_id=<id>"
```

Format: standard-conformant SSE; every `data:` line is a JSON
update with `{address, value, ts_us, forced}`.

Stop via `monitor.unsubscribe(stream_id)`.

---

## Adding your own tools?

**Currently:** the ForgeIEC Studio tool set is **hard-coded** —
there is **no plug-in API** for user-defined tools in the server
process. If you need an action that's missing:

- **Open an issue** with the use case
- **Fork + pull request** is explicitly welcome — tool registration
  is in `editor/src/runtime/FMcpServer.cpp` in one place per family
  (e.g. `registerProjectExtraTools`). For repo access, send us your
  SSH public key first
- **Alternatively a second MCP server** that uses ForgeIEC's MCP
  and exposes its own tool list (aggregator pattern)

A real plug-in API is on the roadmap but has no sprint yet.

---

## Next

- [IT view](/help/mcp/it/) — how to deploy + monitor
- [Architecture deep-dive](/help/ai/architecture/) — spec details + standards
- Source repository: `ForgeIEC/forgeiec-studio` in the Forgejo —
  access once your SSH public key is enabled
- [Back to the MCP overview](/help/mcp/)
