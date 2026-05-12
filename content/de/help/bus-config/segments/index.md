---
title: "Bus-Segmente"
summary: "Felder pro Segment, Bridge-Lifecycle, protokoll-spezifische Settings"
---

{{< components "studio,tongs,anvild" >}}

## Was ist ein Segment?

Ein **Bus-Segment** ist **ein physisches Netzwerk auf einer
Schnittstelle des PLC-Targets** — Ethernet-Port (`eth0`,
`enp3s0`) fuer Modbus TCP / EtherCAT / EtherNet-IP, serieller Port
(`/dev/ttyUSB0`) fuer Modbus RTU / Profibus DP.

Pro Segment startet `anvild` **genau einen Bridge-Daemon**
(`tongs-modbustcp`, `tongs-ethercat`, ...). Dieser handhabt den
Verkehr zu allen Devices im Segment.

Ein Projekt kann beliebig viele Segmente halten — jedes mit
eigenem Protokoll, Schnittstelle und Polling-Takt. Eine schnelle
EtherCAT-Achssteuerung (`eth1`, 1 ms) + eine langsame Modbus-TCP-
Sensorerfassung (`eth0`, 100 ms) laufen parallel im gleichen
Projekt.

---

## Felder eines Segments

Die Struct-Definition liegt in
`editor/include/model/FBusSegmentConfig.h`. Persistiert wird ein
Segment im `.forge`-Projekt als `<fi:segment>` unter
`<fi:busConfig>` (siehe [Bus-Konfiguration](../)).

### Identitaet + Protokoll

| Feld | Typ | Bedeutung |
|---|---|---|
| `segmentId` | UUID | Stabiler Primaerschluessel — automatisch beim Anlegen, nicht editierbar. Ueberlebt Rename, Protokoll-Wechsel, IP-Aenderung. |
| `protocol` | Enum | `modbustcp` / `modbusrtu` / `ethercat` / `profibus` / `ethernetip`. Bestimmt welcher Bridge-Daemon startet. |
| `name` | String | User-Label (z.B. `"Halle1"`). Frei waehlbar, im Tree + in Logs sichtbar, **ist** Teil des IEC-Namespaces (`anvil.Halle1.<Device>.<Var>`). |
| `enabled` | Bool | Ein-/Ausschalter. `false` = Bridge wird nicht gestartet, Devices bleiben offline. Default: `true`. |

### Schnittstelle + Routing

| Feld | Typ | Bedeutung |
|---|---|---|
| `interface` | String | Netzwerk-Schnittstelle (`eth0`, `/dev/ttyUSB0`). Bridge gibt das an die Socket-/Serial-API weiter. |
| `bindAddress` | String (IP/CIDR) | Quell-IP fuer ausgehende TCP-Verbindungen, z.B. `192.168.24.100/24`. Leer = OS waehlt automatisch. |
| `gateway` | String (IP) | Default-Gateway fuer Pakete die das lokale Subnet verlassen. Leer = kein Gateway. |
| `pollIntervalMs` | Int (ms) | Abfrageintervall der Bridge. `0` = so schnell wie moeglich. Typisch: `100` fuer Modbus TCP, `0` fuer EtherCAT. |

### Network-Settings (Advanced)

Diese Felder decken Faelle ab in denen OS-Defaults nicht reichen —
typisch: viele parallele TCP-Verbindungen pro Slave, lange-laufende
Sessions ueber NAT, mehrere Subnetze auf einer NIC.

| Feld | Typ | Bedeutung |
|---|---|---|
| `subnetCidr` | String (CIDR) | Lokales Subnetz des Segments. Erlaubt per-Device-Gateway-Overrides wenn die NIC mehrere Netze fuehrt. |
| `sourcePortRange` | String `"min-max"` | TCP-Quellport-Pool, z.B. `30000-39999`. Leer = ephemerer OS-Bereich. Wichtig bei vielen parallelen Verbindungen zum selben Slave. |
| `keepAliveIdleSec` | Int (s) | Sekunden Leerlauf vor erstem TCP-Keep-Alive. `0` = OS-Default. |
| `keepAliveIntervalSec` | Int (s) | Abstand zwischen Probes. `0` = OS-Default. |
| `keepAliveCount` | Int | Anzahl fehlgeschlagener Probes bis Verbindung als tot gilt. `0` = OS-Default. |
| `maxConnections` | Int | Obergrenze des Verbindungspools. `0` = unlimitiert. Schutz vor Slave-Geraeten mit harter Verbindungs-Obergrenze. |
| `vlanId` | Int (1..4094) | 802.1Q-VLAN-Tag. `0` = ungetagged. |

### Protokoll-spezifische Settings

Im `settings`-Map (Key/Value) liegen Werte die nur fuer ein
bestimmtes Protokoll Sinn ergeben:

| Protokoll | Typische Settings |
|---|---|
| `modbustcp` | `port`, `timeout_ms` |
| `modbusrtu` | `serial_port`, `baud_rate`, `parity`, `stop_bits` |
| `ethercat` | `dc_sync_shift_ns`, `cycle_time_us` |
| `profibus` | `master_address`, `baud_rate` |

Plus protokollunabhaengig: `log_level`, `log_file`.

---

## Edit-Pfad in ForgeIEC Studio

Im Bus-Tree-Panel beide Pfade gleichwertig:

| Aktion | Wirkung |
|---|---|
| **Einfach-Klick** auf einen Segment-Knoten | `FPropertiesPanel` (rechts) zeigt alle Felder als Inline-Editoren. Aenderungen werden bei `editingFinished` ins Projekt geschrieben + dirty-Flag gesetzt. |
| **Doppelklick** | Modal-Dialog `FSegmentDialog` mit gleichem Feld-Set, gruppiert in *Allgemein* / *Protokoll* / *Advanced Network* / *Logging*. OK uebernimmt, Cancel verwirft. |

---

## Bridge-Lifecycle

Sobald Sie ein Segment anlegen + `enabled=true` setzen + speichern:

1. `anvild` erkennt das neue Segment beim naechsten Project-Push
2. anvild's Subprocess-Manager spawnt den passenden Bridge-Daemon
   (`tongs-<protocol>`) mit der Segment-ID als Argument
3. Bridge oeffnet die konfigurierte Schnittstelle + verbindet sich
   mit jedem Device
4. Live-Status laeuft per **Anvil-Zero-Copy-IPC** zwischen Bridge
   und PLC-Runtime — keine TCP-Loopback-Latenz
5. Bei Bridge-Crash startet anvild den Daemon auto-neu; die
   PLC-Logik laeuft ununterbrochen weiter

Bridge-Status pro Segment per MCP `bellows.protocol_status`
abrufbar, oder direkt im Bus-Panel als Farb-Indicator (gruen/gelb/
rot/grau).

---

## Beispiel: Modbus-TCP-Segment

```toml
[[bus_segments]]
segment_id     = "a3f7c2e1-7c4f-4e1a-9f9c-1a2b3c4d5e6f"
protocol       = "modbustcp"
name           = "Halle1"
enabled        = true
interface      = "eth0"
bind_address   = "192.168.24.100/24"
gateway        = ""
poll_interval  = 100

[bus_segments.settings]
port           = "502"
timeout_ms     = "2000"
log_level      = "info"
log_file       = "/var/log/forgeiec/halle1.log"
```

Effekt:

- `tongs-modbustcp` startet auf `eth0` mit Quell-IP `192.168.24.100`
- Polled alle Devices im 100-ms-Takt
- Akzeptiert pro Request bis 2000 ms Antwortzeit vor Timeout
- Logs nach `/var/log/forgeiec/halle1.log`
- IEC-Variablen erreichen Sie als `anvil.Halle1.<Device>.<...>`

---

## Verwandte Themen

- [Bus-Konfiguration — Schema-Ueberblick](../) — 5-Level-Namespace,
  FDD-System, XML-Persistenz
- [Bus-Devices](../devices/) — Geraete + Module + FDDs
- [Tongs-Bridge-Familie](/news/tongs-bridges/) — Fault-Modell +
  Bridge-Lifecycle
