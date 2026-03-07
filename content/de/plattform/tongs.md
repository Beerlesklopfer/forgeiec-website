---
title: "Tongs"
description: "Feldbus-Bridges — Modbus TCP/RTU, EtherCAT, Profibus als eigenstaendige Prozesse"
weight: 6
---

## Die Zange

Die Zange greift ins Feuer und holt das gluehende Werkstueck heraus.
**Tongs** sind die Feldbus-Bridges der ForgeIEC-Plattform — sie greifen
in die industrielle Peripherie und bringen Prozessdaten sicher zum
SPS-Kern.

---

## Unterstuetzte Protokolle

| Protokoll | Bridge | Medium | Status |
|-----------|--------|--------|--------|
| **Modbus TCP** | `tongs-modbustcp` | Ethernet | Verfuegbar |
| **Modbus RTU** | `tongs-modbusrtu` | RS-485 (seriell) | Verfuegbar |
| **EtherCAT** | `tongs-ethercat` | Ethernet (Echtzeit) | In Entwicklung |
| **Profibus DP** | `tongs-profibus` | Seriell (Feldbus) | In Entwicklung |

---

## Architektur: Ein Prozess pro Segment

Jede Bridge laeuft als eigenstaendiger Prozess. `anvild` startet, ueberwacht
und restartet Bridges automatisch. Ein Absturz einer Bridge beeintraechtigt
weder den SPS-Kern noch andere Bridges.

```
anvild
  |-- tongs-modbustcp --config config.toml --segment mb1
  |-- tongs-modbustcp --config config.toml --segment mb2
  |-- tongs-ethercat  --config config.toml --segment ec1
  +-- tongs-profibus  --config config.toml --segment pb1
```

Die Kommunikation zwischen `anvild` und den Bridges erfolgt ueber
Anvil Technology (Zero-Copy Shared Memory). Jedes Segment erhaelt
seinen eigenen IPC-Kanal.

---

## Segment-Hierarchie

Tongs organisiert die industrielle Kommunikation in einer
CoDeSys-kompatiblen Hierarchie:

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

## Geraeteerkennung

Der integrierte Netzwerk-Scanner erkennt Feldgeraete automatisch:

- **ICMP Ping-Scan** — Erreichbare Hosts im Subnetz ermitteln
- **Port-Scan** — Modbus-Port (502) und weitere Dienste pruefen
- **Register-Scan** — Modbus-Register auslesen und Geraetetyp identifizieren
- **FDD-Geraetekatalog** — Bekannte Geraete anhand ihrer Register-Signaturen
  zuordnen

Gefundene Geraete landen im Scanner-Pool und koennen per Drag-and-Drop
einem Segment zugeordnet werden.

---

## Automatische Adressvergabe

IEC-Adressen (`%IX`, `%QW`, `%MD` etc.) werden global und kollisionsfrei
vergeben. Bestehende Adressen in globalen Variablenlisten werden
beruecksichtigt. Die zugehoerigen VAR_ANVIL-Transportbloecke werden
automatisch generiert.

---

## Richtungsmodell

Jede Variable hat eine eindeutige Richtung:

- **in** (Subscribe/Read) — Bridge liest vom Feldgeraet, SPS empfaengt
- **out** (Publish/Write) — SPS sendet, Bridge schreibt zum Feldgeraet

Es gibt kein "inout". Die Bridge filtert: nur "in"-Variablen werden
gelesen (Modbus FC3), nur "out"-Variablen werden geschrieben
(Modbus FC5/FC6/FC16).

---

## Konfiguration

Segmente und Geraete werden in `config.toml` konfiguriert:

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
| **IPC** | Anvil Technology (Zero-Copy Shared Memory) |
| **Prozessmodell** | Ein Daemon pro aktivem Segment |
| **Plattformen** | x86_64, ARM64, ARMv7 (Linux) |

---

<div style="text-align:center; padding: 2rem;">

**Tongs — Der sichere Griff in die industrielle Peripherie.**

blacksmith@forgeiec.io

</div>
