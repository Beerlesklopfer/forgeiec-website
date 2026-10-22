---
title: "Partner"
summary: "Gemeinsam die Zukunft der Automatisierung schmieden"
---

## Partnerschaft bei ForgeIEC

ForgeIEC ist ein Open-Source-Projekt, das von der Überzeugung lebt,
dass industrielle Automatisierung für alle zugänglich sein muss.
Wir suchen Partner, die diese Vision teilen und bereit sind, die
Zukunft der Automatisierung aktiv mitzugestalten.

---

## Unsere Source-Repositories

Die Code-Basis liegt im **Forgejo** unter `git.forgeiec.io`.
Die Repositories sind nicht öffentlich einsehbar. Zugriff — lesend
wie schreibend — läuft über SSH: Sie schicken uns Ihren
SSH-Public-Key, wir schalten ihn frei. Danach können Sie den Code
vor einer Bewerbung durchsehen.

| Repository | Was drin ist | Forgejo |
|---|---|---|
| **forgeiec-studio** | C++/Qt6 IDE + Bus-Konfig + MCP-Server | [git.forgeiec.io/ForgeIEC/forgeiec-studio](https://git.forgeiec.io/ForgeIEC/forgeiec-studio) |
| **anvil** | Rust/Tokio PLC-Runtime + Bridge-Subprozess-Manager | [git.forgeiec.io/ForgeIEC/anvil](https://git.forgeiec.io/ForgeIEC/anvil) |
| **bellows** | OPC-UA/HMI-Gateway | [git.forgeiec.io/ForgeIEC/bellows](https://git.forgeiec.io/ForgeIEC/bellows) |
| **forgeiec-website** | Hugo-Site die Sie gerade lesen | [git.forgeiec.io/ForgeIEC/forgeiec-website](https://git.forgeiec.io/ForgeIEC/forgeiec-website) |

Jedes Repo enthält ein eigenes `documentation/architecture/`-
Unterverzeichnis bzw. eine Spec-Sammlung — wer dort tiefer
einsteigen will, findet die normativen RFC-2119-Specs in voller
Länge.

---

## Voraussetzungen

### Nachgewiesenes Open-Source-Engagement

Bewerber müssen bereits bewiesen haben, dass sie den Gedanken von
Open Source unterstützen. Das bedeutet:

- **Nachweisbare Beiträge** zu bestehenden Open-Source-Projekten
  (Commits, Pull Requests, Bug Reports, Dokumentation)
- **Öffentliches Profil** auf Plattformen wie GitHub, GitLab oder
  Codeberg
- **Aktive Teilnahme** an Open-Source-Communities — nicht nur
  Nutzung, sondern Mitgestaltung

Wir glauben, dass Taten mehr sagen als Worte. Wer Open Source nur
als Marketinginstrument betrachtet, ohne selbst beizutragen, passt
nicht zu unserer Philosophie.

### Gemeinsame Werte

- **Transparenz** — Offene Kommunikation, nachvollziehbare
  Entscheidungen
- **Zusammenarbeit** — Code Reviews, gemeinsame Architektur-
  Diskussionen, geteiltes Wissen
- **Qualität** — Dokumentierte Tests, sauberer Code,
  industrietaugliche Zuverlässigkeit
- **Langfristigkeit** — Partnerschaft ist kein Sprint, sondern ein
  Marathon

---

## Bereiche in denen wir konkret Unterstützung suchen

Wenn die Voraussetzungen oben für Sie passen — hier sind die
Subsysteme an denen wir besonders nach Mitstreitern suchen:

### 🔧 Bus-Bridges (tongs-*)

{{< components "tongs,anvild" >}}

- **tongs-ethercat** — DC-Sync, Slave-State-Machine, ENI-XML-Import
- **tongs-profibus** — DP-Master, GSD-Import-Toolchain
- **tongs-ethernetip** — CIP-Connections, EDS-Import
- **tongs-can** — CANopen + J1939

Skeleton + Fault-Model + IPC-Wire-Format stehen — der protokoll-
spezifische Teil fehlt.

### 🛠️ Studio-Editor-Features

{{< components "studio" >}}

- **FBD/LD/SFC-Editoren** — heute liegt der Fokus auf ST. Grafische
  Sprachen brauchen eigene Tree-sitter-Grammatik + Canvas-Renderer.
- **Vendor-Catalog-Pflege** — FDDs für weitere Hersteller (heute:
  Weidmueller). GSDML/EDS/ESI-Konverter sind willkommen.
- **Internationalisierung** — Studio + Website werden nach
  EN/DE/FR/ES/ZH/JA/TR/AR übersetzt; manche Sprachen sind nur
  maschinell vorbefüllt.

### 🌬️ HMI-Anbindung (bellowsd)

{{< components "bellowsd" >}}

- **OPC-UA-Companion-Specs** — bellowsd unterstützt heute generische
  OPC-UA-Knoten. Companion-Spec-Adapter (z.B. PackML,
  OPC-UA-Robotics) sind willkommen.
- **HMI-Frameworks** — `Hearth` ist als IIoT-Subscriber-Layer in
  Planung. Wer mit MQTT, Time-Series-DBs (InfluxDB, TimescaleDB)
  oder Grafana-Pipelines arbeitet, kann hier Architektur
  mitgestalten.

### 🔥 Runtime + Determinismus (anvild)

{{< components "anvild" >}}

- **Real-Time-Linux-Tuning** — PREEMPT_RT-Kernel, CPU-Pinning,
  Cache-Locality für Sub-Millisekunden-Cycle-Times
- **Rust+LLVM-Codegen (rusty)** — geplante Migration der Layer-1-
  Codegen weg von matiec/C-Output hin zu Rust+LLVM. Determinismus-
  Garantien + Online-Change-Vorbereitung.
- **Hardware-Targets** — Raspberry Pi, BeagleBone, industrielle
  x86, ARM-SBCs.

### 📚 Bildung + Dokumentation

{{< components "studio" >}}

- **Tutorials** — von „erstes Knight-Rider in 5 Minuten" bis
  „komplette Maschinensteuerung mit OPC-UA + EtherCAT"
- **Beispiel-Projekte** — heute liegen nur 2 Demos im Tree
- **Lehr-Curriculum** — Hochschulen die ForgeIEC als Lehr-IDE
  einsetzen wollen. Wir liefern Studio kostenlos, Dozenten bringen
  IEC-Curriculum.

---

## Was wir bieten

### Zugang zur ForgeIEC-Plattform

- Frühzeitiger Zugriff auf neue Features und Entwicklungszweige
- Direkter Draht zum Kernteam
- Möglichkeit, die Roadmap aktiv mitzugestalten

### Gemeinsame Entwicklung

- Gemeinsame Arbeit an industriellen Bussystem-Treibern
- Integration herstellerspezifischer Hardware
- Entwicklung branchenspezifischer Erweiterungen

### Technischer Support

- Priorisierte Fehlerbehebung
- Architektur-Beratung für eigene Erweiterungen
- Unterstützung bei der Integration in bestehende Systeme

---

## Formen der Partnerschaft

### Technologie-Partner

Hersteller von Automatisierungskomponenten, die ihre Hardware in
ForgeIEC integrieren möchten. Gemeinsame Treiberentwicklung,
Gerätekonfigurationen und Testverfahren.

### Integrations-Partner

Systemintegratoren und Ingenieursbüros, die ForgeIEC in
Kundenprojekten einsetzen. Praxiswissen fließt zurück in die
Entwicklung.

### Bildungs-Partner

Hochschulen und Ausbildungsstätten, die ForgeIEC in der Lehre
verwenden. Freier Zugang für den Bildungsbereich — die nächste
Generation von Automatisierungstechnikern sollte mit offenen
Werkzeugen lernen.

---

## Aktuell registrierte Partner

Stand 2026-05: noch keine externen Partner — die Plattform ist im
Aufbau-Sprint, Partner-Onboarding kommt sobald die ersten Subsystem-
APIs (Bridge-SDK, FDD-Format) stabilisiert sind.

Wenn Sie zu den ersten gehören wollen: siehe „Bewerbung" unten.

---

## Bewerbung

Sie möchten Partner werden? Schreiben Sie uns mit:

- Beschreibung Ihrer Organisation
- Links zu Ihren Open-Source-Beiträgen
- Ihre Motivation für eine Partnerschaft
- Konkreter Bereich, in dem Sie beitragen möchten
- Ihren SSH-Public-Key, wenn Sie den Code vorab durchsehen wollen

---

<div style="text-align:center; padding: 2rem;">

**Gemeinsam schmieden wir die Werkzeuge der Zukunft.**

blacksmith@forgeiec.io

</div>
