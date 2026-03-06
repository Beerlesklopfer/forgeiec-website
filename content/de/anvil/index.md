---
title: "Anvil Technology\u00ae"
summary: "Auf unserem Amboss werden Ihre Daten geschmiedet"
---

## Der Amboss: Herzstück jeder Schmiede

In jeder Schmiede ist der Amboss das zentrale Werkstück — hier wird geformt,
gehärtet und veredelt. **Anvil Technology\u00ae** ist die Zwischenschicht zwischen dem
SPS-Laufzeitsystem und den Feldbus-Bridges. Hier werden Ihre Prozessdaten
geschmiedet: empfangen, transformiert und an die richtigen Empfänger verteilt.

Anvil nutzt intern eine proprietäre Zero-Copy Shared-Memory-Transportschicht
für inter-Prozess-Kommunikation. Keine Serialisierung, keine Kopien,
keine Kompromisse.

---

## Architektur

```
┌──────────────┐         ┌────────────┐         ┌──────────────────┐
│              │         │            │         │                  │
│ SPS-Programm │◄───────►│  forgeiecd  │◄───────►│  Modbus-Bridge   │──► Feldgeräte
│  (IEC Code)  │  gRPC   │  (Daemon)  │  Anvil  │  EtherCAT-Bridge │──► Antriebe
│              │         │            │ Anvil   │  Profibus-Bridge  │──► Sensoren
└──────────────┘         └────────────┘         │  OPC-UA-Bridge   │──► SCADA
                                                └──────────────────┘

                         ◄── Anvil ──►
                         Zero-Copy IPC
                         Shared Memory
```

Der Datenaustausch zwischen `forgeiecd` und den Protocol-Bridges erfolgt
über **Anvil Technology\u00ae** — einen hochperformanten IPC-Kanal auf Basis von Zero-Copy
Shared Memory. Jedes Segment erhält seinen eigenen Kommunikationskanal.

---

## Warum Anvil Technology\u00ae?

### Mikrosekunden-Latenz

Konventionelle IPC-Mechanismen (Pipes, Sockets, Message Queues) kopieren
Daten zwischen Prozessen. Anvil eliminiert jede Kopie. Die Daten liegen
in gemeinsamem Speicher — der Empfänger liest direkt.

| Methode | Typische Latenz | Kopien |
|---------|----------------|--------|
| TCP Socket | 50–200 µs | 2–4 |
| Unix Socket | 10–50 µs | 2 |
| **Anvil Technology\u00ae** | **< 1 µs** | **0** |

### Industriequalität

- Deterministisches Verhalten — keine dynamische Speicherallokation im Hot Path
- Lock-freie Algorithmen — kein Blockieren, kein Deadlock
- Publish/Subscribe-Modell — lose Kopplung zwischen Produzent und Konsument
- Automatische Lebenszyklusverwaltung — Bridges werden überwacht und bei Absturz neu gestartet

### PUBLISH/SUBSCRIBE im IEC-Programm

Anvil Technology\u00ae integriert sich nahtlos in die IEC 61131-3 Programmierung:

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

Anvil Technology\u00ae verbindet das SPS-Programm mit allen industriellen Feldbussen:

| Protokoll | Bridge | Status |
|-----------|--------|--------|
| **Modbus TCP** | `forgeiec-modbustcp` | Verfügbar |
| **Modbus RTU** | `forgeiec-modbusrtu` | Verfügbar |
| **EtherCAT** | `forgeiec-ethercat` | In Entwicklung |
| **Profibus DP** | `forgeiec-profibus` | In Entwicklung |
| **OPC-UA** | `forgeiec-opcua` | Geplant |

Jede Bridge läuft als eigenständiger Prozess. `forgeiecd` startet, überwacht
und restartet Bridges automatisch. Ein Absturz einer Bridge beeinträchtigt
weder die SPS noch andere Bridges.

---

## Technische Details

- **IPC-Framework**: Anvil Technology\u00ae (proprietäres Zero-Copy Shared Memory)
- **Architektur**: Ein Publisher/Subscriber-Kanal pro Bus-Segment
- **Datenformat**: Rohe IEC-Variablen — keine Serialisierung, kein Overhead
- **Plattformen**: x86_64, ARM64, ARMv7 (Linux)
- **Prozessmodell**: Ein Bridge-Prozess pro aktivem Segment

---

<div style="text-align:center; padding: 2rem;">

**Anvil Technology\u00ae — Wo Daten zu Steuerbefehlen geschmiedet werden.**

blacksmith@forgeiec.io

</div>
