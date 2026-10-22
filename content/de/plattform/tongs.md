---
title: "Tongs"
description: "Feldbus-Bridges — Modbus TCP/RTU, LoRaWAN, EtherCAT, PROFIBUS, EtherNet/IP als eigenständige Prozesse"
weight: 6
---

## Die Zange

Die Zange greift ins Feuer und holt das glühende Werkstück heraus.
**Tongs** sind die Feldbus-Bridges der ForgeIEC-Plattform — sie greifen
in die industrielle Peripherie und bringen Prozessdaten sicher zum
SPS-Kern.

---

## Unterstützte Protokolle

| Protokoll | Bridge | Medium | Status |
|-----------|--------|--------|--------|
| **Modbus TCP** | `tongs-modbustcp` | Ethernet | {{< status "use" "verfügbar" >}} |
| **Modbus RTU** | `tongs-modbusrtu` | RS-485 (seriell) | {{< status "use" "verfügbar" >}} |
| **LoRaWAN** | `tongs-lorawan` | Funk (Sensorik für Landwirtschaft und weitläufige Anlagen) | {{< status "wip" "in Arbeit (Schwerpunkt)" >}} |
| **EtherCAT** | `tongs-ethercat` | Ethernet (Echtzeit) | {{< status "wip" "Gerüst, in Arbeit" >}} |
| **PROFIBUS DP** | `tongs-profibus` | Seriell (Feldbus) | {{< status "wip" "Gerüst, in Arbeit" >}} |
| **EtherNet/IP** | `tongs-ethernetip` | Ethernet | {{< status "wip" "Gerüst, in Arbeit" >}} |

<!-- ENTWURF: Laut Audit W-14 liefert das Paket forgeiec-anvil-server kein tongs-modbusrtu aus; der Eigentümer nennt Modbus RTU verfügbar. Auslieferung prüfen. -->

---

## Architektur: Ein Prozess pro Segment

Jede Bridge läuft als eigenständiger Prozess. Der Anvil-Server (anvild) startet, überwacht
und restartet Bridges automatisch. Ein Absturz einer Bridge beeinträchtigt
weder den SPS-Kern noch andere Bridges.

```
anvild
  |-- tongs-modbustcp --config config.toml --segment mb1
  |-- tongs-modbustcp --config config.toml --segment mb2
  |-- tongs-ethercat  --config config.toml --segment ec1
  +-- tongs-profibus  --config config.toml --segment pb1
```

Die Kommunikation zwischen `anvild` und den Bridges erfolgt über
Anvil Technology (Zero-Copy Shared Memory). Jedes Segment erhält
seinen eigenen IPC-Kanal.

---

## Segment-Hierarchie

Tongs organisiert die industrielle Kommunikation in einer
aus etablierten SPS-Werkzeugen gewohnten Hierarchie:

```
Bussysteme
+-- Modbus TCP: Halle 1 (eth0) [aktiv]
|   +-- 192.168.1.100 -- Temperaturmodul (Slave 1)
|   |   +-- Temperatur : INT (%IW0)   [Subscribe]
|   |   +-- Sollwert : INT (%QW10)    [Publish]
|   +-- 192.168.1.101 -- Pumpe (Slave 2)
+-- Modbus RTU: Labor (/dev/ttyUSB0)
+-- Unzugeordnet (Scanner-Pool)
    +-- 192.168.2.55 -- Unbekannt
```

---

## Geräteerkennung

Der integrierte Netzwerk-Scanner erkennt Feldgeräte automatisch:

- **ICMP Ping-Scan** — Erreichbare Hosts im Subnetz ermitteln
- **Port-Scan** — Modbus-Port (502) und weitere Dienste prüfen
- **Register-Scan** — Modbus-Register auslesen und Gerätetyp identifizieren
- **FDD-Gerätekatalog** — Bekannte Geräte anhand ihrer Register-Signaturen
  zuordnen

Gefundene Geräte landen im Scanner-Pool und können per Drag-and-Drop
einem Segment zugeordnet werden.

---

## Automatische Adressvergabe

IEC-Adressen (`%IX`, `%QW`, `%MD` etc.) werden global und kollisionsfrei
vergeben. Bestehende Adressen in globalen Variablenlisten werden
berücksichtigt. Die zugehörigen VAR_ANVIL-Transportblöcke werden
automatisch generiert.

---

## Richtungsmodell

Jede Variable hat eine eindeutige Richtung:

- **in** (Subscribe/Read) — Bridge liest vom Feldgerät, SPS empfängt
- **out** (Publish/Write) — SPS sendet, Bridge schreibt zum Feldgerät

Es gibt kein "inout". Die Bridge filtert: nur "in"-Variablen werden
gelesen (Modbus FC3), nur "out"-Variablen werden geschrieben
(Modbus FC5/FC6/FC16).

---

## Konfiguration

Segmente und Geräte werden in `config.toml` konfiguriert:

```toml
[[bus_segments]]
id = "mb1"
protocol = "modbus_tcp"
enabled = true

[bus_segments.settings]
interface = "eth0"
port = 502

[[bus_segments.devices]]
name = "Temperaturmodul"
host = "192.168.1.100"
slave_id = 1
```

---

## Technische Details

| Eigenschaft | Wert |
|-------------|------|
| **Sprache** | Rust |
| **Modbus-Crate** | tokio-modbus 0.17 |
| **IPC** | Anvil-Bus (iceoryx2, Zero-Copy Shared Memory) |
| **Prozessmodell** | Ein Daemon pro aktivem Segment |
| **Plattformen** | x86_64, ARM64, ARMv7 (Linux) |
| **Lizenz** | AGPL-3.0-or-later |

---

<div style="text-align:center; padding: 2rem;">

**Tongs — Der sichere Griff in die industrielle Peripherie.**

blacksmith@forgeiec.io

</div>
