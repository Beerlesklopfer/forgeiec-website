---
title: "Bus-Konfiguration"
summary: "PLCopen-XML-Schema fuer die industrielle Feldbus-Konfiguration"
---

## Namespace

```
https://forgeiec.io/v2/bus-config
```

Dieses Schema beschreibt die ForgeIEC-Erweiterung des PLCopen-XML-Formats
zur Speicherung der Feldbus-Konfiguration innerhalb von `.forge`-Projektdateien.
Es nutzt den standardkonformen `<addData>`-Mechanismus von PLCopen TC6.

## Ueberblick

Die Bus-Konfiguration definiert die physische Topologie einer Anlage:
**Segmente** (Feldbusnetze) enthalten **Devices** (Geraete), und jedes
Device ist ueber ein Bus-Binding mit den I/O-Variablen im Projekt verknuepft.

```
.forge-Projekt
  +-- Segmente (Feldbus-Netze)
  |     +-- Devices (Geraete)
  |           +-- Variablen (via Bus-Binding im Adress-Pool)
  +-- Adress-Pool (FAddressPool)
        +-- Variable: DI_1, %IX0.0, busBinding → Maibeere
        +-- Variable: DO_1, %QX0.0, busBinding → Maibeere
```

## XML-Struktur

Die Bus-Konfiguration wird als `<addData>` auf Projektebene gespeichert:

```xml
<project>
  <!-- Standard PLCopen-Inhalt -->
  <types>...</types>
  <instances>...</instances>

  <!-- ForgeIEC Bus-Konfiguration -->
  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="Feldbus Halle 1"
                    enabled="true"
                    interface="eth0"
                    bindAddress="192.168.24.100/24"
                    gateway=""
                    pollIntervalMs="0">

          <fi:device hostname="Maibeere"
                     ipAddress="192.168.24.25"
                     port="502"
                     slaveId="1"
                     anvilGroup="Maibeere"/>

          <fi:device hostname="Stachelbeere"
                     ipAddress="192.168.24.26"
                     port="502"
                     slaveId="1"
                     anvilGroup="Stachelbeere"/>

        </fi:segment>

      </fi:busConfig>
    </data>
  </addData>
</project>
```

## Elemente

### `fi:busConfig`

Wurzelelement. Enthaelt ein oder mehrere `fi:segment`-Elemente.

| Attribut | Pflicht | Beschreibung |
|----------|---------|--------------|
| `xmlns:fi` | ja | Namespace: `https://forgeiec.io/v2` |

### `fi:segment`

Ein Feldbus-Segment (physisches Netz).

| Attribut | Pflicht | Typ | Beschreibung |
|----------|---------|-----|--------------|
| `id` | ja | UUID | Eindeutige Segment-ID |
| `protocol` | ja | String | Protokoll: `modbustcp`, `modbusrtu`, `ethercat`, `profibus` |
| `name` | ja | String | Anzeigename (frei waehlbar) |
| `enabled` | nein | Bool | Segment aktiv (`true`) oder deaktiviert (`false`). Standard: `true` |
| `interface` | nein | String | Netzwerk-Interface (z.B. `eth0`, `/dev/ttyUSB0`) |
| `bindAddress` | nein | String | IP/CIDR fuer das Interface (z.B. `192.168.24.100/24`) |
| `gateway` | nein | String | Gateway-Adresse (leer = kein Gateway) |
| `pollIntervalMs` | nein | Int | Abfrageintervall in Millisekunden (`0` = so schnell wie moeglich) |

### `fi:device`

Ein Geraet innerhalb eines Segments.

| Attribut | Pflicht | Typ | Beschreibung |
|----------|---------|-----|--------------|
| `hostname` | ja | String | Geraetename (wird als Device-ID verwendet) |
| `ipAddress` | nein | String | IP-Adresse (Modbus TCP) |
| `port` | nein | Int | TCP-Port (Standard: `502`) |
| `slaveId` | nein | Int | Modbus Slave-ID |
| `anvilGroup` | nein | String | Anvil-IPC-Gruppe fuer Zero-Copy-Transport |

## Variable-zu-Device-Verknuepfung

I/O-Variablen werden **nicht** im `fi:device`-Element aufgelistet.
Stattdessen traegt jede Variable im Adress-Pool ein `busBinding`-Attribut,
das auf den `hostname` des Devices zeigt:

```
FLocatedVariable
  name: "DI_1"
  address: "%IX0.0"
  anvilGroup: "Maibeere"
  busBinding:
    deviceId: "Maibeere"
    modbusAddress: 0
    count: 1
```

Diese Trennung ist redundanzfrei: das Device kennt seine Variablen nicht
direkt, aber alle Variablen eines Devices lassen sich ueber das Binding
filtern.

## IEC-Adressvergabe

Die IEC-Adresse einer gebundenen Variable ergibt sich aus der physischen
Topologie:

```
Segment-Basis + Device-Offset + Register-Position
```

| Adressbereich | Bedeutung | Herkunft |
|---------------|-----------|----------|
| `%IX` / `%IW` / `%ID` | Physischer Eingang | Bus-Binding |
| `%QX` / `%QW` / `%QD` | Physischer Ausgang | Bus-Binding |
| `%MX` / `%MW` / `%MD` | Merker (kein physisches I/O) | Pool-Allokator |

Beim **Binden** einer Variable an ein Device wechselt die Adresse von
`%M*` (Merker) nach `%I*` oder `%Q*` (physisch). Beim **Entbinden**
erhaelt die Variable automatisch eine freie Merker-Adresse.

## Unterstuetzte Protokolle

| Protokoll | `protocol`-Wert | Medium | Bridge-Daemon |
|-----------|----------------|--------|---------------|
| Modbus TCP | `modbustcp` | Ethernet | `tongs-modbustcp` |
| Modbus RTU | `modbusrtu` | RS-485 (seriell) | `tongs-modbusrtu` |
| EtherCAT | `ethercat` | Ethernet (Echtzeit) | `tongs-ethercat` |
| Profibus DP | `profibus` | Seriell (Feldbus) | `tongs-profibus` |

## Kompatibilitaet

Das Attribut `handleUnknown="discard"` stellt sicher, dass PLCopen-
konforme Werkzeuge, die ForgeIEC nicht kennen, die Bus-Konfiguration
ignorieren koennen ohne Fehler zu erzeugen. Umgekehrt liest ForgeIEC
unbekannte `<addData>`-Bloecke anderer Hersteller und bewahrt sie
beim Speichern.

---

<div style="text-align:center; padding: 2rem;">

**ForgeIEC Bus-Konfiguration — Offline-faehig, PLCopen-konform, redundanzfrei.**

blacksmith@forgeiec.io

</div>
