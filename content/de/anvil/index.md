---
title: "Anvil-Bus"
summary: "Auf unserem Amboss werden Ihre Daten geschmiedet"
---

## Der Amboss: Herzstück jeder Schmiede

In jeder Schmiede ist der Amboss das zentrale Werkstück — hier wird geformt,
gehärtet und veredelt. **Anvil** ist die Zwischenschicht zwischen dem
SPS-Laufzeitsystem und den Feldbus-Bridges. Hier werden Ihre Prozessdaten
geschmiedet: empfangen, transformiert und an die richtigen Empfänger verteilt.

Anvil nutzt intern eine Zero-Copy-Shared-Memory-Transportschicht auf Basis
von iceoryx2 für die Kommunikation zwischen den Prozessen. Keine Serialisierung, keine Kopien,
keine Kompromisse.

---

## Architektur

```
 Workstation              Steuerung (Linux)
+-----------+  gRPC  +---------------------+
|  Studio   |------->|  Anvil-Server       |  startet und überwacht
+-----------+        |  (anvild)           |-----------------------+
                     +---------------------+                       |
                                                                   v
   +------------------+   Anvil-Bus (iceoryx2,   +------------------+
   | forgeiec_plc     |<------------------------>| tongs-* Bridges  |--> Feldgeräte
   | (SPS-Zyklus)     |   Zero-Copy Shared Mem.) | (je Segment ein  |
   +------------------+                          |  Prozess)        |
                                                 +------------------+
```

Der Datenaustausch zwischen dem SPS-Zyklus (`forgeiec_plc`), dem Anvil-Server (anvild) und den Protocol-Bridges erfolgt
über **Anvil** — einen hochperformanten IPC-Kanal auf Basis von Zero-Copy
Shared Memory. Jedes Segment erhält seinen eigenen Kommunikationskanal.

---

## Warum Anvil?

### Mikrosekunden-Latenz

Konventionelle IPC-Mechanismen (Pipes, Sockets, Message Queues) kopieren
Daten zwischen Prozessen. Anvil eliminiert jede Kopie. Die Daten liegen
in gemeinsamem Speicher — der Empfänger liest direkt.

| Methode | Typische Latenz | Kopien |
|---------|----------------|--------|
| TCP Socket | 50–200 µs | 2–4 |
| Unix Socket | 10–50 µs | 2 |
| **Anvil** | **< 1 µs** | **0** |

### Auf den Betrieb ausgelegt

- Deterministisches Verhalten — keine dynamische Speicherallokation im Hot Path
- Lock-freie Algorithmen — kein Blockieren, kein Deadlock
- Publish/Subscribe-Modell — lose Kopplung zwischen Produzent und Konsument
- Automatische Lebenszyklusverwaltung — Bridges werden überwacht und bei Absturz neu gestartet

### PUBLISH/SUBSCRIBE im IEC-Programm

Anvil integriert sich nahtlos in die IEC 61131-3 Programmierung:

```iec
VAR_GLOBAL PUBLISH 'Motoren'
    K1_Mains    AT %QX0.0 : BOOL;
    K1_Speed    AT %QW10  : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Sensoren'
    Temperatur  AT %IW0   : INT;
    Druck       AT %IW2   : INT;
END_VAR
```

Die PUBLISH/SUBSCRIBE-Schlüsselwörter sind eine ForgeIEC-Erweiterung des
IEC 61131-3 Standards. Der Compiler erzeugt automatisch die Anvil-Anbindung.

---

## Unterstützte Protokolle

Anvil verbindet das SPS-Programm mit den Feldbus-Bridges:

| Protokoll | Bridge | Status |
|-----------|--------|--------|
| **Modbus TCP** | `tongs-modbustcp` | {{< status "use" "verfügbar" >}} |
| **Modbus RTU** | `tongs-modbusrtu` | {{< status "use" "verfügbar" >}} |
| **LoRaWAN** | `tongs-lorawan` | {{< status "wip" "in Arbeit (Schwerpunkt)" >}} |
| **EtherCAT** | `tongs-ethercat` | {{< status "wip" "Gerüst, in Arbeit" >}} |
| **PROFIBUS DP** | `tongs-profibus` | {{< status "wip" "Gerüst, in Arbeit" >}} |
| **EtherNet/IP** | `tongs-ethernetip` | {{< status "wip" "Gerüst, in Arbeit" >}} |

Jede Bridge läuft als eigenständiger Prozess. `anvild` startet, überwacht
und restartet Bridges automatisch. Ein Absturz einer Bridge beeinträchtigt
weder die SPS noch andere Bridges.

---

## Technische Details

- **IPC-Framework**: Anvil-Bus (iceoryx2, Zero-Copy Shared Memory)
- **Architektur**: Ein Publisher/Subscriber-Kanal pro Bus-Segment
- **Datenformat**: Rohe IEC-Variablen — keine Serialisierung, kein Overhead
- **Plattformen**: x86_64, ARM64, ARMv7 (Linux)
- **Prozessmodell**: Ein Bridge-Prozess pro aktivem Segment

---

<div style="text-align:center; padding: 2rem;">

**Anvil — wo Daten zu Steuerbefehlen geschmiedet werden.**

blacksmith@forgeiec.io

</div>
