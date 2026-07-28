---
title: "Vom ersten Byte an: die ForgeIEC-Geschichte"
date: 2026-05-13
weight: 1
summary: "Wie aus einem OpenPLC-Fork eine eigenstaendige IEC-61131-3-Plattform wurde — und warum"
components: [studio, anvild, bellowsd, tongs]
---

{{< components "studio,anvild,bellowsd,tongs" >}}

## 2018: Der Anfang — OpenPLC

Der erste Commit dieses Repositorys traegt das Datum
**14. Juni 2018**. Damals heisst das Projekt nicht ForgeIEC,
sondern **OpenPLC v3 beta 1** — eine offene SPS-Runtime von
**Thiago Alves**, geschrieben in C/C++ mit einer Web-basierten
Konfigurations-Oberflaeche in Python/Flask.

OpenPLC hat einen klaren Wert: Sie koennen IEC 61131-3-Code
(Strukturierter Text + die anderen vier Sprachen) auf normaler
Linux-Hardware ausfuehren, ohne kommerzielle Editor-Lizenz, ohne
Hersteller-Bindung. Das war revolutionaer. Modbus-Master, GPIO,
RaspberryPi-Support — alles drin.

Was OpenPLC nicht hat: einen ernsthaften **Editor**. Die Web-UI
ist gut fuer kleine Projekte, aber bei industrieller Komplexitaet
faellt sie zurueck.

---

## 2019–2024: Die Latenz-Jahre

Zwischen 2019 und Anfang 2025 passiert nicht viel: kleine Bugfixes
(Modbus-Buffer-Overflow, libmodbus-Fork, Webserver-Tweaks),
aber kein grosser Sprung. Das ist die Realitaet von Open-Source-
Projekten — solange niemand investiert, stagniert es.

Wir lernen in diesen Jahren: **das Fundament traegt**. Die
matiec-Compiler-Toolchain ist solide, der IEC-Code-Generator
funktioniert, die Runtime laeuft zuverlaessig auf x86 + ARM.
Was fehlt ist alles **drumherum** — Editor, Bus-System,
Diagnose-Werkzeuge, Hersteller-Daten-Integration.

---

## 2026-03-01: Der grosse Umbau beginnt

Mit dem Commit
[`82780f7`](https://git.forgeiec.io/ForgeIEC/forgeiec-studio/commit/82780f7)
am **1. Maerz 2026** kommt der naechste Schritt: ein
**eigenstaendiger C++/Qt6-Editor** wird ins Repository
eingefuehrt. Native Desktop-Anwendung, kein Browser, kein
Python-Flask im UI-Pfad mehr.

Gleichen Tag der naechste Brocken: **gRPC-Client im Editor**, plus
das Backend wird zu `forgeiecd` umbenannt (commit
[`93ed9c9`](https://git.forgeiec.io/ForgeIEC/forgeiec-studio/commit/93ed9c9)).
Die alte HTTP-Webserver-Bedienung weicht einer modernen
**gRPC-Pipeline** mit Streaming + Protokoll-Versionierung.

Die naechsten Tage taktet es eng:

- **3. Maerz** — Bus-System, Model/View-Refactor, F-Prefix-Renames
  (commit `dd85396`)
- **4. Maerz** — EtherCAT + Profibus Bridges, CMake-Migration
- **5. Maerz** — Hugo-Website als Submodul angelegt
- **6. Maerz** — **DEL → Anvil**: das Shared-Memory-IPC-Subsystem
  bekommt seinen Industrie-Namen (commit `3fc636c`)
- **7. Maerz** — **Forge Studio Branding**, Bridge-Family
  `anvil-*` benannt, Dirty-Bit-Verwaltung, BusModel MVC

In **eine Woche** wird aus einer Web-UI-Toolbox ein
**eigenstaendiger Desktop-Editor mit moderner Architektur**.

---

## Maerz–April 2026: Die Architektur konsolidiert sich

Es folgen mehrere Wochen tiefer Refactor-Arbeit:

- **Debian-Pakete + CPack** (26. Maerz) — kein manuelles
  Installations-Skript mehr
- **Multi-Task-Scheduler** (11. April) — IEC-Tasks laufen jetzt
  echt parallel, pthread-basiert
- **Bus-Panel-Merge** (13. April) — getrennte Sichten auf das
  gleiche Modell zusammengelegt
- **-1416 LOC Refactor** (16. April) — FBusDeviceDialog
  rausgeworfen, Bus-Spalten konsolidiert
- **`FVariableBase` + `FLocatedVariable` → `FVariable`** (26. April)
  — der zentrale Variablen-Typ wird vereinheitlicht

Hier passiert das Wichtigste was man als Anwender **nicht**
sieht: das **Daten-Modell** wird so umgebaut, dass es echte
industrielle Komplexitaet traegt. `FAddressPool` als Single-Source-
of-Truth, Pool-Variablen als der einzige Container, alte
POU-VarLists nur noch als Spiegel.

Das ist die Grundlage dafuer dass spaeter die KI-Schicht
verlaesslich operieren kann — sie sieht ein **konsistentes
Modell**, nicht eine Sammlung legacy gewachsener Datenstrukturen.

---

## Mai 2026: Sicherheit + KI

Mit dem Datenmodell stabil koennen die big-ticket-Sprints kommen:

- **2. Mai** — **Per-Variable Safety-Flags** (Cluster A): Force,
  Monitor, HMI-Export werden pro Variable einzeln gegated.
  Spaeter wird daraus die 3-Layer-Sicherheits-Architektur.
- **8. Mai** — **MCP-Plattform**: Spec geschrieben, Sprint MCP-1
  (Prompts in QSettings).
- **9. Mai** — **Live-Diagnose-Pipeline** — FB-Member-Resolution,
  FLiveValueStore-Lifecycle-Fix.
- **10. Mai** — **Headless-Modus + Devloop-CLI** — fuer
  CI/Build-Server. Codegen.deploy wird scriptable.
- **11. Mai** — **MCP-3.6**: Chat-Tab wird interner MCP-Client.
- **12. Mai** — **MCP-4a + 4b Phase A–D**: Remote-Bind, Bearer-
  Auth, Trust-Store, mTLS, Caretaker-Modell.

Damit ist der **technische Sprung** komplett: ForgeIEC ist
nicht mehr nur ein offener IEC-61131-3-Editor, sondern eine **eigene
Plattform** mit Federation, KI-Integration und nachvollziehbaren
Sicherheits-Schichten.

---

## Heute, 13. Mai 2026: Wo wir stehen

Die Plattform ist aufgeteilt in vier Subsysteme, jedes mit eigener
Spec im
[`documentation/architecture/`](https://git.forgeiec.io/ForgeIEC/forgeiec-studio)-
Verzeichnis:

| Subsystem | Spec | Rolle |
|---|---|---|
| **ForgeIEC Studio** | `mcp-platform-v1.md` | IDE — Editor + KI-Helfer + MCP-Server |
| **anvild** | `anvil-platform-v2.md` | PLC-Runtime + Plug-In-Plattform + Online-Change |
| **Anvil (IPC)** | (in anvil-platform-v2 §13) | Zero-Copy-Shared-Memory zwischen Subsystemen |
| **tongs-* (Bridges)** | `tongs-platform-v1.md` | Feldbus-Plug-ins mit Fault-Model + FDD-Diag-Bits |
| **Bus-System** | `bus-system-v1.md` | Segmente/Devices/IEC-Zugriff |
| **Editor-Datenmodell** | `editor-data-v1.md` | FAddressPool SSoT + .forge-Format |
| **Codegen** | `codegen-v1.md` | C-Output + matiec-Interop |

Alle Specs RFC-2119-normativ. Code + Spec gehen synchron — jede
Aenderung durchlaeuft denselben Review-Prozess.

---

## Was ForgeIEC anders macht

| Andere | ForgeIEC |
|---|---|
| Proprietaere SPS-IDEs | Vollstaendig Open-Source (AGPL-3.0) |
| Vendor-Lock-in fuer Geraete | Hersteller-FDDs als First-Class-Citizen |
| KI nur als Code-completion-Plugin | KI als gleichberechtigter MCP-Client mit Audit-Log |
| Force-Setzungen ohne Schutzschicht | 4-Layer-Defense pro Variable |
| Monolithische Runtime | Modulare Bridge-Familie mit getrennten Daemons |
| Closed-Source-Binaries | Build aus Quellcode reproduzierbar, signiert per APT |

---

## Wo es hingeht

Auf dem Sprint-Plan stehen:

- **Caretaker-Toggle-UI** in den Preferences — heute noch
  QSettings-Editieren
- **`team.revoke_peer` voll**, `team.rotate_cert`,
  `team.export_setup` — letzte Drittel der MCP-4b Phase-D
- **Anvil-Plattform v2**: Online-Change waehrend laufender
  PLC-Cycle, Plug-In-Architektur fuer eigene Boundary-Typen
- **Codegen-v1 → v2**: Migration der C-Code-Generierung nach
  Rust+LLVM (rusty-Backend) — Determinismus-Garantien +
  Online-Change-Vorbereitung
- **Hearth** — der naechste Subsystem-Baustein fuer IIoT-
  Subscriber (Mosquitto-Cloud, Time-Series-DB)
- **Tongs-EtherCAT, Tongs-Profibus, Tongs-EthernetIP** voll
  implementiert

Der rote Faden bleibt: **eine offene, ehrliche Plattform** die
mit der industriellen Realitaet umgehen kann — keine bunten
Versprechen, kein Marketing-Lack, sondern belastbare Architektur-
Entscheidungen die in der Spec stehen und die Sie im Source nach-
pruefen koennen.

---

## Lesen Sie weiter

- [Architektur + Sicherheit](/help/ai/architecture/) — die
  Tiefe-Tour fuer Auditoren
- [Download](/download/) — alle Komponenten via APT-Repository
- [Source-Tree](https://git.forgeiec.io/ForgeIEC/forgeiec-studio)
- Frueheste Wurzeln:
  [Thiago Alves' OpenPLC v3](https://www.openplcproject.com/) — wo
  alles anfing
