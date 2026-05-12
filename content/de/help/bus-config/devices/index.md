---
title: "Bus-Devices"
summary: "Konfiguration eines Geraets innerhalb eines Bus-Segments — FDD-Integration, Module, Status-Variablen, per-Device-Overrides"
---

{{< components "studio,tongs,anvild" >}}

## Was ist ein Device?

Ein **Bus-Device** ist **ein einzelnes Geraet innerhalb eines
Segments** — Modbus-TCP-Slave (E/A-Block, Frequenzumrichter),
EtherCAT-Slave (Servo-Achse, I/O-Koppler), Profibus-DP-Slave oder
EtherNet/IP-Adapter. Pro Device fuehrt der Bridge-Daemon eine
logische Verbindung, polled die konfigurierten Register und
publiziert die Daten ueber **Anvil-Zero-Copy-IPC** an die
PLC-Runtime.

Ein Device kann **modular** sein: ein Buskoppler (Slot 0) traegt
1..N I/O-Module in den Slots 1..N. Kompaktgeraete ohne Erweiterungs-
Slots haben eine leere `modules`-Liste — die Variablen liegen
dann direkt am Slot 0.

---

## FDD-Integration

Statt jedes Geraet manuell zu beschreiben, importieren Sie eine
**Hersteller-FDD** beim Anlegen. ForgeIEC Studio:

1. Liest `<Identification>`, `<DiagnosticDecode>`, `<ModuleProtocol>`,
   `<Document>` aus der FDD
2. Zeigt das **eingebettete PDF-Datenblatt** im Documents-Tab des
   Properties-Panels
3. Fuellt **Status-Variablen** aus den Diagnose-Bit-Definitionen
4. Filtert den **Module-Picker** so dass nur kompatible Module
   sichtbar sind (per `<ModuleProtocol>`-Match)

Im `catalogRef`-Feld des Devices steht der Verweis auf die
verwendete FDD. Sie koennen eine FDD austauschen (z.B.
`weidmueller/UR20-FBC-PN-IRT-V2` → `-V3`), behalten aber alle
I/O-Variablen-Bindings — die Identitaet haengt an der `deviceId`-
UUID, nicht am Hersteller-Eintrag.

Eigene FDDs anlegen ueber `File → New FDD` (Diagnostics-Tab +
Documents-Tab im FDD-Editor).

Mehr zum FDD-System: [News-Eintrag](/news/catalog-fdd/).

---

## Felder eines Devices

Die Struct-Definition liegt in
`editor/include/model/FBusSegmentConfig.h`. Persistiert wird ein
Device im `.forge`-Projekt als `<fi:device>` unter
`<fi:segment>` (siehe [Bus-Konfiguration](../)).

### Identitaet + Adressierung

| Feld | Typ | Bedeutung |
|---|---|---|
| `deviceId` | UUID | Stabiler Primaerschluessel — automatisch beim Anlegen, ueberlebt Hostname-Rename und IP-Wechsel. Haelt damit alle Variablen-Bindings stabil. |
| `hostname` | String | User-sichtbares Label (`"Stachelbeere"`, `"Maibeere"`). **Ist** Teil des IEC-Namespaces (`anvil.<Segment>.Stachelbeere.<...>`). DHCP-sicher, aber **kein** Primaerschluessel. |
| `ipAddress` | String (IP) | IP-Adresse (Modbus TCP / EtherNet/IP). Leer fuer Geraete ohne IP (EtherCAT-Slaves identifizieren sich ueber Bus-Position). |
| `port` | Int | TCP-Port. Default `502` (Modbus TCP). |
| `slaveId` | Int | Modbus-Slave-ID (1..247). Bei TCP meist `1`. |
| `catalogRef` | String | Verweis auf den FDD-Katalogeintrag, z.B. `"weidmueller/UR20-FBC-PN-IRT-V2"`. Treibt Module-Picker + Diagnose-Bit-Aufloesung. |
| `description` | String | Frei-Text (`"Bewaesserungsventil Sued"`). |

### Module (Slots)

| Feld | Typ | Bedeutung |
|---|---|---|
| `modules` | Liste `FBusModuleConfig` | I/O-Module des Geraets. Slot 0 = Koppler / Kompaktgeraet, Slots 1..N = Erweiterungs-Module. Pro Modul: `slotIndex`, `catalogRef`, `name`, `baseAddress`, `settings`. |

Bei modularen Couplern kommt jedes Modul mit seiner eigenen
FDD-Datei daher — wieder mit Diagnose-Bits + Datenblatt. Der
Picker zeigt nur Module die der Coupler laut seiner `<ModuleProtocol>`
versteht.

### Per-Device-Overrides

Ueberschreiben — nur fuer **dieses** Device — die entsprechenden
Werte des Segments. `0` bzw. leerer String bedeutet *vom Segment
erben*. Im Properties-Panel meist unter *Advanced Overrides*
eingeklappt.

| Feld | Typ | Bedeutung |
|---|---|---|
| `mac` | String `AA:BB:CC:DD:EE:FF` | MAC-Adresse fuer statisches ARP / Identitaetskontrolle. Schuetzt vor IP-Klau bei DHCP-Geraeten. |
| `endianness` | Enum | `"ABCD"` (Big-Endian, IEC-Default), `"DCBA"` (Word-Swap), `"BADC"` (Byte-Swap), `"CDAB"` (beide). Leer = vom Segment erben. |
| `timeoutOverrideMs` | Int (ms) | Per-Device-Timeout. `0` = Segment-Timeout. |
| `retryCount` | Int | Wiederholungen pro Request. `0` = Segment-Default. |
| `connectionMode` | Enum | `"always"` (TCP offen halten) oder `"on_demand"` (pro Transaktion neu verbinden). Leer = Segment-Default. |
| `gatewayOverride` | String (IP) | Eigenes Gateway wenn das Device in einem anderen Subnet sitzt als die Bind-NIC. |

### Device-spezifische Settings

Im `settings`-Map (Key/Value) liegen Werte die nur fuer dieses
Geraet oder seinen Geraetetyp Sinn ergeben — z.B. ein Schwellenwert
eines Frequenzumrichters oder ein bevorzugter Modbus-Funktionscode.

---

## Edit-Pfad in ForgeIEC Studio

| Aktion | Wirkung |
|---|---|
| **Einfach-Klick** auf einen Device-Knoten | `FPropertiesPanel` zeigt alle Felder als Inline-Editoren — Allgemein, Override-Block, Diagnose-Bits mit Live-Werten, Status-Tabelle. |
| **Doppelklick** | Modal-Dialog `FBusDeviceDialog`. Im Edit-Modus ist der "Import aus Katalog"-Button gesperrt, damit ein nachtraeglicher FDD-Import keine bestehenden I/O-Variablen-Bindings ueberschreibt. |

---

## Status-Variablen (read-only)

Jedes Device veroeffentlicht zur Laufzeit eine Status-Struktur.
Diese Werte zeigt das Properties-Panel als **read-only Tabelle** —
die Bridge schreibt sie, der ST-Code liest sie. Auf der ST-Seite
sind sie unter `anvil.<Segment>.<Device>.Status.<Var>` zugaenglich:

| Status-Variable | Typ | Bedeutung |
|---|---|---|
| `xOnline` | `BOOL` | Geraet aktuell erreichbar (letzter Request hat geantwortet) |
| `eState` | `INT` | Zustands-Enum: 0=offline, 1=connecting, 2=online, 3=error |
| `wErrorCount` | `WORD` | Fehlgeschlagene Requests seit Bridge-Start |
| `sLastErrorMsg` | `STRING` | Letzte Fehlermeldung (Timeout, Modbus-Exception, ...) |

Zusaetzlich erscheinen alle Bits aus der **FDD-`<DiagnosticDecode>`**-
Sektion als typsichere Status-Member — z.B. `WireBreak`,
`ShortCircuit`, `OverTemperature`. Bedeutung + Schweregrad sieht
das Properties-Panel mehrsprachig (DE/EN) aus der FDD.

ST-Beispiel:

```text
IF anvil.Halle1.Maibeere.Status.xOnline AND
   anvil.Halle1.Maibeere.Status.wErrorCount < 10 AND
   NOT anvil.Halle1.Maibeere.Status.WireBreak THEN
    bSensor_OK := TRUE;
END_IF;
```

KI-Helfer-Diagnose-Loop via MCP `catalog.diag_bits` liefert die
aufgeloeste Bedeutung dieser Bits in Klartext.

---

## Beispiel: Weidmueller-UR20-Buskoppler mit zwei Modulen

Ein ProfiNet-IRT-Coupler (UR20-FBC-PN-IRT-V2) mit einem 8-DI-Modul
und einem 8-DO-Modul:

```toml
[[bus_segments.devices]]
device_id    = "0e5d5537-e328-44e6-8214-78d529b18ebd"
hostname     = "Stachelbeere"
ip_address   = "192.168.24.25"
port         = 502
slave_id     = 1
catalog_ref  = "weidmueller/UR20-FBC-PN-IRT-V2"
description  = "Buskoppler Halle 1, Reihe A"

[[bus_segments.devices.modules]]
slot_index   = 0
catalog_ref  = "weidmueller/UR20-FBC-PN-IRT-V2"
name         = "Koppler"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 1
catalog_ref  = "weidmueller/UR20-8DI-P"
name         = "8 DI Slot 1"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 2
catalog_ref  = "weidmueller/UR20-8DO-P"
name         = "8 DO Slot 2"
base_address = 0
```

Effekt:

- Die 8 Eingaenge erscheinen im Adress-Pool als `%IX0.0..%IX0.7`
  mit `deviceId=0e5d5537-...`, `moduleSlot=1`, `modbusAddress=0..7`
- Die 8 Ausgaenge analog mit `moduleSlot=2`
- ST-Zugriff: `anvil.Halle1.Stachelbeere.IO.DI_1` /
  `anvil.Halle1.Stachelbeere.IO.DO_1`
- Diagnose-Bits aus der FDD: `Status.WireBreak`,
  `Status.ShortCircuit`, etc. — typsicher, mehrsprachig erklaert

---

## Verwandte Themen

- [Bus-Segmente](../segments/) — das Netz in dem das Device lebt
- [Bus-Konfiguration — Schema-Ueberblick](../) — 5-Level-Namespace,
  XML-Persistenz
- [Catalog + FDD-System](/news/catalog-fdd/) — Hersteller-Daten +
  Diagnose-Bit-Resolver
- [Tongs-Bridge-Familie](/news/tongs-bridges/) — Fault-Model
