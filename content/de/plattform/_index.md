---
title: "Plattform"
description: "Die ForgeIEC-Plattform — die Werkzeuge der Schmiede, jedes mit klarem Auftrag"
weight: 10
---

> **Neu hier?** [Der ForgeIEC-Verbund](verbund/) erklärt das Ganze in einem
> Zug: das Bild, die Begriffe, die drei Wege und die Fallen — der Einstieg,
> bevor die Einzelseiten unten Sinn ergeben.

## Was die Plattform leistet

ForgeIEC ist eine vollständige Plattform für industrielle
Automatisierung — von der Programmierung bis zum Leitsystem. Jede
Komponente trägt den Namen eines Schmiedewerkzeugs und hat einen
klar umrissenen Auftrag. Komponenten sind eigenständige Daemonen
bzw. Anwendungen, gemeinsam laufen sie über Zero-Copy-IPC und
gRPC.

| | Komponente | Auftrag | Stand |
|:---:|---|---|---|
| {{< comp-icon "studio" >}}   | **ForgeIEC Studio** | IEC-61131-3-IDE + Bus-Konfig + KI-Helfer | produktiv |
| {{< comp-icon "anvild" >}}   | **anvild**          | PLC-Runtime + Anvil-Zero-Copy-IPC zwischen Subsystemen | produktiv |
| {{< comp-icon "bellowsd" >}} | **bellowsd**        | OPC-UA / HMI-Gateway | in Arbeit |
| {{< comp-icon "tongs" >}}    | **tongs-***         | Feldbus-Bridges (Modbus / EtherCAT / Profibus / EthernetIP) | gemischt |
| {{< comp-icon "screen" >}}   | **Screen**          | Industrieller Kiosk-Browser (Bedienpanel) | produktiv |
| {{< comp-icon "hearth" >}}   | **Hearth**          | IIoT-Subscriber / SCADA-Schicht | in Arbeit |
| {{< comp-icon "ledger" >}}   | **Ledger**          | Auftragsverwaltung / MES-Integration | in Planung |

---

## Die Komponenten

### 🛠️ ForgeIEC Studio — die Werkbank

{{< components "studio" >}}

Native C++/Qt6-IDE auf der Workstation. Alle fünf IEC-Sprachen
(ST + IL + FBD + LD + SFC), Bus-Konfiguration, Live-Monitor,
Oszilloskop, KI-Helfer eingebaut. Tree-sitter-basierte Syntax,
gRPC-Anbindung an anvild, MCP-Server für LLM-Tooling.

[Mehr erfahren](forge-studio/)

### 🔥 anvild — die Runtime + Anvil-IPC

{{< components "anvild" >}}

Rust/Tokio-Daemon auf der Ziel-SPS. Multi-Task-Scheduler mit
pthread-Parallelität, deterministische Scan-Cycles, gRPC-Listener
für das Studio, Subprozess-Manager für die Bus-Bridges.

Eingebaut ist **Anvil** — die Zero-Copy-Shared-Memory-Schicht
zwischen Runtime, Bridges und externen Subscribern. ABI-Probe gegen
Type-Hash-Drift; Segmente abgestürzter Peers werden automatisch
zurückgeholt, ohne lebende Peers anzutasten. Wire-Protokoll für
Status, I/O, Diagnostik.

[Mehr erfahren](anvil/)

### 🌬️ bellowsd — der Blasebalg

{{< components "bellowsd" >}}

OPC-UA-Server + Modbus-TCP-Server für HMI-Anbindung. Exportiert
Pool-Variablen mit `bellows_export`-Flag als OPC-UA-Knoten +
Modbus-Coils. Pro Variable einzeln gegated.

[Mehr erfahren](bellows/)

### 🔧 tongs-* — die Feldbus-Zangen

{{< components "tongs,anvild" >}}

Pro Protokoll ein eigener Daemon. Einheitliches Fault-Modell
(`OK/WARN/FAULT/OFFLINE/UNKNOWN`), FDD-getriebene Diagnose-Bits,
Anvil-Zero-Copy-IPC zur Runtime. Modbus-TCP produktiv; EtherCAT,
Profibus und EtherNet/IP in Arbeit.

[Mehr erfahren](tongs/)

### 🖥️ Screen — der Kiosk-Browser

{{< components "screen" >}}

CEF-basierter Industrie-Kiosk-Browser (Chromium Embedded Framework
+ Rust + winit). Läuft fullscreen auf Bedienpanels, öffnet eine
beliebige Web-HMI (Bellows / Hearth / 3rd-party). Integrierter
Rocket-Web-Server für Settings (Netz, WireGuard, Zeitzone,
80+ Sprachen), D-Bus-Backend für NetworkManager / timedated /
localed.

[Mehr erfahren](screen/)

### 🏠 Hearth — der Herd

{{< components "hearth" >}}

IIoT-Subscriber + SCADA-Schicht. Subscribet Anvil-Topics — anvild
legt den passenden Descriptor dafür unter
`/etc/forgeiec/hearth/descriptor.toml` ab. Als Paket
`hearth-server` im APT-Repository verfügbar. Geplant:
Time-Series-DB-Anbindung (InfluxDB, TimescaleDB), Mosquitto-MQTT-
Bridge, Alarm-Management, Grafana-Dashboards.

[Mehr erfahren](hearth/)

### 📒 Ledger — das Auftragsbuch

{{< components "ledger" >}}

Auftragsverwaltung + MES-Integration. Plant: Produktionsaufträge,
Stückzahl-Tracking, Rückverfolgbarkeit (Material → Charge →
Produkt), Schichtbuch, Brücke zu ERP-Systemen. In Planung — kommt
nach Hearth.

[Mehr erfahren](ledger/)

---

## Wie die Komponenten zusammenspielen

```mermaid
flowchart LR
    Studio[ForgeIEC Studio<br/>IDE + KI]
    Anvild[anvild<br/>Runtime]
    Bridges["tongs-*<br/>Feldbus-Bridges"]
    Bellows[bellowsd<br/>HMI Gateway]
    Screen[Screen<br/>Kiosk-Browser]
    Hearth[Hearth<br/>IIoT / SCADA]
    Ledger[Ledger<br/>MES]

    Studio -.->|gRPC| Anvild
    Anvild -->|Anvil IPC| Bridges
    Anvild -->|Anvil IPC| Bellows
    Anvild -->|Anvil IPC| Hearth
    Bellows -->|OPC-UA / Modbus| Hearth
    Hearth -->|HTTP| Screen
    Hearth -.->|REST| Ledger
```

Studio sitzt auf der Workstation, alles andere auf den Ziel-
Systemen. Workstations + Ziel-Systeme können über das
[Team-Federation-Modell](/news/federation-team-trust/) miteinander
verbunden werden — mehrere Workstations sehen ihre Anlagen.

---

## Open Source + Aufbauend auf Vorgängern

Alle Komponenten sind **AGPL-3.0**. Der Source liegt im Forgejo
unter `git.forgeiec.io` — die Repositories sind nicht öffentlich
einsehbar, der Zugriff läuft über SSH nach Freischaltung Ihres
SSH-Public-Keys (siehe [Partner](/de/partner/)). Build
reproduzierbar über CPack — signiertes APT-Repository für
Debian/Ubuntu, signiertes RPM-Repository für AlmaLinux 9 und
Fedora 44.

ForgeIEC steht auf den Schultern von **OpenPLC** (Thiago Alves,
seit 2018) und behält Datei-Kompatibilität zu OpenPLC-Projekten.
Lesen Sie die [Founding-Story](/news/die-forgeiec-geschichte/) für
den vollen Werdegang vom OpenPLC-Fork zur eigenständigen
Plattform.

---

<div style="text-align:center; padding: 2rem;">

**Die Werkzeuge der Schmiede. Open by default.**

blacksmith@forgeiec.io

</div>
