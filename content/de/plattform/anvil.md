---
title: "Anvil"
description: "Echtzeit-SPS-Laufzeitumgebung mit Zero-Copy IPC und Feldbus-Bridge-Management"
weight: 2
---

## Der Amboss

In jeder Schmiede ist der Amboss das zentrale Werkstück — hier wird geformt,
gehärtet und veredelt. **Anvil** ist die Laufzeitumgebung der
ForgeIEC-Plattform: der Ort, an dem Quellcode auf Echtzeitausführung trifft.

Anvil verwaltet den SPS-Scan-Zyklus, die Prozessabbilder und den
Datenaustausch zwischen dem SPS-Programm und den Feldbus-Bridges. Der
Laufzeit-Daemon, der **Anvil-Server (anvild)**, ist das Herzschlag-gebende
Element jeder ForgeIEC-Installation. (Das Programm heißt seit
September 2026 `anvil-server`, der Dienst `forgeiec-anvil-server.service`.)

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
   +------------------+            ^             |  Prozess)        |
                                   |             +------------------+
                             +-----------+
                             |  Hearth   |  Bedienoberfläche (Vorschau)
                             +-----------+
```

Der SPS-Zyklus läuft als eigener Prozess `forgeiec_plc`; anvild
startet ihn und die Bridges, nimmt die Befehle des Studios entgegen
und überwacht alles.

---

## Echtzeit-Scan-Zyklus

Der SPS-Kern arbeitet in einem deterministischen Scan-Zyklus:

1. **Eingaben lesen** — Prozessabbild aus den Feldbus-Bridges übernehmen
2. **Programm ausführen** — IEC-Code abarbeiten
3. **Ausgaben schreiben** — Ergebnisse an die Bridges verteilen

Der Zyklus läuft mit konfigurierbarer Zykluszeit. Anvil garantiert
deterministisches Verhalten ohne dynamische Speicherallokation im Hot Path.

---

## Anvil Technology -- Zero-Copy IPC

Der Datenaustausch zwischen `anvild` und den Protocol-Bridges erfolgt
über **Anvil Technology** — einen hochperformanten IPC-Kanal auf Basis
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

Die PUBLISH/SUBSCRIBE-Schlüsselwörter sind eine ForgeIEC-Erweiterung des
IEC 61131-3 Standards. Der Compiler erzeugt automatisch die Anvil-Anbindung.
Im Editor werden die zugehörigen VAR_ANVIL-Blöcke automatisch generiert
und synchronisiert.

---

## Bridge-Management

`anvild` startet, überwacht und verwaltet alle Feldbus-Bridges als
Subprozesse:

- **Ein Prozess pro Segment** — Isolation und unabhängiger Betrieb
- **Automatischer Neustart** — abgestürzte Bridges werden erkannt und
  neu gestartet
- **Konfiguration via TOML** — `config.toml` definiert Segmente, Geräte
  und Verbindungsparameter
- **gRPC-Schnittstelle** — Forge Studio steuert den Daemon remote

---

## Kompilierung

Die Kompilierung folgt einem zweistufigen Modell:

1. **Workstation**: Forge Studio übersetzt den IEC-Code mit dem
   eigenen Compiler-Kern in C++-Quelltext
2. **Zielsystem**: `anvild` generiert ein plattformspezifisches Makefile
   und ruft `make` (g++) auf

Auf dem Zielsystem werden lediglich `make`, `g++`, `libstdc++` und
`librt` benötigt, um den generierten C++-Code zur Laufzeit zu
kompilieren. Es wird bewusst kein zusätzlicher IEC-Compiler auf der
Ziel-SPS installiert.

---

## Technische Details

| Eigenschaft | Wert |
|-------------|------|
| **Sprache** | Rust |
| **Kommunikation** | gRPC (tonic/prost) |
| **IPC** | Anvil-Bus (iceoryx2, Zero-Copy Shared Memory) |
| **Konfiguration** | TOML |
| **Plattformen** | x86_64, ARM64, ARMv7 (Linux) |
| **Prozessmodell** | systemd-Daemon + Subprozesse |
| **Lizenz** | AGPL-3.0-or-later; Runtime-API, libanvil und generierter Code: Apache-2.0 |

---

## Ansichten

{{< screenshot program="studio" name="plc-stats" alt="Laufzeitstatistik der Steuerung im Studio" caption="Laufzeitstatistik: Zustand, Programm, Laufzeit und Zykluswerte, live." >}}


<div style="text-align:center; padding: 2rem;">

**Anvil — Wo Daten zu Steuerbefehlen geschmiedet werden.**

blacksmith@forgeiec.io

</div>
