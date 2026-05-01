---
title: "Bus-Segmente"
summary: "Konfiguration eines Feldbus-Segments (physisches Netz auf einer Schnittstelle)"
---

## Ueberblick

Ein **Bus-Segment** beschreibt **ein physisches Netzwerk auf einer
Schnittstelle des PLC-Targets** — typischerweise ein Ethernet-Port
(`eth0`, `enp3s0`) fuer Modbus TCP / EtherCAT / EtherNet-IP, oder ein
serieller Port (`/dev/ttyUSB0`) fuer Modbus RTU / Profibus DP. Pro Segment
spawnt der `anvild`-Daemon **genau einen Bridge-Prozess** (`tongs-modbustcp`,
`tongs-ethercat`, ...), der den Verkehr zu allen Devices in diesem Segment
abwickelt.

Ein Projekt kann beliebig viele Segmente halten — jedes mit eigenem
Protokoll, eigener Schnittstelle und eigenem Polling-Takt. So koennen
z.B. eine schnelle EtherCAT-Achssteuerung (`eth1`, 1 ms) und eine langsame
Modbus-TCP-Sensorerfassung (`eth0`, 100 ms) parallel im selben Projekt
laufen.

## Felder eines Segments

Die Struct-Definition liegt in `editor/include/model/FBusSegmentConfig.h`.
Persistiert wird ein Segment im `.forge`-Projekt als `<fi:segment>` unter
`<fi:busConfig>` (siehe [Bus-Konfiguration](../)).

### Identitaet + Protokoll

| Feld | Typ | Bedeutung |
|---|---|---|
| `segmentId` | UUID | Stabiler Primaerschluessel — automatisch beim Anlegen erzeugt, nicht editierbar. Ueberlebt Rename, Protokoll-Wechsel und IP-Aenderung. |
| `protocol` | Enum | `modbustcp` / `modbusrtu` / `ethercat` / `profibus` / `ethernetip`. Bestimmt, welcher Bridge-Daemon gestartet wird. |
| `name` | String | User-Label (z.B. `"Feldbus Halle 1"`). Frei waehlbar, im Tree und in Logs sichtbar. |
| `enabled` | Bool | Ein-/Ausschalter. `false` = Bridge wird nicht gestartet, Devices bleiben offline. Default: `true`. |

### Schnittstelle + Routing

| Feld | Typ | Bedeutung |
|---|---|---|
| `interface` | String | Netzwerk-Schnittstelle (`eth0`, `enp3s0`, `/dev/ttyUSB0`). Wird vom Bridge an die Socket- bzw. Serial-API uebergeben. |
| `bindAddress` | String (IP/CIDR) | Quell-IP fuer ausgehende TCP-Verbindungen, z.B. `192.168.24.100/24`. Leer = OS waehlt automatisch die erste IP der Schnittstelle. |
| `gateway` | String (IP) | Default-Gateway fuer Pakete, die das lokale Subnet verlassen. Leer = kein Gateway. |
| `pollIntervalMs` | Int (ms) | Abfrageintervall der Bridge. `0` = so schnell wie moeglich (busy-loop / Echtzeit). Typisch: `100` fuer Modbus TCP, `0` fuer EtherCAT. |

### Network-Settings (Advanced)

Diese Felder kamen mit dem Network-Settings-Sprint hinzu und decken Faelle
ab, in denen die OS-Defaults nicht ausreichen — typisch: mehrere parallele
TCP-Verbindungen pro Slave, lange-laufende TCP-Sessions ueber NAT, oder
mehrere Subnetze auf einer NIC.

| Feld | Typ | Bedeutung |
|---|---|---|
| `subnetCidr` | String (CIDR) | Lokales Subnetz des Segments, z.B. `192.168.24.0/24`. Erlaubt der Bridge, per-Device-Gateway-Overrides korrekt zu routen, wenn die Bind-NIC mehrere Netze fuehrt. |
| `sourcePortRange` | String `"min-max"` | TCP-Quellport-Pool fuer ausgehende Verbindungen, z.B. `30000-39999`. Leer = OS waehlt aus dem ephemeren Bereich. Wichtig, wenn parallel viele Verbindungen zum selben Slave aufgebaut werden (eine Verbindung pro Quellport). |
| `keepAliveIdleSec` | Int (s) | Sekunden Leerlauf, bevor das erste TCP-Keep-Alive gesendet wird. `0` = OS-Default. |
| `keepAliveIntervalSec` | Int (s) | Abstand zwischen Keep-Alive-Probes. `0` = OS-Default. |
| `keepAliveCount` | Int | Anzahl fehlgeschlagener Probes, bevor die Verbindung als tot gilt. `0` = OS-Default. |
| `maxConnections` | Int | Obergrenze des Verbindungspools. `0` = unlimitiert. Schutz gegen Slave-Geraete mit harter Verbindungs-Obergrenze. |
| `vlanId` | Int (1..4094) | 802.1Q-VLAN-Tag fuer ausgehende Frames. `0` = ungetagged. |

### Protokoll-spezifische Settings

Im `settings`-Map (Key/Value) liegen alle Werte, die nur fuer ein bestimmtes
Protokoll Sinn ergeben — z.B. fuer Modbus TCP: `port`, `timeout_ms`; fuer
Modbus RTU: `serial_port`, `baud_rate`, `parity`, `stop_bits`; fuer Profibus:
`master_address`. Auch `log_level` und `log_file` sind protokollunabhaengig
in dieser Map abgelegt.

## Edit-Pfad

Im Bus-Tree-Panel sind beide Pfade gleichwertig — sie operieren auf demselben
Feld-Set, der inhaltliche Effekt ist identisch:

| Aktion | Wirkung |
|---|---|
| **Einfach-Klick** auf einen Segment-Knoten | Das `FPropertiesPanel` (Standard-Andockstelle: rechts) zeigt alle Felder als Inline-Editoren — Aenderungen werden sofort beim `editingFinished` ins Projekt geschrieben und markieren das Projekt als dirty. |
| **Doppelklick** auf einen Segment-Knoten | Oeffnet den modalen `FSegmentDialog` mit demselben Feld-Set, gruppiert in *Allgemein* / *Modbus TCP* / *Advanced Network* / *Logging*. OK uebernimmt die Werte, Cancel verwirft sie. |

## Beispiel: Modbus-TCP-Segment

```toml
[[bus_segments]]
segment_id     = "a3f7c2e1-7c4f-4e1a-9f9c-1a2b3c4d5e6f"
protocol       = "modbustcp"
name           = "Feldbus Halle 1"
enabled        = true
interface      = "eth0"
bind_address   = "192.168.24.100/24"
gateway        = ""
poll_interval  = 100   # ms

[bus_segments.settings]
port           = "502"
timeout_ms     = "2000"
log_level      = "info"
log_file       = "/var/log/forgeiec/halle1.log"
```

Das Segment startet `tongs-modbustcp` auf `eth0` mit Quell-IP
`192.168.24.100`, fragt alle Devices im 100-ms-Takt ab und akzeptiert pro
Request bis zu 2000 ms Antwortzeit, bevor ein Timeout-Fehler im Status-Stream
landet.

## Verwandte Themen

* [Bus-Konfiguration — Schema-Ueberblick](../) — XML-Persistenz und
  PLCopen-`<addData>`-Mechanismus.
* [Bus-Devices](../devices/) — Geraete innerhalb eines Segments.
* [Projekt-Dateiformat](../../file-format/) — `.forge`-XML-Wurzel.
