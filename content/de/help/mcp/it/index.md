---
title: "MCP fuer IT + Betrieb"
summary: "Deployment, Netzwerk, Zertifikate, Logs, Monitoring, Troubleshooting"
---

## Zielpublikum

Administrator oder Betriebs-Verantwortliche. Aufgaben:

- ForgeIEC Studio auf Workstations installieren + ausrollen
- Netzwerk-Anbindung absichern
- Identitaeten + Trust-Store verwalten
- Logs auswerten, Monitoring anbinden
- Probleme im laufenden Betrieb diagnostizieren

---

## Netzwerk

| Aspekt | Wert |
|---|---|
| Default-Port | 7531 (TCP) |
| Override per QSettings | `mcp/bind_port` |
| Bind-Adresse | `127.0.0.1` ohne Inbound-Profile; `0.0.0.0` mit |
| Endpoints | `/mcp/v1/info`, `/mcp/v1/manifest`, `/mcp/v1/rpc`, `/mcp/v1/events` |
| TLS | aktiv bei `0.0.0.0`-Bind, optional bei `127.0.0.1` |
| Long-lived Connections | SSE-Streams pro aktivem Watch (auf `/mcp/v1/events`) |

Firewall-Regeln pro Workstation:

```
# eingehend: 7531/tcp von definierten Peer-IPs
iptables -A INPUT -p tcp --dport 7531 -s <peer-cidr> -j ACCEPT
iptables -A INPUT -p tcp --dport 7531 -j REJECT
```

---

## Zertifikate

### Server-Cert

| Pfad | Inhalt |
|---|---|
| `~/.config/ForgeIEC/mcp/server.crt` | RSA-4096, SAN-bound, 10 Jahre |
| `~/.config/ForgeIEC/mcp/server.key` | RSA-4096 Private Key, 600 |
| `~/.config/ForgeIEC/mcp/server.san` | SAN-Manifest (regeneriert Cert bei Aenderung) |

Auto-Generation beim ersten Server-Start. Regeneration bei
Bind-Adress-Aenderung (RFC-6125-SAN-Compliance).

### Trust-Store (mTLS-Modus)

| Pfad | Inhalt |
|---|---|
| `~/.config/ForgeIEC/mcp/trust/*.pem` | Team-CA-Cert(s) — als Trust-Anker |
| `~/.config/ForgeIEC/mcp/trust/peers.toml` | signierte Member-Liste |
| `~/.config/ForgeIEC/mcp/trust/revoked.toml` | signierte Revocations-Liste |

Hot-Reload beim Drop/Modify dieser Dateien (QFileSystemWatcher,
200 ms Debounce).

### Caretaker-CA (nur falls Caretaker-Rolle aktiv)

| Pfad | Inhalt |
|---|---|
| `~/.config/ForgeIEC/mcp/ca-team/ca.crt` | Team-CA-Cert |
| `~/.config/ForgeIEC/mcp/ca-team/ca.key` | Team-CA-Private-Key, 600 |

Backup-relevant. Verlust = Team kann keine neuen Member mehr
ausstellen + keine bestehenden mehr widerrufen.

---

## Identitaeten + Tokens

| Quelle | Inhalt |
|---|---|
| Bearer-Token pro Profil | QSettings `mcp/profiles/<name>/bearer_token` |
| Inbound-Allow-List | QSettings `mcp/profiles/<name>/accepts_inbound_mcp` |
| Member-Cert | von Caretaker signiertes Cert in `peers.toml` |

Token-Rotation:

1. `Preferences → AI → Profile`, Token regenerieren
2. Neuen Token an Clients ausgeben
3. Editor neustarten

---

## Log-Dateien

| Pfad | Format | Rotation |
|---|---|---|
| `~/.config/ForgeIEC/mcp_audit.log` | JSONL append-only | keine (manuelles Trim bei Bedarf) |
| `journalctl -u anvild` | systemd-Journal | systemd-Defaults |
| `journalctl -u bellowsd` | systemd-Journal | systemd-Defaults |
| Editor-Logs | stderr + `editor.recent_logs` MCP-Tool (500-Eintraege Ring) | flüchtig |

### Audit-Log-Format

JSON-Objekt pro Zeile:

```json
{"ts":"2026-05-12T20:13:05Z",
 "tool":"project.write.add_variable",
 "args":{"name":"LED_00","iec_type":"BOOL","address":"%MX0.0"},
 "choice":"yes",
 "caller":"local"}
```

Empfohlene Auswertung: `jq` oder Loki/Promtail mit JSON-Parser.

---

## Backup

| Datei/Verzeichnis | Kategorie |
|---|---|
| `~/.config/ForgeIEC/mcp/ca-team/` | **kritisch** (Caretaker-Workstation) |
| `~/.config/ForgeIEC/mcp/trust/` | wichtig (Trust-Store + Roster) |
| `~/.config/ForgeIEC/mcp/server.key` | regenerierbar (auto bei Start) |
| `~/.config/ForgeIEC/mcp_audit.log` | je nach Compliance-Anforderung |
| `/var/lib/anvil/` | enthaelt Projekt-Store + Config |
| `/etc/forgeiec/bellows/` | bellowsd-Konfig |

Caretaker-Workstation: `ca-team/ca.key` ist die einzige nicht-
regenerierbare Datei. Verlust = Team-CA-Recovery noetig.

---

## Monitoring

### Health-Check

```bash
curl -k -s -H "Authorization: Bearer $TOKEN" \
     https://forgeiec-ws.local:7531/mcp/v1/info
```

200 OK + JSON-Body → Server lebt. Erweiterter Check via `server_info`-Tool:

```bash
curl -k -s -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     https://forgeiec-ws.local:7531/mcp/v1/rpc \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
          "params":{"name":"server_info","arguments":{}}}' \
     | jq -r '.result.content[0].text | fromjson'
```

Liefert u.a.:

| Feld | Nutzung im Monitoring |
|---|---|
| `editor_build.build_time` | Drift zur erwarteten Version |
| `editor_build.git_dirty` | Sollte in Production false sein |
| `editor_build.mcp_override_securities` | Sollte in Production false sein |
| `mtls_active` | Trust-Store geladen? |
| `trust_store_size` | Anzahl Team-CAs |
| `has_project` | Hat ein Projekt offen |
| `tls_active` | TLS active |

### anvild Health

```bash
systemctl is-active anvild
systemctl is-active bellowsd
```

### Variable-Monitor

Pro Variable + Stream-Subscription steigt der Watch-Verkehr. Per
`monitor.is_running`:

```json
{ "connected": true, "watch_active": true, "host": "localhost",
  "user": "admin", "authenticated": true }
```

Anbindung an Prometheus/Grafana: per Cron-Skript `server_info` +
`monitor.is_running` abfragen, in textfile-collector schreiben.

---

## Troubleshooting

### MCP-Server reagiert nicht

| Symptom | Diagnose |
|---|---|
| Connection refused | Editor nicht gestartet oder anderer Port — `ss -tlnp` |
| TLS handshake failed | Server-Cert abgelaufen oder Hostname-Mismatch — Cert neu generieren (Bind-Adress-Aenderung triggert das auto) |
| 401 Unauthorized | Token falsch oder Profil deaktiviert — Preferences pruefen |
| FORGE_ERR_NO_PROJECT | Projekt nicht offen — `project.open` zuerst |

### Variable bleibt "haengen"

Siehe [FAQ](/help/faq/stuck-variables-shm/). Stale Anvil-SHM.
Fix: PLC-Runtime neu starten (`Stop` + `Start` bzw.
`Build → Compile and Upload`) — Anvil raeumt die Segmente toter
Nodes dabei selbst auf. SHM-Dateien nicht von Hand loeschen.

### Build-Mismatch

Wenn `server_info.editor_build.mcp_override_securities=true` auf
einer Produktiv-Workstation: Editor mit Override-Version
installiert. Sicherheits-Risiko. Korrektur:

```bash
sudo apt install --reinstall forgeiec-studio
sudo systemctl restart anvild
```

### Deploy schlaegt fehl

`codegen.deploy_status.build_log_tail` liefert den g++-stderr-Tail
(letzte 16 KB). Wenn `Auto-start failed: Runtime binary not found`:

```bash
journalctl -u anvild -n 50 --no-pager
```

In der Regel fehlende C-Toolchain auf dem PLC-Target oder
disk-full.

### Audit-Log waechst unbegrenzt

```bash
# Rotation manuell
mv ~/.config/ForgeIEC/mcp_audit.log \
   ~/.config/ForgeIEC/mcp_audit.log.$(date +%Y%m%d)
# Editor kreiert die Datei neu beim naechsten Schreib-Event
```

Logrotate-Config:

```
/home/*/.config/ForgeIEC/mcp_audit.log {
    weekly
    rotate 12
    compress
    missingok
    notifempty
    copytruncate
}
```

---

## Deployment-Pattern

### Single-Workstation

Default. Editor + anvild + bellowsd auf einem Host. Bind 127.0.0.1.
Kein Trust-Store. Bearer optional.

### Team-Setup (mehrere Workstations)

Pro Workstation: Editor + lokaler anvild. Trust-Store geteilt
(USB, Git-Repo, geteiltes Laufwerk).

Caretaker auf einer Workstation. Andere als Member.

Peers.toml + revoked.toml zentral pflegen, signiert verteilen.

### Build-Server-Setup

Headless-Workstation ohne GUI nutzt CLI / MCP zur Build-Pipeline:

```
ForgeIEC Studio (headless --no-gui) --mcp-bind 0.0.0.0:7531
   ↓ Bearer-Auth
CI-Runner (curl + jq)
   ↓ ruft project.open, codegen.compile, codegen.deploy
PLC-Target
```

Vorteile: zentrale Build-Logs, gleiche Build-Umgebung, kein
Workstation-Drift.

---

## Weiter

- [MCP-Protokoll fuer Applikationsingenieure](/help/mcp/programmers/)
- [Architektur + Sicherheits-Engineering](/help/ai/architecture/)
- [FAQ](/help/faq/)
- [Zurueck zur MCP-Uebersicht](/help/mcp/)
