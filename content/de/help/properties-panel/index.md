---
title: "Properties-Panel"
summary: "Inline-Editor fuer das im Project-Tree selektierte Bus-Element"
---

## Ueberblick

Das **Properties-Panel** ist die rechte Detail-Anzeige des
Editor-Hauptfensters. Es zeigt **alle Felder des aktuell im
Project-Tree selektierten Elements** an und macht sie inline editierbar
— ohne dass man fuer jeden Edit einen modalen Dialog oeffnen muss.

```
Project-Tree                          Properties-Panel
+-- Bus                               +-- Name:        OG-Modbus
|   +-- segment_modbus    <-- klick   |   Protocol:    [modbustcp ▼]
|       +-- device_motor              |   Interface:   eth0
|           +-- slot_0                |   Bind Addr:   192.168.1.10/24
+-- Programs                          |   Poll:        100 ms
|   +-- PLC_PRG                       |   Enabled:     [x]
                                      |   Port:        502
                                      |   Timeout:     2000 ms
```

Ein **Single-Click** auf einen Knoten im Project-Tree erzeugt sofort die
passende Felder-Liste — ein **Doppelklick** oeffnet zusaetzlich den
modalen Konfigurations-Dialog ([Bus-Konfiguration](../bus-config/)) mit
identischem Feld-Set.

Das Panel ist in eine `QScrollArea` gewickelt und scrollt vertikal:
Devices mit FDD-Erweiterungen + Status-Tabelle bekommen leicht
40+ Felder, und die muessen alle erreichbar bleiben, auch wenn der
Dock-Bereich schmal ist.

## Bus-Segment

Wenn ein Bus-Segment selektiert ist, zeigt das Panel:

| Feld | Bedeutung |
|---|---|
| **Name** | Anzeige-Name im Project-Tree. |
| **Protocol** | `modbustcp`, `modbusrtu`, `ethercat`, `profibus`, `ethernetip`. |
| **Interface** | Netzwerk-Interface, an das der Bridge bindet (`eth0`, `eth1`, …). |
| **Bind Address** | CIDR-Notation, z. B. `192.168.1.10/24`. Validiert. |
| **Gateway** | Default-Gateway fuer den Bridge-Prozess. |
| **Poll Interval** | Periode in `ms`, mit der der Bridge die Devices abfragt. |
| **Enabled** | Bridge-Subprozess aktiv (an / aus). |

### Advanced Network (alle optional)

Spiegelt die gleichnamige Gruppe aus dem `FSegmentDialog` und
ueberschreibt OS- bzw. Bridge-Defaults:

  - **Subnet CIDR** (`192.168.24.0/24`)
  - **Source Port Range** (`30000-39999`)
  - **Keep-Alive Idle / Interval / Count** (TCP-Heartbeat)
  - **Max Connections** (`0` = unlimited)
  - **VLAN ID** (`0` = untagged)

### Protokoll-spezifisch

| Protokoll | Felder |
|---|---|
| `modbustcp`  | `Port` (Default `502`), `Timeout` in `ms` (Default `2000`). |
| `modbusrtu`  | `Serial Port` (z. B. `/dev/ttyUSB0`), `Baud Rate`, `Parity` (`none`/`even`/`odd`). |
| `profibus`   | `Serial Port`, `Baud Rate` (bis 12 Mbit/s), `Master Address` (0..126). |

### Logging

  - **Log Level** — `off` / `error` / `warn` / `info` / `debug`.
  - **Log File** — z. B. `/var/log/forgeiec/segment.log`. Leer = stdout.

## Bus-Device

| Feld | Bedeutung |
|---|---|
| **Hostname** | DNS-Name oder Anzeige-Name. |
| **IP Address** | IPv4 des Devices. |
| **Port** | Modbus-Port am Slave (Default `502`). |
| **Slave ID** | Modbus-Unit-ID (0..247). |
| **Anvil Group** | Anvil-IPC-Gruppen-Name — zugleich der Name der auto-generierten `AnvilVarList`. Beim Umbenennen werden GVL-Tag, AnvilVarList und alle Pool-Variablen mit `anvilGroup = oldGroup` synchron umbenannt. |

### Advanced Overrides (alle optional, leer = Segment-Default)

  - **MAC Address** — `AA:BB:CC:DD:EE:FF`. Mit Validator.
  - **Endianness** — `ABCD` / `DCBA` / `BADC` / `CDAB`.
  - **Timeout** in `ms`. `0` = vom Segment erben.
  - **Retry Count**. `0` = vom Segment erben.
  - **Connection Mode** — `always connected` oder `on demand`.
  - **Gateway (override)** — nur wenn das Device in einem anderen Subnet liegt.
  - **Description** — freier Text (z. B. `Bewaesserungsventil Sued`).

### Status-Variablen (read-only)

Jedes Device exponiert automatisch das Common-Fault-Model — sieben
implizite Felder, die ueber Anvil als read-only Status-Topic
veroeffentlicht werden:

| Name | IEC-Typ | Bedeutung |
|---|---|---|
| `xOnline`              | `BOOL`         | TRUE wenn `eState = Online` oder `Degraded`. |
| `eState`               | `eDeviceState` | Aktueller Fehlerzustand. |
| `wErrorCount`          | `UDINT`        | Fehler insgesamt seit Bridge-Start. |
| `wConsecutiveFailures` | `UDINT`        | Fehler seit letztem `Online` (resettet auf `Online`). |
| `wLastErrorCode`       | `UINT`         | `0` = keiner; `1..99` Common; `100+` Protokoll. |
| `sLastErrorMsg`        | `STRING[48]`   | UTF-8, zero-padded. |
| `tLastTransition`      | `ULINT`        | Unix-Zeit (ms) des letzten State-Wechsels. |

Wenn das Device an eine **FDD** (Field-Device-Description) gebunden
ist (`catalogRef`), zeigt die Status-Tabelle zusaetzlich die
FDD-spezifischen Erweiterungen mit dem Vermerk `FDD +<offset>` in der
`Source`-Spalte.

Im ST-Code sind alle Status-Variablen unter
`anvil.<seg>.<dev>.Status.*` ansprechbar:

```iec
IF NOT anvil.OG_Modbus.K1_Mains.Status.xOnline THEN
    Lampe_Stoerung := TRUE;
END_IF;
```

## Bus-Module

Bus-Module sind I/O-Slices innerhalb eines Devices. Das Panel zeigt:

### Metadata

  - **Module** (Anzeige-Name oder `catalogRef`)
  - **Slot** (Slot-Index im Device)
  - **Catalog** (FDD-Referenz, z. B. `Beckhoff.EL2008`)
  - **Base Addr** (IEC-Basis-Offset)

### IO-Variables-Tabelle

Listet alle Pool-Variablen, deren `busBinding.deviceId` und
`busBinding.moduleSlot` zu diesem Modul passen. Spalten:

| Spalte | Inhalt |
|---|---|
| **Name** | Pool-Name (editierbar, z. B. `Motor_Run`). |
| **Type** | IEC-Typ (editierbar, z. B. `BOOL`, `INT`). |
| **Address** | IEC-Adresse (`%IX0.0`, read-only). |
| **Bus Addr** | Modbus-Register-Offset (read-only). |
| **Dir** | `in` oder `out` (read-only). |

Sortierreihenfolge: Inputs vor Outputs, dann nach Bus-Adresse aufsteigend.

## Edit-Verhalten

Jeder Edit im Panel laeuft direkt gegen das Modell:

  1. Edit im Widget (`editingFinished` / `valueChanged` / `toggled`).
  2. Modell-Feld wird aktualisiert (`seg->name = ...`).
  3. `project->markDirty()` setzt das Dirty-Flag.
  4. Signal `busConfigEdited` wird emittiert.
  5. Das MainWindow refresht das Project-Tree-Label, falls noetig.

Es gibt **kein** explizites `Apply` und **kein** `Cancel` — Edits sind
sofort wirksam. `Ctrl+Z` (Undo) auf dem Project-Tree macht den letzten
Edit rueckgaengig.

## Verwandte Themen

  - [Bus-Konfiguration](../bus-config/) — modale Dialoge mit
    identischem Feld-Set, fuer Power-User mit hohem Edit-Volumen.
  - [Variables Panel](../variables/) — der Pool, aus dem die
    `IO-Variables`-Tabelle stammt.
