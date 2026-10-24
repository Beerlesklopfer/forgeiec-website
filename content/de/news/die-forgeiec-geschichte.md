---
title: "Vom ersten Byte an: die ForgeIEC-Geschichte"
date: 2026-05-13
weight: 1
summary: "Wie aus einem Fork von OpenPLC eine eigenständige IEC-61131-3-Plattform wurde — und warum"
components: [studio, anvild, tongs]
---

{{< components "studio,anvild,tongs" >}}

{{< callout type="note" title="Überarbeitet im Oktober 2026" >}}
Dieser Beitrag beschreibt den Stand vom Mai 2026. Im Oktober 2026 wurde
er an den heutigen Stand angepasst: matiec ist abgelöst, die
Sicherheitsangaben sind vereinheitlicht, die Herkunft ist ohne
Jahreszahl beschrieben.
{{< /callout >}}

## Der Anfang — ein Fork von OpenPLC

ForgeIEC begann als **Fork von OpenPLC** — der offenen SPS-Runtime von
**Thiago Alves** und ihren Mitwirkenden, geschrieben in C/C++ mit einer
webbasierten Konfigurations-Oberfläche in Python/Flask.
<!-- ENTWURF: Jahr des Forks offen — Git belegt eigene Arbeit erst ab Februar 2026 (Audit W-17); Eigentümer nennt 2018. Keine Jahreszahl, bis ein Beleg vorliegt. -->

OpenPLC hat einen klaren Wert: Sie können IEC 61131-3-Code auf
normaler Linux-Hardware ausführen, ohne kommerzielle Editor-Lizenz,
ohne Hersteller-Bindung. Modbus-Master, GPIO, Raspberry-Pi-Support —
alles drin.

Was OpenPLC nicht hat: einen ernsthaften **Editor**. Die Web-UI
ist gut für kleine Projekte, aber bei industrieller Komplexität
fällt sie zurück.

OpenPLC wird von seiner Gemeinschaft weiterentwickelt; ForgeIEC
übernimmt dieses Fundament und baut darauf auf. Den Compiler matiec
hat ForgeIEC inzwischen durch einen **eigenen, objektorientierungs­
fähigen Kern** ersetzt, der ST nach C++ übersetzt und auch METHOD,
INTERFACE und EXTENDS beherrscht.

---

## 2026-03-01: Der große Umbau beginnt

Mit dem Commit `82780f7`
am **1. März 2026** kommt der nächste Schritt: ein
**eigenständiger C++/Qt6-Editor** wird ins Repository
eingeführt. Native Desktop-Anwendung, kein Browser, kein
Python-Flask im UI-Pfad mehr.

Gleichen Tag der nächste Brocken: **gRPC-Client im Editor**, plus
das Backend wird zu `forgeiecd` umbenannt (commit `93ed9c9`).
Die alte HTTP-Webserver-Bedienung weicht einer modernen
**gRPC-Pipeline** mit Streaming + Protokoll-Versionierung.

Die nächsten Tage taktet es eng:

- **3. März** — Bus-System, Model/View-Refactor, F-Prefix-Renames
  (commit `dd85396`)
- **4. März** — EtherCAT + Profibus Bridges, CMake-Migration
- **5. März** — Hugo-Website als Submodul angelegt
- **6. März** — **DEL → Anvil**: das Shared-Memory-IPC-Subsystem
  bekommt seinen Industrie-Namen (commit `3fc636c`)
- **7. März** — **Forge Studio Branding**, Bridge-Family
  `anvil-*` benannt, Dirty-Bit-Verwaltung, BusModel MVC

In **eine Woche** wird aus einer Web-UI-Toolbox ein
**eigenständiger Desktop-Editor mit moderner Architektur**.

---

## März–April 2026: Die Architektur konsolidiert sich

Es folgen mehrere Wochen tiefer Refactor-Arbeit:

- **Debian-Pakete + CPack** (26. März) — kein manuelles
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
industrielle Komplexität trägt. `FAddressPool` als Single-Source-
of-Truth, Pool-Variablen als der einzige Container, alte
POU-VarLists nur noch als Spiegel.

Das ist die Grundlage dafür dass später die KI-Schicht
verlässlich operieren kann — sie sieht ein **konsistentes
Modell**, nicht eine Sammlung legacy gewachsener Datenstrukturen.

---

## Mai 2026: Sicherheit + KI

Mit dem Datenmodell stabil können die big-ticket-Sprints kommen:

- **2. Mai** — **Per-Variable Safety-Flags** (Cluster A): Force,
  Monitor, HMI-Export werden pro Variable einzeln gegated.
  Daraus wird später die Force-Sperre: dreifach gesperrt — beim
  Codegen, in der Runtime und im Editor; für die KI kommt eine vierte
  Sperre im MCP-Server hinzu.
- **8. Mai** — **MCP-Plattform**: Spec geschrieben, Sprint MCP-1
  (Prompts in QSettings).
- **9. Mai** — **Live-Diagnose-Pipeline** — FB-Member-Resolution,
  FLiveValueStore-Lifecycle-Fix.
- **10. Mai** — **Headless-Modus + Devloop-CLI** — für
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

Die Plattform ist aufgeteilt in sieben Bausteine, jeder mit eigener
Spec im `documentation/architecture/`-Verzeichnis des
Source-Trees:

| Subsystem | Spec | Rolle |
|---|---|---|
| **ForgeIEC Studio** | `mcp-platform-v1.md` | IDE — Editor + KI-Helfer + MCP-Server |
| **Anvil-Server (anvild)** | `anvil-platform-v2.md` | PLC-Runtime + Plug-In-Plattform + Online-Change |
| **Anvil (IPC)** | (in anvil-platform-v2 §13) | Zero-Copy-Shared-Memory zwischen Subsystemen |
| **tongs-* (Bridges)** | `tongs-platform-v1.md` | Feldbus-Plug-ins mit Fault-Model + FDD-Diag-Bits |
| **Bus-System** | `bus-system-v1.md` | Segmente/Devices/IEC-Zugriff |
| **Editor-Datenmodell** | `editor-data-v1.md` | FAddressPool SSoT + .forge-Format |
| **Codegen** | `codegen-v1.md` | eigener ST-Kern → C++ |

Alle Specs RFC-2119-normativ. Code + Spec gehen synchron — jede
Änderung durchläuft denselben Review-Prozess.

---

## Was ForgeIEC anders macht

| Andere | ForgeIEC |
|---|---|
| Proprietäre SPS-IDEs | AGPL-3.0-or-later; Ihr Projekt (generierter Code, Runtime-API, libanvil) unter Apache-2.0 |
| Vendor-Lock-in für Geräte | Hersteller-FDDs als First-Class-Citizen |
| KI nur als Code-completion-Plugin | KI als gleichberechtigter MCP-Client mit Audit-Log |
| Force-Setzungen ohne Schutzschicht | Force dreifach gesperrt (Codegen, Runtime, Editor), für die KI eine vierte Sperre |
| Monolithische Runtime | Modulare Bridge-Familie mit getrennten Daemons |
| Closed-Source-Binaries | Signierte Pakete aus einer automatisierten CI; Quellcode auf Anfrage |

---

## Wo es hingeht

Auf dem Sprint-Plan stehen:

- **Caretaker-Toggle-UI** in den Preferences — heute noch
  QSettings-Editieren
- **`team.revoke_peer` voll**, `team.rotate_cert`,
  `team.export_setup` — letzte Drittel der MCP-4b Phase-D
- **Anvil-Plattform v2**: Online-Change während laufender
  PLC-Cycle, Plug-In-Architektur für eigene Boundary-Typen
<!-- ENTWURF: Der Mai-Plan nannte hier eine Migration der Codegenerierung nach Rust+LLVM (rusty). Ob das noch Plan ist, entscheidet der Eigentümer (Audit W-16); bis dahin nicht genannt. -->
- **Hearth** — die Bedienoberfläche; heute als Vorschau über den
  Anvil-Bus verfügbar
- **Tongs-LoRaWAN** (Schwerpunkt), danach **Tongs-EtherCAT,
  Tongs-Profibus, Tongs-EthernetIP** voll implementiert

Der rote Faden bleibt: **eine offene, ehrliche Plattform** die
mit der industriellen Realität umgehen kann — keine bunten
Versprechen, kein Marketing-Lack, sondern belastbare Architektur-
Entscheidungen, die in der Spec stehen und die Sie im Quellcode
nachprüfen können (Einsicht auf Anfrage).

---

## Lesen Sie weiter

- [Architektur + Sicherheit](/de/help/ai/architecture/) — die
  Tiefe-Tour für Auditoren
- [Download](/de/download/) — alle Komponenten via APT-Repository
- Source-Tree: `ForgeIEC/forgeiec-studio` im Forgejo — Zugriff
  nach Freischaltung Ihres SSH-Public-Keys
- Früheste Wurzeln:
  [OpenPLC von Thiago Alves](https://www.openplcproject.com/) — wo
  alles anfing
