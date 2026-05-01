---
title: "Bus-Devices"
summary: "Konfiguration eines Geraets innerhalb eines Bus-Segments (Modbus-Slave, EtherCAT-Slave, ...)"
---

## Ueberblick

Ein **Bus-Device** ist ein **einzelnes Geraet innerhalb eines Segments** —
typisch ein Modbus-TCP-Slave (E/A-Block, Frequenzumrichter), ein
EtherCAT-Slave (Servo-Achse, I/O-Koppler), ein Profibus-DP-Slave oder ein
EtherNet-IP-Adapter. Pro Device verwaltet die zustaendige Bridge eine
logische Verbindung, polled die konfigurierten Register und veroeffentlicht
die Daten ueber die Anvil-IPC-Gruppe an die PLC-Runtime.

Ein Device kann **modular** sein: ein Buskoppler (Slot 0) traegt 1..N
I/O-Module in den Slots 1..N. Kompaktgeraete ohne Erweiterungs-Slots haben
eine leere `modules`-Liste — die Variablen liegen dann direkt am Slot 0.

## Felder eines Devices

Die Struct-Definition liegt in `editor/include/model/FBusSegmentConfig.h`
(neben dem Segment). Persistiert wird ein Device im `.forge`-Projekt als
`<fi:device>` unter `<fi:segment>` (siehe [Bus-Konfiguration](../)).

### Identitaet + Adressierung

| Feld | Typ | Bedeutung |
|---|---|---|
| `deviceId` | UUID | Stabiler Primaerschluessel — automatisch beim Anlegen erzeugt. Ueberlebt Hostname-Rename und IP-Wechsel und haelt damit alle Variablen-Bindings stabil. |
| `hostname` | String | User-sichtbares Label (`"Maibeere"`, `"Stachelbeere"`). DHCP-sicher, aber ausdruecklich **kein** Primaerschluessel. |
| `ipAddress` | String (IP) | IP-Adresse (Modbus TCP / EtherNet-IP). Leer fuer Geraete ohne IP (EtherCAT-Slaves identifizieren sich ueber Position auf dem Bus). |
| `port` | Int | TCP-Port. Default `502` (Modbus TCP). |
| `slaveId` | Int | Modbus-Slave-ID (1..247). Bei TCP meist `1`. |
| `anvilGroup` | String | Anvil-IPC-Gruppe fuer den Zero-Copy-Transport zwischen Bridge und PLC-Runtime. Konvention: gleicher Name wie `hostname`. |
| `catalogRef` | String | Optionaler Verweis auf einen FDD-Katalogeintrag (`"WAGO-750-352"`), der das Geraet beschreibt. |
| `description` | String | Frei-Text-Beschreibung (`"Bewaesserungsventil Sued"`). |

### Module (Slots)

| Feld | Typ | Bedeutung |
|---|---|---|
| `modules` | Liste `FBusModuleConfig` | I/O-Module des Geraets. Slot 0 = Koppler / Kompaktgeraet, Slots 1..N = Erweiterungs-Module. Pro Modul: `slotIndex`, `catalogRef`, `name`, `baseAddress`, `settings`. |

### Per-Device-Overrides

Diese Felder ueberschreiben — nur fuer **dieses** Device — die entsprechenden
Werte des Segments. `0` bzw. leerer String bedeutet *vom Segment erben*.
Im Properties-Panel sind sie unter dem Block *Advanced Overrides*
zusammengefasst und meist eingeklappt.

| Feld | Typ | Bedeutung |
|---|---|---|
| `mac` | String `AA:BB:CC:DD:EE:FF` | MAC-Adresse fuer statisches ARP / Identitaetskontrolle. Schuetzt vor IP-Klau bei DHCP-Geraeten. |
| `endianness` | Enum | Wort-/Byte-Reihenfolge fuer Multi-Register-Werte: `"ABCD"` (Big-Endian, IEC-Default), `"DCBA"` (Word-Swap), `"BADC"` (Byte-Swap), `"CDAB"` (Byte-Swap + Word-Swap). Leer = vom Segment erben. |
| `timeoutOverrideMs` | Int (ms) | Per-Device-Timeout. `0` = Segment-Timeout verwenden. |
| `retryCount` | Int | Wiederholungs-Versuche pro Request. `0` = Segment-Default. |
| `connectionMode` | Enum | `"always"` (TCP zwischen Zyklen offen halten) oder `"on_demand"` (pro Transaktion neu verbinden). Leer = Segment-/Bridge-Default. |
| `gatewayOverride` | String (IP) | Eigenes Gateway, wenn das Device in einem anderen Subnet sitzt als die Bind-NIC. |

### Geraete-spezifische Settings

Im `settings`-Map (Key/Value) liegen alle Werte, die nur fuer dieses Geraete
oder seinen Geraetetyp Sinn ergeben — z.B. ein Schwellenwert eines
Frequenzumrichters oder ein bevorzugter Funktionscode.

## Edit-Pfad

| Aktion | Wirkung |
|---|---|
| **Einfach-Klick** auf einen Device-Knoten | `FPropertiesPanel` zeigt alle Felder als Inline-Editoren — Allgemein-Block (Hostname, IP, Port, SlaveId, Anvil-Group), Override-Block (MAC, Timeout, Retries, Endianness, Connection-Mode, Gateway-Override, Description) und die Status-Tabelle. |
| **Doppelklick** auf einen Device-Knoten | Oeffnet den modalen `FBusDeviceDialog` mit identischem Feld-Set. Im Edit-Modus ist der "Import aus Katalog"-Button gesperrt, damit ein nachtraeglicher FDD-Import keine bestehenden I/O-Variablen-Bindings ueberschreibt. |

## Status-Variablen (read-only)

Jedes Device veroeffentlicht zur Laufzeit eine Status-Struktur, die der
Daemon ueber den gRPC-Status-Stream sendet. Diese Werte werden im
Properties-Panel als **read-only Tabelle** angezeigt und sind aus
Anwender-Sicht **nicht editierbar** — die Bridge schreibt sie. Im
ST-Code sind sie aber als qualifizierte Pfade unter `anvil.<seg>.<dev>.Status.*`
ansprechbar:

| Status-Variable | Typ | Bedeutung |
|---|---|---|
| `xOnline` | `BOOL` | Geraet aktuell erreichbar (letzter Request hat geantwortet). |
| `eState` | `INT` | Zustands-Enum: 0=offline, 1=connecting, 2=online, 3=error. |
| `wErrorCount` | `WORD` | Zaehler fuer fehlgeschlagene Requests seit Start des Bridges. |
| `sLastErrorMsg` | `STRING` | Letzte Fehlermeldung (Timeout, Modbus-Exception, ...). |

```iec
IF anvil.Halle1.Maibeere.Status.xOnline AND
   anvil.Halle1.Maibeere.Status.wErrorCount < 10 THEN
    bSensor_OK := TRUE;
END_IF;
```

## Beispiel: WAGO-750-Buskoppler mit zwei Slots

Ein Modbus-TCP-Buskoppler 750-352 mit einem 8-DI-Modul (750-430) auf Slot 1
und einem 8-DO-Modul (750-530) auf Slot 2:

```toml
[[bus_segments.devices]]
device_id    = "0e5d5537-e328-44e6-8214-78d529b18ebd"
hostname     = "Maibeere"
ip_address   = "192.168.24.25"
port         = 502
slave_id     = 1
anvil_group  = "Maibeere"
catalog_ref  = "WAGO-750-352"
description  = "Buskoppler Halle 1, Reihe A"

[[bus_segments.devices.modules]]
slot_index   = 0
catalog_ref  = "WAGO-750-352"
name         = "Koppler"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 1
catalog_ref  = "WAGO-750-430"
name         = "8 DI Slot 1"
base_address = 0     # Coil 0..7

[[bus_segments.devices.modules]]
slot_index   = 2
catalog_ref  = "WAGO-750-530"
name         = "8 DO Slot 2"
base_address = 0     # Discrete Output 0..7
```

Die 8 Eingaenge erscheinen im Adress-Pool als `%IX0.0..%IX0.7` mit
`deviceId="0e5d5537-..."`, `moduleSlot=1` und `modbusAddress=0..7`. Die
8 Ausgaenge analog mit `moduleSlot=2`.

## Verwandte Themen

* [Bus-Segmente](../segments/) — das Netz, in dem das Device lebt.
* [Bus-Konfiguration — Schema-Ueberblick](../) — XML-Persistenz.
* [Projekt-Dateiformat](../../file-format/) — Adress-Pool und
  Variable-zu-Device-Bindings.
