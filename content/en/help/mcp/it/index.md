---
title: "MCP for IT + operations"
summary: "Deployment, network, certificates, logs, monitoring, troubleshooting"
---

## Target audience

Administrator or operations engineer. Tasks:

- Install + roll out ForgeIEC Studio on workstations
- Secure the network connection
- Manage identities + trust store
- Read logs, hook up monitoring
- Diagnose problems during operation

---

## Network

| Aspect | Value |
|---|---|
| Default port | 7531 (TCP) |
| Override via QSettings | `mcp/bind_port` |
| Bind address | `127.0.0.1` without inbound profile; `0.0.0.0` with |
| Endpoints | `/mcp/v1/info`, `/mcp/v1/manifest`, `/mcp/v1/rpc`, `/mcp/v1/events` |
| TLS | active for `0.0.0.0` bind, optional for `127.0.0.1` |
| Long-lived connections | SSE streams per active watch (on `/mcp/v1/events`) |

Firewall rules per workstation:

```
# inbound: 7531/tcp from defined peer IPs
iptables -A INPUT -p tcp --dport 7531 -s <peer-cidr> -j ACCEPT
iptables -A INPUT -p tcp --dport 7531 -j REJECT
```

---

## Certificates

### Server cert

| Path | Content |
|---|---|
| `~/.config/ForgeIEC/mcp/server.crt` | RSA-4096, SAN-bound, 10 years |
| `~/.config/ForgeIEC/mcp/server.key` | RSA-4096 private key, 600 |
| `~/.config/ForgeIEC/mcp/server.san` | SAN manifest (regenerates cert on change) |

Auto-generated on first server start. Regenerated when bind
address changes (RFC 6125 SAN compliance).

### Trust store (mTLS mode)

| Path | Content |
|---|---|
| `~/.config/ForgeIEC/mcp/trust/*.pem` | Team-CA cert(s) — as trust anchors |
| `~/.config/ForgeIEC/mcp/trust/peers.toml` | signed member list |
| `~/.config/ForgeIEC/mcp/trust/revoked.toml` | signed revocation list |

Hot-reload on drop/modify of these files (QFileSystemWatcher,
200 ms debounce).

### Caretaker CA (only when Caretaker role is active)

| Path | Content |
|---|---|
| `~/.config/ForgeIEC/mcp/ca-team/ca.crt` | Team-CA cert |
| `~/.config/ForgeIEC/mcp/ca-team/ca.key` | Team-CA private key, 600 |

Backup-relevant. Loss = team can no longer issue new members or
revoke existing ones.

---

## Identities + tokens

| Source | Content |
|---|---|
| Bearer token per profile | QSettings `mcp/profiles/<name>/bearer_token` |
| Inbound allow-list | QSettings `mcp/profiles/<name>/accepts_inbound_mcp` |
| Member cert | Caretaker-signed cert in `peers.toml` |

Token rotation:

1. `Preferences → AI → Profile`, regenerate token
2. Distribute the new token to clients
3. Restart Studio

---

## Log files

| Path | Format | Rotation |
|---|---|---|
| `~/.config/ForgeIEC/mcp_audit.log` | JSONL append-only | none (manual trim if needed) |
| `journalctl -u anvild` | systemd journal | systemd defaults |
| `journalctl -u bellowsd` | systemd journal | systemd defaults |
| Studio logs | stderr + `editor.recent_logs` MCP tool (500-entry ring) | volatile |

### Audit log format

One JSON object per line:

```json
{"ts":"2026-05-12T20:13:05Z",
 "tool":"project.write.add_variable",
 "args":{"name":"LED_00","iec_type":"BOOL","address":"%MX0.0"},
 "choice":"yes",
 "caller":"local"}
```

Recommended consumption: `jq` or Loki/Promtail with JSON parser.

---

## Backup

| File / directory | Category |
|---|---|
| `~/.config/ForgeIEC/mcp/ca-team/` | **critical** (Caretaker workstation) |
| `~/.config/ForgeIEC/mcp/trust/` | important (trust store + roster) |
| `~/.config/ForgeIEC/mcp/server.key` | regeneratable (auto on start) |
| `~/.config/ForgeIEC/mcp_audit.log` | depends on compliance requirement |
| `/var/lib/anvil/` | contains project store + config |
| `/etc/forgeiec/bellows/` | bellowsd config |

Caretaker workstation: `ca-team/ca.key` is the only
non-regeneratable file. Loss = Team-CA recovery required.

---

## Monitoring

### Health check

```bash
curl -k -s -H "Authorization: Bearer $TOKEN" \
     https://forgeiec-ws.local:7531/mcp/v1/info
```

200 OK + JSON body → server alive. Extended check via the
`server_info` tool:

```bash
curl -k -s -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     https://forgeiec-ws.local:7531/mcp/v1/rpc \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
          "params":{"name":"server_info","arguments":{}}}' \
     | jq -r '.result.content[0].text | fromjson'
```

Returns, among others:

| Field | Use in monitoring |
|---|---|
| `editor_build.build_time` | drift from expected version |
| `editor_build.git_dirty` | should be false in production |
| `editor_build.mcp_override_securities` | should be false in production |
| `mtls_active` | trust store loaded? |
| `trust_store_size` | number of Team-CAs |
| `has_project` | has a project open |
| `tls_active` | TLS active |

### anvild health

```bash
systemctl is-active anvild
systemctl is-active bellowsd
```

### Variable monitor

Per variable + stream subscription the watch traffic rises. Via
`monitor.is_running`:

```json
{ "connected": true, "watch_active": true, "host": "localhost",
  "user": "admin", "authenticated": true }
```

Prometheus/Grafana integration: cron-poll `server_info` +
`monitor.is_running`, write into textfile collector.

---

## Troubleshooting

### MCP server doesn't respond

| Symptom | Diagnosis |
|---|---|
| Connection refused | Studio not running or different port — `ss -tlnp` |
| TLS handshake failed | server cert expired or hostname mismatch — regenerate cert (bind address change triggers it automatically) |
| 401 Unauthorized | token wrong or profile disabled — check Preferences |
| FORGE_ERR_NO_PROJECT | project not open — call `project.open` first |

### Variable "sticks"

See [FAQ](/help/faq/stuck-variables-shm/). Stale iceoryx2 SHM. Fix:
`systemctl restart anvild` (since v0.1.0+ auto cleanup at startup).

### Build mismatch

If `server_info.editor_build.mcp_override_securities=true` on a
productive workstation: Studio is installed with the override
version. Security risk. Fix:

```bash
sudo apt install --reinstall forgeiec-studio
sudo systemctl restart anvild
```

### Deploy fails

`codegen.deploy_status.build_log_tail` returns the last 16 KB of
g++ stderr. If `Auto-start failed: Runtime binary not found`:

```bash
journalctl -u anvild -n 50 --no-pager
```

Typically: missing C toolchain on the PLC target, or disk full.

### Audit log grows unbounded

```bash
# Manual rotation
mv ~/.config/ForgeIEC/mcp_audit.log \
   ~/.config/ForgeIEC/mcp_audit.log.$(date +%Y%m%d)
# Studio re-creates the file on the next write event
```

Logrotate config:

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

## Deployment patterns

### Single workstation

Default. Studio + anvild + bellowsd on one host. Bind 127.0.0.1.
No trust store. Bearer optional.

### Team setup (multiple workstations)

Per workstation: Studio + local anvild. Trust store shared (USB,
Git repo, shared drive).

One workstation is Caretaker. Others are members.

peers.toml + revoked.toml maintained centrally, distributed
signed.

### Build server setup

Headless workstation without GUI uses CLI / MCP for the build
pipeline:

```
ForgeIEC Studio (headless --no-gui) --mcp-bind 0.0.0.0:7531
   ↓ bearer auth
CI runner (curl + jq)
   ↓ calls project.open, codegen.compile, codegen.deploy
PLC target
```

Benefits: central build logs, same build environment, no
workstation drift.

---

## Next

- [MCP protocol for application engineers](/help/mcp/programmers/)
- [Architecture + security engineering](/help/ai/architecture/)
- [FAQ](/help/faq/)
- [Back to the MCP overview](/help/mcp/)
