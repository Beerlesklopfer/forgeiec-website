---
title: "Anvil"
description: "Echtzeit-SPS-Laufzeitumgebung mit Zero-Copy IPC und Feldbus-Bridge-Management"
weight: 2
---

## Der Amboss

In jeder Schmiede ist der Amboss das zentrale Werkstueck — hier wird geformt,
gehaertet und veredelt. **Anvil** ist die Laufzeitumgebung der
ForgeIEC-Plattform: der Ort, an dem Quellcode auf Echtzeitausfuehrung trifft.

Anvil verwaltet den SPS-Scan-Zyklus, die Prozessabbilder und den
Datenaustausch zwischen dem SPS-Programm und den Feldbus-Bridges. Der
Laufzeit-Daemon `anvild` ist das Herzschlag-gebende Element jeder
ForgeIEC-Installation.

---

## Architektur

```
+--------------+         +------------+         +------------------+
|              |         |            |         |                  |
| SPS-Programm |<------->|  anvild    |<------->|  Modbus-Bridge   |--> Feldgeraete
|  (IEC Code)  |  gRPC   |  (Daemon)  |  Anvil  |  EtherCAT-Bridge |--> Antriebe
|              |         |            |  SHM    |  Profibus-Bridge  |--> Sensoren
+--------------+         +------------+         |  OPC-UA-Bridge   |--> SCADA
                                                +------------------+

                         <-- Anvil -->
                         Zero-Copy IPC
                         Shared Memory
```

---

## Echtzeit-Scan-Zyklus

Der SPS-Kern arbeitet in einem deterministischen Scan-Zyklus:

1. **Eingaben lesen** — Prozessabbild aus den Feldbus-Bridges uebernehmen
2. **Programm ausfuehren** — IEC-Code abarbeiten
3. **Ausgaben schreiben** — Ergebnisse an die Bridges verteilen

Der Zyklus laeuft mit konfigurierbarer Zykluszeit. Anvil garantiert
deterministisches Verhalten ohne dynamische Speicherallokation im Hot Path.

---

## Anvil Technology -- Zero-Copy IPC

Der Datenaustausch zwischen `anvild` und den Protocol-Bridges erfolgt
ueber **Anvil Technology** — einen hochperformanten IPC-Kanal auf Basis
von Zero-Copy Shared Memory:

- **Mikrosekunden-Latenz** — keine Serialisierung, keine Kopien
- **Lock-freie Algorithmen** — kein Blockieren, kein Deadlock
- **Publish/Subscribe-Modell** — lose Kopplung zwischen Produzent und Konsument
- **Ein Kanal pro Segment** — Isolation zwischen Bussystemen

| Methode | Typische Latenz | Kopien |
|---------|----------------|--------|
| TCP Socket | 50-200 us | 2-4 |
| Unix Socket | 10-50 us | 2 |
| **Anvil Technology** | **< 1 us** | **0** |

---

## PUBLISH/SUBSCRIBE im IEC-Programm

Anvil Technology integriert sich nahtlos in die IEC 61131-3 Programmierung:

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

Die PUBLISH/SUBSCRIBE-Schluesselwoerter sind eine ForgeIEC-Erweiterung des
IEC 61131-3 Standards. Der Compiler erzeugt automatisch die Anvil-Anbindung.
Im Editor werden die zugehoerigen VAR_ANVIL-Bloecke automatisch generiert
und synchronisiert.

---

## Bridge-Management

`anvild` startet, ueberwacht und verwaltet alle Feldbus-Bridges als
Subprozesse:

- **Ein Prozess pro Segment** — Isolation und unabhaengiger Betrieb
- **Automatischer Neustart** — abgestuerzte Bridges werden erkannt und
  neu gestartet
- **Konfiguration via TOML** — `config.toml` definiert Segmente, Geraete
  und Verbindungsparameter
- **gRPC-Schnittstelle** — Forge Studio steuert den Daemon remote

---

## Kompilierung

Die Kompilierung folgt einem zweistufigen Modell:

1. **Workstation**: Forge Studio fuehrt `iec2c` aus (IEC 61131-3 nach C)
2. **Zielsystem**: `anvild` generiert ein plattformspezifisches Makefile
   und ruft `make` (g++) auf

Kein Compiler auf der SPS erforderlich. Die Workstation uebernimmt die
rechenintensive Arbeit.

---

## Technische Details

| Eigenschaft | Wert |
|-------------|------|
| **Sprache** | Rust |
| **Kommunikation** | gRPC (tonic/prost) |
| **IPC** | Anvil Technology (Zero-Copy Shared Memory) |
| **Konfiguration** | TOML |
| **Plattformen** | x86_64, ARM64, ARMv7 (Linux) |
| **Prozessmodell** | systemd-Daemon + Subprozesse |

---

<div style="text-align:center; padding: 2rem;">

**Anvil — Wo Daten zu Steuerbefehlen geschmiedet werden.**

blacksmith@forgeiec.io

</div>
